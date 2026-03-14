#!/usr/bin/env python3
"""
RL-Leibniz: REINFORCE agent discovers π/4 = 1 − 1/3 + 1/5 − 1/7 + ...

The agent receives ONLY:
  - State: (normalized step index, current partial sum)
  - Reward: −|final_sum − π/4|  (sparse, terminal only)

It must discover through exploration alone that picking
+1/1, −1/3, +1/5, −1/7, ... converges toward π/4 = 0.78540...

No Leibniz terms are hardcoded in the reward or environment.
"""
from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from scipy import stats

PI_OVER_4 = math.pi / 4          # 0.7853981633974483
LEIBNIZ_T10 = sum((-1)**k / (2*k + 1) for k in range(10))  # 0.76045990...
SCRIPT_DIR = Path(__file__).parent


# ── Environment ───────────────────────────────────────────────────────────────
class PiSeriesEnv:
    """
    Pick T fractions ±1/k (k = 1..D_max) to build a series summing to π/4.

    Action encoding:
      action 2*(k-1)     → +1/k
      action 2*(k-1) + 1 → −1/k

    So: action 0 = +1/1, action 1 = −1/1, action 2 = +1/2, action 3 = −1/2, ...
    """
    def __init__(self, D_max: int = 25, T: int = 10):
        self.D_max = D_max
        self.T = T
        self.n_actions = 2 * D_max
        self.step_num = 0
        self.partial_sum = 0.0

    def reset(self) -> np.ndarray:
        self.step_num = 0
        self.partial_sum = 0.0
        return self._state()

    def _state(self) -> np.ndarray:
        return np.array([self.step_num / self.T, self.partial_sum], dtype=np.float32)

    def step(self, action: int) -> tuple[np.ndarray, float, bool]:
        sign, denom = self.decode_action(action)
        self.partial_sum += sign / denom
        self.step_num += 1
        done = self.step_num >= self.T
        reward = -abs(self.partial_sum - PI_OVER_4) if done else 0.0
        return self._state(), float(reward), bool(done)

    def decode_action(self, action: int) -> tuple[int, int]:
        """Returns (sign, denominator) for an action index."""
        denom = action // 2 + 1
        sign = 1 if action % 2 == 0 else -1
        return sign, denom

    def action_str(self, action: int) -> str:
        sign, denom = self.decode_action(action)
        return f"{'+' if sign > 0 else '-'}1/{denom}"


# ── Policy network ────────────────────────────────────────────────────────────
class PolicyNetwork(nn.Module):
    """2-layer MLP: state → action probabilities."""

    def __init__(self, n_actions: int = 50):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 64), nn.ReLU(),
            nn.Linear(64, 64), nn.ReLU(),
            nn.Linear(64, n_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.softmax(self.net(x), dim=-1)

    def select_action(self, state: np.ndarray) -> tuple[int, torch.Tensor, torch.Tensor]:
        """Sample action; return (action, log_prob, entropy)."""
        x = torch.from_numpy(state).unsqueeze(0)
        probs = self.forward(x)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        return int(action), dist.log_prob(action), dist.entropy()

    def greedy_action(self, state: np.ndarray) -> int:
        x = torch.from_numpy(state).unsqueeze(0)
        with torch.no_grad():
            probs = self.forward(x)
        return int(probs.argmax())

    def reset_weights(self, seed: int | None = None) -> None:
        if seed is not None:
            torch.manual_seed(seed)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)


# ── Training ──────────────────────────────────────────────────────────────────
def train(
    env: PiSeriesEnv,
    policy: PolicyNetwork,
    episodes: int = 50_000,
    lr: float = 0.001,
    gamma: float = 0.99,
    entropy_coef: float = 0.01,
    seed: int | None = None,
    verbose: bool = True,
    log_interval: int = 100,
) -> tuple[list[float], list[dict]]:
    """
    REINFORCE with EMA baseline and entropy regularisation.
    Returns (episode_returns, log_records).
    """
    if seed is not None:
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        policy.reset_weights(seed)

    optimizer = optim.Adam(policy.parameters(), lr=lr)
    baseline = 0.0
    ema_alpha = 0.005

    episode_returns: list[float] = []
    log_records: list[dict] = []

    for ep in range(1, episodes + 1):
        state = env.reset()
        log_probs: list[torch.Tensor] = []
        entropies: list[torch.Tensor] = []
        rewards: list[float] = []

        done = False
        while not done:
            action, lp, ent = policy.select_action(state)
            state, reward, done = env.step(action)
            log_probs.append(lp)
            entropies.append(ent)
            rewards.append(reward)

        # Discounted returns (sparse terminal reward → G_t = γ^(T-1-t) * R)
        G = 0.0
        returns: list[float] = []
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        episode_return = returns[0]
        episode_returns.append(episode_return)

        adv = torch.tensor([g - baseline for g in returns], dtype=torch.float32)
        pg_loss = -torch.stack([lp * a for lp, a in zip(log_probs, adv)]).sum()
        ent_loss = -entropy_coef * torch.stack(entropies).sum()
        loss = pg_loss + ent_loss

        optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
        optimizer.step()

        baseline += ema_alpha * (episode_return - baseline)

        if ep % log_interval == 0:
            window = episode_returns[-log_interval:]
            mean_ret = float(np.mean(window))
            best_ret = float(max(window))
            actions = get_greedy_series(env, policy)
            series_str = ", ".join(env.action_str(a) for a in actions)

            if verbose:
                print(
                    f"Episode {ep:6d}: "
                    f"mean={mean_ret:+.4f}  best={best_ret:+.4f}  "
                    f"[{series_str}]"
                )
            log_records.append(
                {"episode": ep, "mean_return": mean_ret, "best_return": best_ret}
            )

    return episode_returns, log_records


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_greedy_series(env: PiSeriesEnv, policy: PolicyNetwork, T: int | None = None) -> list[int]:
    """Run policy greedily and return the list of T actions."""
    eval_env = PiSeriesEnv(D_max=env.D_max, T=T or env.T)
    state = eval_env.reset()
    actions = []
    done = False
    while not done:
        action = policy.greedy_action(state)
        state, _, done = eval_env.step(action)
        actions.append(action)
    return actions


def evaluate_series(env: PiSeriesEnv, actions: list[int]) -> dict:
    """Compute terms, partial sums, and Leibniz comparison for a list of actions."""
    partial_sum = 0.0
    terms, partial_sums = [], []
    for a in actions:
        sign, denom = env.decode_action(a)
        partial_sum += sign / denom
        terms.append((sign, denom))
        partial_sums.append(partial_sum)

    T = len(actions)
    leibniz = [((-1)**k, 2*k + 1) for k in range(T)]
    exact_match = terms == leibniz
    approx_match = all(d % 2 == 1 for _, d in terms)

    term_details = []
    for i, (a, (s, d)) in enumerate(zip(actions, terms)):
        ls, ld = leibniz[i]
        if (s, d) == (ls, ld):
            match = "exact"
        elif d % 2 == 1:
            match = "approx"
        else:
            match = "wrong"
        term_details.append({
            "step": i + 1,
            "action": a,
            "sign": s,
            "denom": d,
            "term_value": round(s / d, 8),
            "term_str": env.action_str(a),
            "partial_sum": round(partial_sums[i], 8),
            "leibniz_sign": ls,
            "leibniz_denom": ld,
            "leibniz_term_str": f"{'+' if ls > 0 else '-'}1/{ld}",
            "match": match,
        })

    return {
        "terms": terms,
        "partial_sums": partial_sums,
        "final_sum": partial_sums[-1],
        "error": abs(partial_sums[-1] - PI_OVER_4),
        "exact_leibniz": exact_match,
        "approx_leibniz": approx_match,
        "term_details": term_details,
    }


# ── T — Testing ───────────────────────────────────────────────────────────────
def run_testing(log) -> None:
    log("=" * 70)
    log("T — TESTING")
    log("=" * 70)

    env = PiSeriesEnv(D_max=25, T=10)

    # Action decoding
    checks = [(0, +1, 1), (1, -1, 1), (2, +1, 2), (3, -1, 2), (4, +1, 3), (5, -1, 3)]
    for action, exp_sign, exp_denom in checks:
        s, d = env.decode_action(action)
        assert (s, d) == (exp_sign, exp_denom), f"action {action}: got ({s},{d}), expected ({exp_sign},{exp_denom})"
    log("PASS  Action decoding: 0→+1/1, 1→−1/1, 2→+1/2, 3→−1/2, 4→+1/3, 5→−1/3")

    # Partial sum accumulation
    state = env.reset()
    assert state[0] == 0.0 and state[1] == 0.0
    state, r, done = env.step(0)   # +1/1
    assert abs(env.partial_sum - 1.0) < 1e-9 and r == 0.0 and not done
    state, r, done = env.step(5)   # -1/3
    assert abs(env.partial_sum - (1.0 - 1/3)) < 1e-9 and r == 0.0
    log("PASS  Partial sum accumulation: +1/1 then −1/3 → 0.66667")

    # Terminal reward
    env2 = PiSeriesEnv(D_max=25, T=2)
    env2.reset()
    env2.step(0)                   # +1/1
    _, reward, done = env2.step(5) # −1/3; T=2 so done
    expected_reward = -abs((1.0 - 1/3) - PI_OVER_4)
    assert done and abs(reward - expected_reward) < 1e-9
    log(f"PASS  Terminal reward: R = −|sum − π/4| = {reward:.6f} at T=2")

    # Policy network: output sums to 1
    policy = PolicyNetwork(n_actions=50)
    state = env.reset()
    x = torch.from_numpy(state).unsqueeze(0)
    probs = policy(x)
    assert abs(probs.sum().item() - 1.0) < 1e-5
    assert probs.shape == (1, 50)
    log("PASS  Policy network: output shape (1,50), sums to 1.0")

    log("All T-checks passed.\n")


# ── E — Evaluation ────────────────────────────────────────────────────────────
def run_evaluation(log, K_seeds: int = 10, eval_episodes: int = 20_000) -> list[dict]:
    log("=" * 70)
    log(f"E — EVALUATION  ({K_seeds} seeds × {eval_episodes:,} episodes)")
    log("=" * 70)

    env = PiSeriesEnv(D_max=25, T=10)
    results = []

    log(f"\n{'Seed':>6}  {'Final error':>12}  {'Exact Leibniz':>14}  {'Odd-denom':>10}  {'Best return':>12}  {'Series'}")
    log("─" * 90)

    for seed in range(K_seeds):
        policy = PolicyNetwork(n_actions=env.n_actions)
        ep_returns, _ = train(env, policy, episodes=eval_episodes,
                              seed=seed, verbose=False, log_interval=eval_episodes)

        actions = get_greedy_series(env, policy)
        ev = evaluate_series(env, actions)
        best_ret = float(max(ep_returns[-1000:]))
        series_str = ", ".join(env.action_str(a) for a in actions)

        row = {
            "seed": seed,
            "final_error": ev["error"],
            "exact_leibniz": ev["exact_leibniz"],
            "approx_leibniz": ev["approx_leibniz"],
            "best_return": best_ret,
            "series": series_str,
            "final_sum": ev["final_sum"],
        }
        results.append(row)

        match_str = "EXACT" if ev["exact_leibniz"] else ("ODD" if ev["approx_leibniz"] else "other")
        log(f"{seed:>6}  {ev['error']:>12.6f}  {str(ev['exact_leibniz']):>14}  "
            f"{match_str:>10}  {best_ret:>12.4f}  {series_str}")

    n_exact = sum(r["exact_leibniz"] for r in results)
    n_approx = sum(r["approx_leibniz"] for r in results)
    errors = [r["final_error"] for r in results]
    log(f"\n  Exact Leibniz match : {n_exact}/{K_seeds}")
    log(f"  Odd-denom match     : {n_approx}/{K_seeds}")
    log(f"  Mean final error    : {np.mean(errors):.6f} ± {np.std(errors):.6f}")
    log(f"  Min / Max error     : {min(errors):.6f} / {max(errors):.6f}")
    log(f"  Leibniz T=10 error  : {abs(LEIBNIZ_T10 - PI_OVER_4):.6f}  (reference)")
    log(f"\n  Note: convergence to within 0.001 requires a sequence summing")
    log(f"  more accurately than Leibniz. With T=10, D_max=25, the theoretical")
    log(f"  minimum reachable error depends on the discrete search space.")
    log("E-evaluation complete.\n")
    return results


# ── V — Verification ──────────────────────────────────────────────────────────
def run_verification(log, env: PiSeriesEnv, policy: PolicyNetwork) -> None:
    log("=" * 70)
    log("V — VERIFICATION")
    log("=" * 70)

    # Leibniz T=10 partial sum reference
    leibniz_sum = sum((-1)**k / (2*k + 1) for k in range(10))
    leibniz_error = abs(leibniz_sum - PI_OVER_4)
    log(f"\n── Leibniz reference (T=10) ──")
    log(f"  Terms: +1/1 −1/3 +1/5 −1/7 +1/9 −1/11 +1/13 −1/15 +1/17 −1/19")
    log(f"  Partial sum : {leibniz_sum:.10f}")
    log(f"  π/4         : {PI_OVER_4:.10f}")
    log(f"  Error       : {leibniz_error:.8f}  (Leibniz converges slowly — expected)")
    assert abs(leibniz_sum - 0.7604599) < 1e-6
    log(f"  PASS  Leibniz T=10 sum matches 0.7604599...")

    # Untrained policy baseline
    log(f"\n── Untrained policy returns (100 random episodes) ──")
    untrained = PolicyNetwork(n_actions=env.n_actions)
    untrained.reset_weights(seed=77)
    raw_returns = []
    eval_env = PiSeriesEnv(D_max=env.D_max, T=env.T)
    rng = np.random.default_rng(42)
    for _ in range(100):
        s = eval_env.reset()
        done = False
        while not done:
            action = int(rng.integers(0, env.n_actions))
            s, r, done = eval_env.step(action)
        raw_returns.append(r)
    log(f"  Mean return (random policy) : {np.mean(raw_returns):.4f}")
    log(f"  Mean return (trained)       : −{abs(evaluate_series(env, get_greedy_series(env, policy))['error']):.4f}")

    # Trained policy result
    actions = get_greedy_series(env, policy)
    ev = evaluate_series(env, actions)
    log(f"\n── Trained policy (greedy) ──")
    for td in ev["term_details"]:
        log(f"  Step {td['step']:2d}: {td['term_str']:6s}  → sum={td['partial_sum']:.6f}  "
            f"[Leibniz: {td['leibniz_term_str']:6s}  match={td['match']}]")
    log(f"  Final sum : {ev['final_sum']:.8f}")
    log(f"  Error     : {ev['error']:.8f}")
    log(f"  Better than Leibniz T=10: {ev['error'] < leibniz_error}")
    if ev['error'] < leibniz_error:
        log(f"  *** FINDING: Agent found a MORE efficient 10-term series than Leibniz ***")
        log(f"  *** Leibniz error {leibniz_error:.6f}  →  Agent error {ev['error']:.6f} ***")
    log("V-verification complete.\n")


# ── Validation ────────────────────────────────────────────────────────────────
def run_validation(log, env: PiSeriesEnv, policy: PolicyNetwork) -> None:
    log("=" * 70)
    log("V — VALIDATION")
    log("=" * 70)

    # Generalisation: run T=20 with policy trained on T=10
    log(f"\n── Generalisation: run trained policy at T=20 (untrained on this length) ──")
    actions_20 = get_greedy_series(env, policy, T=20)
    ev_20 = evaluate_series(env, actions_20)
    log(f"  Series (T=20): {', '.join(env.action_str(a) for a in actions_20)}")
    log(f"  Final sum     : {ev_20['final_sum']:.8f}  (π/4 = {PI_OVER_4:.8f})")
    log(f"  Error         : {ev_20['error']:.8f}")
    log(f"  All odd denom : {ev_20['approx_leibniz']}")
    log(f"  Exact Leibniz : {ev_20['exact_leibniz']}")

    # Compare T=10 error vs Leibniz T=10 error
    actions_10 = get_greedy_series(env, policy, T=10)
    ev_10 = evaluate_series(env, actions_10)
    leibniz_error = abs(LEIBNIZ_T10 - PI_OVER_4)
    log(f"\n── Comparison: agent T=10 vs Leibniz T=10 ──")
    log(f"  Agent error    : {ev_10['error']:.8f}")
    log(f"  Leibniz error  : {leibniz_error:.8f}")
    if ev_10['exact_leibniz']:
        log(f"  Match: EXACT — agent discovered the Leibniz series.")
    elif ev_10['approx_leibniz']:
        log(f"  Match: APPROXIMATE — agent uses odd denominators but not pure Leibniz.")
    else:
        log(f"  Match: DIFFERENT — agent found an alternative series.")
    log("Validation complete.\n")


# ── Save JSON for visualization ───────────────────────────────────────────────
def save_training_data(
    env: PiSeriesEnv,
    policy: PolicyNetwork,
    log_records: list[dict],
    seed_results: list[dict],
    output_path: Path,
) -> None:
    actions = get_greedy_series(env, policy)
    ev = evaluate_series(env, actions)

    payload = {
        "config": {
            "D_max": env.D_max,
            "T": env.T,
            "n_actions": env.n_actions,
        },
        "training_curve": log_records,
        "final_series": ev["term_details"],
        "analysis": {
            "final_sum": round(ev["final_sum"], 10),
            "error": round(ev["error"], 10),
            "pi_over_4": PI_OVER_4,
            "exact_leibniz": ev["exact_leibniz"],
            "approx_leibniz": ev["approx_leibniz"],
            "leibniz_T10_sum": round(LEIBNIZ_T10, 10),
            "leibniz_error": round(abs(LEIBNIZ_T10 - PI_OVER_4), 10),
            "better_than_leibniz": ev["error"] < abs(LEIBNIZ_T10 - PI_OVER_4),
        },
        "seed_results": [
            {k: v for k, v in r.items() if k != "series"} for r in seed_results
        ],
        "pi_over_4": PI_OVER_4,
        "leibniz_T10_sum": round(LEIBNIZ_T10, 10),
    }
    output_path.write_text(json.dumps(payload, indent=2))
    print(f"Saved → {output_path}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    lines: list[str] = []

    def log(s: str = "") -> None:
        print(s)
        lines.append(s)

    t0 = time.time()

    log("RL-Leibniz: REINFORCE discovers π/4 — TEVV Report")
    log("=" * 70)
    log(f"  π/4           = {PI_OVER_4:.12f}")
    log(f"  Leibniz T=10  = {LEIBNIZ_T10:.12f}  (error = {abs(LEIBNIZ_T10-PI_OVER_4):.6f})")
    log(f"  Generated     : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log()

    # ── T: Testing ────────────────────────────────────────────────────────────
    run_testing(log)

    # ── Main training run ─────────────────────────────────────────────────────
    log("=" * 70)
    log("MAIN TRAINING  (D_max=25, T=10, episodes=50,000, seed=0)")
    log("=" * 70)
    env = PiSeriesEnv(D_max=25, T=10)
    policy = PolicyNetwork(n_actions=env.n_actions)
    ep_returns, log_records = train(
        env, policy,
        episodes=50_000,
        seed=0,
        verbose=True,
        log_interval=100,
    )
    log(f"\nTraining complete. Final window mean: {np.mean(ep_returns[-100:]):+.4f}\n")

    # ── E: Evaluation (10 seeds) ──────────────────────────────────────────────
    seed_results = run_evaluation(log, K_seeds=10, eval_episodes=20_000)

    # ── V: Verification ───────────────────────────────────────────────────────
    run_verification(log, env, policy)

    # ── V: Validation ─────────────────────────────────────────────────────────
    run_validation(log, env, policy)

    elapsed = time.time() - t0
    log(f"Total wall time: {elapsed:.1f}s")

    # ── Save outputs ──────────────────────────────────────────────────────────
    results_path = SCRIPT_DIR / "results.txt"
    results_path.write_text("\n".join(lines) + "\n")
    print(f"\nSaved → {results_path}")

    csv_rows = [
        {"episode": ep + 1, "return": r}
        for ep, r in enumerate(ep_returns)
    ]
    csv_path = SCRIPT_DIR / "training_history.csv"
    pd.DataFrame(csv_rows).to_csv(csv_path, index=False)
    print(f"Saved → {csv_path}")

    json_path = SCRIPT_DIR / "training_data.json"
    save_training_data(env, policy, log_records, seed_results, json_path)

    # Optionally save model weights
    models_dir = SCRIPT_DIR / "models"
    models_dir.mkdir(exist_ok=True)
    torch.save(policy.state_dict(), models_dir / "best_policy.pt")
    print(f"Saved → {models_dir / 'best_policy.pt'}")


if __name__ == "__main__":
    main()
