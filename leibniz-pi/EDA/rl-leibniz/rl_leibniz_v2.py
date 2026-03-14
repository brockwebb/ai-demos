#!/usr/bin/env python3
"""
RL-Leibniz v2: Redesigned REINFORCE with curriculum learning, two-headed
actions, and dense per-step reward.

Key changes from v1:
  - Two-headed action (sign head + denominator head): separable concepts
  - Previous term added to state: enables sign-alternation learning
  - Per-step reward 0.1 × (old_error − new_error): dense progress signal
  - Variable episode length T ~ [T_min, T_max] per episode
  - Curriculum: T ranges grow across three phases of training
  - Wider backbone: 128 units vs 64
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

PI_OVER_4 = math.pi / 4
SCRIPT_DIR = Path(__file__).parent


def leibniz_sum(T: int) -> float:
    return sum((-1)**k / (2*k + 1) for k in range(T))


LEIBNIZ_REFS = {T: leibniz_sum(T) for T in (10, 20, 50, 100)}


# ── Environment ───────────────────────────────────────────────────────────────
class PiSeriesEnvV2:
    """
    Two-headed action space:
      sign_action:  0 → +1,  1 → −1
      denom_action: k → denominator (k + 1)

    State: [step / T_max,  partial_sum,  previous_term]
    """
    T_NORM = 40  # constant normalisation so step feature stays in [0, 1] for T ≤ 40

    def __init__(self, D_max: int = 30):
        self.D_max = D_max
        self.current_T = 10
        self.step_num = 0
        self.partial_sum = 0.0
        self.prev_term = 0.0

    def reset(self, T: int | None = None) -> np.ndarray:
        self.current_T = T if T is not None else 10
        self.step_num = 0
        self.partial_sum = 0.0
        self.prev_term = 0.0
        return self._state()

    def _state(self) -> np.ndarray:
        return np.array(
            [self.step_num / self.T_NORM, self.partial_sum, self.prev_term],
            dtype=np.float32,
        )

    def step(self, sign_action: int, denom_action: int):
        sign = 1 if sign_action == 0 else -1
        denom = denom_action + 1
        term = sign / denom

        old_error = abs(self.partial_sum - PI_OVER_4)
        self.partial_sum += term
        new_error = abs(self.partial_sum - PI_OVER_4)
        self.prev_term = term
        self.step_num += 1

        done = self.step_num >= self.current_T

        # Dense per-step reward (scale 0.1 to stay subordinate to terminal)
        step_reward = 0.1 * (old_error - new_error)
        terminal_reward = -new_error if done else 0.0
        reward = step_reward + terminal_reward

        return self._state(), float(reward), bool(done)

    def term_str(self, sign_action: int, denom_action: int) -> str:
        sign = 1 if sign_action == 0 else -1
        denom = denom_action + 1
        return f"{'+' if sign > 0 else '-'}1/{denom}"


# ── Policy ────────────────────────────────────────────────────────────────────
class PolicyNetworkV2(nn.Module):
    """
    Shared 3→128→128 backbone with two independent heads:
      sign_head:  → softmax(2)
      denom_head: → softmax(D_max)
    """
    def __init__(self, D_max: int = 30):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(3, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
        )
        self.sign_head  = nn.Linear(128, 2)
        self.denom_head = nn.Linear(128, D_max)

    def forward(self, x: torch.Tensor):
        h = self.backbone(x)
        return (
            F.softmax(self.sign_head(h),  dim=-1),
            F.softmax(self.denom_head(h), dim=-1),
        )

    def select_action(self, state: np.ndarray):
        """Sample (sign_a, denom_a, joint_log_prob, joint_entropy)."""
        x = torch.from_numpy(state).unsqueeze(0)
        sp, dp = self.forward(x)
        sd = torch.distributions.Categorical(sp)
        dd = torch.distributions.Categorical(dp)
        sa = sd.sample()
        da = dd.sample()
        lp  = sd.log_prob(sa) + dd.log_prob(da)
        ent = sd.entropy()    + dd.entropy()
        return int(sa), int(da), lp, ent

    def greedy_action(self, state: np.ndarray) -> tuple[int, int]:
        x = torch.from_numpy(state).unsqueeze(0)
        with torch.no_grad():
            sp, dp = self.forward(x)
        return int(sp.argmax()), int(dp.argmax())

    def reset_weights(self, seed: int | None = None) -> None:
        if seed is not None:
            torch.manual_seed(seed)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)


# ── Curriculum ────────────────────────────────────────────────────────────────
def get_T_range(episode: int, total: int = 100_000) -> tuple[int, int]:
    """Three-phase curriculum: T ranges grow as training progresses."""
    if episode <= 10_000:
        return 3, 10
    elif episode <= 50_000:
        return 5, 25
    else:
        return 10, 40


# ── Training ──────────────────────────────────────────────────────────────────
def train_v2(
    env: PiSeriesEnvV2,
    policy: PolicyNetworkV2,
    episodes: int = 100_000,
    lr: float = 3e-4,
    gamma: float = 0.99,
    entropy_coef: float = 0.01,
    seed: int | None = None,
    verbose: bool = True,
    log_interval: int = 500,
) -> tuple[list[float], list[dict]]:
    if seed is not None:
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        policy.reset_weights(seed)

    optimizer = optim.Adam(policy.parameters(), lr=lr)
    baseline = 0.0
    ema_alpha = 0.01

    episode_returns: list[float] = []
    log_records: list[dict] = []

    for ep in range(1, episodes + 1):
        T_min, T_max = get_T_range(ep, episodes)
        T = random.randint(T_min, T_max)
        state = env.reset(T=T)

        log_probs:  list[torch.Tensor] = []
        entropies:  list[torch.Tensor] = []
        rewards:    list[float]        = []

        done = False
        while not done:
            sa, da, lp, ent = policy.select_action(state)
            state, reward, done = env.step(sa, da)
            log_probs.append(lp)
            entropies.append(ent)
            rewards.append(reward)

        G = 0.0
        returns: list[float] = []
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        episode_return = returns[0]
        episode_returns.append(episode_return)

        adv = torch.tensor([g - baseline for g in returns], dtype=torch.float32)
        pg_loss  = -torch.stack([lp * a for lp, a in zip(log_probs, adv)]).sum()
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
            T_lo, T_hi = get_T_range(ep, episodes)

            # Greedy series at T=10 for logging
            terms10 = get_greedy_terms(env, policy, T=10)
            series_str = ", ".join(
                env.term_str(sa, da) for sa, da in terms10
            )
            pattern = detect_leibniz([s / (d + 1) for s, d in
                                      [(1 if sa == 0 else -1, da) for sa, da in terms10]])

            if verbose:
                phase = ("1" if ep <= 10_000 else "2" if ep <= 50_000 else "3")
                flag = " ★LEIBNIZ★" if pattern["is_leibniz"] else (
                       " (alt-sign)" if pattern["signs_alternate"] else "")
                print(
                    f"Ep {ep:6d} [ph{phase} T∈[{T_lo},{T_hi}]]: "
                    f"mean={mean_ret:+.4f}  best={best_ret:+.4f}  "
                    f"[{series_str}]{flag}"
                )
            log_records.append({
                "episode": ep,
                "mean_return": mean_ret,
                "best_return": best_ret,
                "T_lo": T_lo,
                "T_hi": T_hi,
            })

    return episode_returns, log_records


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_greedy_terms(
    env: PiSeriesEnvV2, policy: PolicyNetworkV2, T: int
) -> list[tuple[int, int]]:
    """Greedy rollout for T steps; returns list of (sign_action, denom_action)."""
    state = env.reset(T=T)
    actions = []
    done = False
    while not done:
        sa, da = policy.greedy_action(state)
        state, _, done = env.step(sa, da)
        actions.append((sa, da))
    return actions


def actions_to_terms(actions: list[tuple[int, int]]) -> list[float]:
    """Convert (sign_action, denom_action) pairs to float term values."""
    return [(1 if sa == 0 else -1) / (da + 1) for sa, da in actions]


def detect_leibniz(terms: list[float], tolerance: float = 0.01) -> dict:
    """
    Check if a list of float term values approximates the Leibniz pattern.
    Leibniz: signs alternate, denominators are consecutive odd integers 1,3,5,...
    """
    if len(terms) < 2:
        return {"signs_alternate": True, "denoms_odd": True,
                "denoms_increasing": True, "is_leibniz": False}

    signs_alternate = all(
        terms[i] * terms[i + 1] < 0 for i in range(len(terms) - 1)
    )
    denoms = [abs(1.0 / t) for t in terms if t != 0]
    denoms_odd = all(
        abs(d - round(d)) < tolerance and round(d) % 2 == 1
        for d in denoms
    )
    denoms_increasing = all(denoms[i] < denoms[i + 1] for i in range(len(denoms) - 1))

    return {
        "signs_alternate": signs_alternate,
        "denoms_odd": denoms_odd,
        "denoms_increasing": denoms_increasing,
        "is_leibniz": signs_alternate and denoms_odd and denoms_increasing,
    }


def evaluate_at_T(
    env: PiSeriesEnvV2,
    policy: PolicyNetworkV2,
    T: int,
) -> dict:
    """Full evaluation of greedy policy at a given T."""
    actions = get_greedy_terms(env, policy, T=T)
    terms = actions_to_terms(actions)
    partial_sums = []
    s = 0.0
    for t in terms:
        s += t
        partial_sums.append(s)
    final_sum = partial_sums[-1]
    error = abs(final_sum - PI_OVER_4)
    pattern = detect_leibniz(terms)
    leibniz_ref = LEIBNIZ_REFS.get(T, leibniz_sum(T))

    term_details = []
    leibniz_terms = [((-1)**k, 2*k + 1) for k in range(T)]
    for i, (a, t, ps) in enumerate(zip(actions, terms, partial_sums)):
        sa, da = a
        sign = 1 if sa == 0 else -1
        denom = da + 1
        ls, ld = leibniz_terms[i] if i < len(leibniz_terms) else (0, 0)
        if sign == ls and denom == ld:
            match = "exact"
        elif denom % 2 == 1:
            match = "approx"
        else:
            match = "wrong"
        term_details.append({
            "step": i + 1,
            "sign_action": sa,
            "denom_action": da,
            "sign": sign,
            "denom": denom,
            "term_value": round(t, 8),
            "term_str": env.term_str(sa, da),
            "partial_sum": round(ps, 8),
            "leibniz_sign": int(ls),
            "leibniz_denom": int(ld),
            "leibniz_term_str": f"{'+' if ls>0 else '-'}1/{ld}" if ld else "—",
            "match": match,
        })

    return {
        "T": T,
        "final_sum": final_sum,
        "error": error,
        "leibniz_sum": leibniz_ref,
        "leibniz_error": abs(leibniz_ref - PI_OVER_4),
        "better_than_leibniz": error < abs(leibniz_ref - PI_OVER_4),
        "pattern": pattern,
        "term_details": term_details,
    }


# ── T — Testing ───────────────────────────────────────────────────────────────
def run_testing(log) -> None:
    log("=" * 70)
    log("T — TESTING")
    log("=" * 70)

    env = PiSeriesEnvV2(D_max=30)

    # Sign head: 0 → +1, 1 → −1
    state = env.reset(T=5)
    _, r0, _ = env.step(0, 0)   # +1/1
    assert abs(env.partial_sum - 1.0) < 1e-9
    log("PASS  sign_action=0 → +1/1  (partial_sum=1.0)")

    env.reset(T=5)
    env.step(1, 0)              # −1/1
    assert abs(env.partial_sum - (-1.0)) < 1e-9
    log("PASS  sign_action=1 → −1/1  (partial_sum=−1.0)")

    # Denom head: action k → denom k+1
    env.reset(T=5)
    env.step(0, 2)              # +1/3
    assert abs(env.partial_sum - (1/3)) < 1e-9
    log("PASS  denom_action=2 → +1/3")

    # Per-step reward: positive when error decreases
    env.reset(T=5)
    old_err = abs(0.0 - PI_OVER_4)      # 0.785...
    _, r, _ = env.step(0, 0)            # +1/1, sum=1.0
    new_err = abs(1.0 - PI_OVER_4)      # 0.215...
    expected_step = 0.1 * (old_err - new_err)
    assert abs(r - expected_step) < 1e-9   # no terminal reward at step 1 of T=5
    log(f"PASS  Per-step reward = {r:.6f} (positive: sum moved toward π/4)")

    # Terminal reward = −|sum − π/4| on last step
    env2 = PiSeriesEnvV2(D_max=30)
    env2.reset(T=2)
    env2.step(0, 0)   # +1/1, not terminal
    _, r_term, done = env2.step(1, 2)   # −1/3, terminal
    expected_step_r = 0.1 * (abs(1.0 - PI_OVER_4) - abs((1.0 - 1/3) - PI_OVER_4))
    expected_term_r = -abs((1.0 - 1/3) - PI_OVER_4)
    assert done
    assert abs(r_term - (expected_step_r + expected_term_r)) < 1e-9
    log(f"PASS  Terminal reward at T=2: {r_term:.6f} = step_r + terminal_r")

    # Variable episode length
    env3 = PiSeriesEnvV2(D_max=30)
    env3.reset(T=3)
    env3.step(0, 0)
    env3.step(0, 0)
    _, _, done = env3.step(0, 0)
    assert done
    log("PASS  Episode terminates at T=3")

    env3.reset(T=7)
    for _ in range(6):
        env3.step(0, 0)
    _, _, done7 = env3.step(0, 0)
    assert done7
    log("PASS  Episode terminates at T=7")

    # Curriculum ranges
    assert get_T_range(1)       == (3, 10)
    assert get_T_range(10_000)  == (3, 10)
    assert get_T_range(10_001)  == (5, 25)
    assert get_T_range(50_000)  == (5, 25)
    assert get_T_range(50_001)  == (10, 40)
    assert get_T_range(100_000) == (10, 40)
    log("PASS  Curriculum phase boundaries: [1,10K]→(3,10), [10K,50K]→(5,25), [50K,100K]→(10,40)")

    # Policy network shape
    policy = PolicyNetworkV2(D_max=30)
    x = torch.zeros(1, 3)
    sp, dp = policy(x)
    assert sp.shape == (1, 2) and dp.shape == (1, 30)
    assert abs(sp.sum().item() - 1.0) < 1e-5
    assert abs(dp.sum().item() - 1.0) < 1e-5
    log("PASS  Policy: sign head (1,2) + denom head (1,30), both sum to 1.0")

    log("All T-checks passed.\n")


# ── V — Verification ──────────────────────────────────────────────────────────
def run_verification(log, env: PiSeriesEnvV2, policy: PolicyNetworkV2) -> None:
    log("=" * 70)
    log("V — VERIFICATION")
    log("=" * 70)

    # Leibniz reference values
    log("\n── Leibniz reference partial sums ──")
    for T, ref in LEIBNIZ_REFS.items():
        err = abs(ref - PI_OVER_4)
        log(f"  T={T:>4d}: sum={ref:.8f}  error={err:.8f}")
    assert abs(LEIBNIZ_REFS[10]  - 0.7604599) < 1e-6
    assert abs(LEIBNIZ_REFS[20]  - 0.7729059) < 1e-6
    assert abs(LEIBNIZ_REFS[50]  - 0.7803980) < 1e-6
    log("PASS  All Leibniz reference values verified")

    # Untrained baseline
    log("\n── Untrained policy baseline (100 random episodes, T=10) ──")
    fresh = PolicyNetworkV2(D_max=env.D_max)
    fresh.reset_weights(seed=42)
    rng = np.random.default_rng(0)
    raw_ret = []
    for _ in range(100):
        s = env.reset(T=10)
        done = False
        ep_r = 0.0
        gamma_t = 1.0
        while not done:
            sa = int(rng.integers(0, 2))
            da = int(rng.integers(0, env.D_max))
            s, r, done = env.step(sa, da)
            ep_r += gamma_t * r
            gamma_t *= 0.99
        raw_ret.append(ep_r)
    log(f"  Mean return (random policy): {np.mean(raw_ret):.4f} ± {np.std(raw_ret):.4f}")

    # Trained policy at T=10
    ev10 = evaluate_at_T(env, policy, T=10)
    log(f"  Trained policy T=10 error : {ev10['error']:.6f}  "
        f"(Leibniz T=10: {ev10['leibniz_error']:.6f})")

    # Training curve monotonicity (rough check)
    log("\n── Trained policy greedy series ──")
    for T_eval in (10, 20, 50):
        ev = evaluate_at_T(env, policy, T=T_eval)
        terms_str = "  ".join(d["term_str"] for d in ev["term_details"][:10])
        p = ev["pattern"]
        log(f"  T={T_eval:>3d}: [{terms_str}{'…' if T_eval > 10 else ''}]")
        log(f"         error={ev['error']:.6f}  alt-sign={p['signs_alternate']}  "
            f"odd-denom={p['denoms_odd']}  increasing={p['denoms_increasing']}  "
            f"is_leibniz={p['is_leibniz']}")
    log("V-verification complete.\n")


# ── E — Evaluation ────────────────────────────────────────────────────────────
def run_evaluation(log, K_seeds: int = 10, eval_episodes: int = 100_000) -> list[dict]:
    log("=" * 70)
    log(f"E — EVALUATION  ({K_seeds} seeds × {eval_episodes:,} episodes)")
    log("=" * 70)

    env = PiSeriesEnvV2(D_max=30)
    all_results = []

    for seed in range(K_seeds):
        t0 = time.time()
        log(f"\n  Seed {seed}: training…")
        policy = PolicyNetworkV2(D_max=env.D_max)
        ep_rets, _ = train_v2(env, policy, episodes=eval_episodes,
                               seed=seed, verbose=False)

        seed_row: dict = {"seed": seed, "T_results": {}}
        for T_eval in (10, 20, 50):
            ev = evaluate_at_T(env, policy, T=T_eval)
            seed_row["T_results"][T_eval] = {
                "error": ev["error"],
                "pattern": ev["pattern"],
                "final_sum": ev["final_sum"],
                "better_than_leibniz": ev["better_than_leibniz"],
            }
        seed_row["best_return_last1k"] = float(max(ep_rets[-1000:]))
        seed_row["elapsed"] = round(time.time() - t0, 1)
        all_results.append(seed_row)

        p20 = seed_row["T_results"][20]["pattern"]
        log(f"  Seed {seed}: T=20 alt-sign={p20['signs_alternate']}  "
            f"odd-denom={p20['denoms_odd']}  is_leibniz={p20['is_leibniz']}  "
            f"error={seed_row['T_results'][20]['error']:.5f}  ({seed_row['elapsed']}s)")

    log("\n── Aggregate ──")
    for T_eval in (10, 20, 50):
        n_alt  = sum(r["T_results"][T_eval]["pattern"]["signs_alternate"] for r in all_results)
        n_odd  = sum(r["T_results"][T_eval]["pattern"]["denoms_odd"]       for r in all_results)
        n_leib = sum(r["T_results"][T_eval]["pattern"]["is_leibniz"]        for r in all_results)
        errors = [r["T_results"][T_eval]["error"] for r in all_results]
        leibniz_err = abs(LEIBNIZ_REFS[T_eval] - PI_OVER_4)
        n_better = sum(r["T_results"][T_eval]["better_than_leibniz"] for r in all_results)
        log(f"\n  T={T_eval}:")
        log(f"    Alt-sign         : {n_alt}/{K_seeds}")
        log(f"    Odd-denom        : {n_odd}/{K_seeds}")
        log(f"    Full Leibniz     : {n_leib}/{K_seeds}")
        log(f"    Better than Leib.: {n_better}/{K_seeds}  (Leibniz error={leibniz_err:.5f})")
        log(f"    Mean error       : {np.mean(errors):.5f} ± {np.std(errors):.5f}")

    log("\n── vs v1 baseline ──")
    log(f"  v1: 0/10 alt-sign, 0/10 odd-denom, mean error 0.036 at T=10")
    log(f"  v2 T=10: see above")
    log("E-evaluation complete.\n")
    return all_results


# ── Validation ────────────────────────────────────────────────────────────────
def run_validation(log, env: PiSeriesEnvV2, policy: PolicyNetworkV2) -> None:
    log("=" * 70)
    log("V — VALIDATION")
    log("=" * 70)

    log("\n── Generalisation test: T=100 (trained on T≤40) ──")
    ev100 = evaluate_at_T(env, policy, T=100)
    terms100 = [d["term_str"] for d in ev100["term_details"]]
    log(f"  Series (first 20 terms): {', '.join(terms100[:20])}…")
    p = ev100["pattern"]
    log(f"  Final sum   : {ev100['final_sum']:.8f}  (π/4 = {PI_OVER_4:.8f})")
    log(f"  Error       : {ev100['error']:.8f}")
    log(f"  Leibniz T=100: sum={LEIBNIZ_REFS[100]:.8f}  error={abs(LEIBNIZ_REFS[100]-PI_OVER_4):.8f}")
    log(f"  Alt-sign    : {p['signs_alternate']}")
    log(f"  Odd-denom   : {p['denoms_odd']}")
    log(f"  Increasing  : {p['denoms_increasing']}")
    log(f"  Is Leibniz  : {p['is_leibniz']}")
    if p["signs_alternate"]:
        log(f"  ✓ Signs continue to alternate at T=100 — agent learned a rule, not a sequence")
    else:
        log(f"  ✗ Signs do not alternate at T=100 — agent did not learn alternating pattern")

    # Per-T convergence comparison
    log(f"\n── Convergence comparison: agent vs Leibniz across T ──")
    log(f"{'T':>6}  {'Agent sum':>12}  {'Agent err':>10}  {'Leibniz err':>12}  {'Better?':>8}")
    log("─" * 56)
    for T_eval in (10, 20, 50, 100):
        ev = evaluate_at_T(env, policy, T=T_eval)
        le = abs(LEIBNIZ_REFS[T_eval] - PI_OVER_4)
        better = "YES" if ev["error"] < le else "no"
        log(f"{T_eval:>6}  {ev['final_sum']:>12.8f}  {ev['error']:>10.6f}  "
            f"{le:>12.6f}  {better:>8}")

    log("Validation complete.\n")


# ── Save JSON for visualization ───────────────────────────────────────────────
def save_training_data_v2(
    env: PiSeriesEnvV2,
    policy: PolicyNetworkV2,
    log_records: list[dict],
    seed_results: list[dict],
    output_path: Path,
) -> None:
    series_by_T = {}
    for T_eval in (10, 20, 50, 100):
        ev = evaluate_at_T(env, policy, T=T_eval)
        series_by_T[f"T{T_eval}"] = ev["term_details"]

    payload = {
        "config": {
            "D_max": env.D_max,
            "T_max": 40,
            "T_norm": env.T_NORM,
            "episodes": 100_000,
            "lr": 3e-4,
        },
        "curriculum_phases": [
            {"label": "Phase 1", "episode_start": 1,      "episode_end": 10_000, "T_lo": 3,  "T_hi": 10},
            {"label": "Phase 2", "episode_start": 10_001,  "episode_end": 50_000, "T_lo": 5,  "T_hi": 25},
            {"label": "Phase 3", "episode_start": 50_001,  "episode_end": 100_000,"T_lo": 10, "T_hi": 40},
        ],
        "training_curve": log_records,
        "series_by_T": series_by_T,
        "pattern_analysis": {
            f"T{T_eval}": evaluate_at_T(env, policy, T_eval)["pattern"]
            for T_eval in (10, 20, 50)
        },
        "seed_results": seed_results,
        "pi_over_4": PI_OVER_4,
        "leibniz_refs": {f"T{k}": v for k, v in LEIBNIZ_REFS.items()},
    }
    output_path.write_text(json.dumps(payload, indent=2))
    print(f"Saved → {output_path}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    lines: list[str] = []

    def log(s: str = "") -> None:
        print(s)
        lines.append(s)

    t_wall = time.time()
    log("RL-Leibniz v2 — TEVV Report")
    log("=" * 70)
    log(f"  π/4 = {PI_OVER_4:.12f}")
    log(f"  Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log()

    # ── T: Testing ────────────────────────────────────────────────────────────
    run_testing(log)

    # ── Main training run (seed=0, 100K episodes) ─────────────────────────────
    log("=" * 70)
    log("MAIN TRAINING  (D_max=30, 100K episodes, seed=0, curriculum)")
    log("=" * 70)
    env = PiSeriesEnvV2(D_max=30)
    policy = PolicyNetworkV2(D_max=env.D_max)
    ep_returns, log_records = train_v2(env, policy, episodes=100_000, seed=0)
    log(f"\nTraining complete. Final 500-ep mean: {np.mean(ep_returns[-500:]):+.4f}\n")

    # ── E: Evaluation ─────────────────────────────────────────────────────────
    seed_results = run_evaluation(log, K_seeds=3, eval_episodes=50_000)

    # ── V: Verification ───────────────────────────────────────────────────────
    run_verification(log, env, policy)

    # ── V: Validation ─────────────────────────────────────────────────────────
    run_validation(log, env, policy)

    elapsed = time.time() - t_wall
    log(f"Total wall time: {elapsed:.1f}s  ({elapsed/60:.1f} min)")

    # ── Save outputs ──────────────────────────────────────────────────────────
    (SCRIPT_DIR / "results_v2.txt").write_text("\n".join(lines) + "\n")
    print(f"\nSaved → {SCRIPT_DIR / 'results_v2.txt'}")

    csv_rows = [{"episode": i + 1, "return": r} for i, r in enumerate(ep_returns)]
    pd.DataFrame(csv_rows).to_csv(SCRIPT_DIR / "training_history_v2.csv", index=False)
    print(f"Saved → {SCRIPT_DIR / 'training_history_v2.csv'}")

    save_training_data_v2(
        env, policy, log_records, seed_results,
        SCRIPT_DIR / "training_data_v2.json",
    )

    models_dir = SCRIPT_DIR / "models"
    models_dir.mkdir(exist_ok=True)
    torch.save(policy.state_dict(), models_dir / "best_policy_v2.pt")
    print(f"Saved → {models_dir / 'best_policy_v2.pt'}")


if __name__ == "__main__":
    main()
