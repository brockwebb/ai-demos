#!/bin/bash
# Creates v3 variants from v2 source files
# Run from: leibniz-pi/
set -e

echo "=== Creating GP v3 variants ==="

# GP Wide: k + integers -20..20
cp gp-leibniz-v2/gp_leibniz_v2.py gp-leibniz-v3/gp_leibniz_v3_wide.py
cd gp-leibniz-v3
sed -i '' 's/TERM_FIXED = \["k", 1, 2, -1\]/TERM_FIXED = ["k", 1]/' gp_leibniz_v3_wide.py
sed -i '' 's/EPHEMERALS = list(range(-5, 6))/EPHEMERALS = list(range(-20, 21))/' gp_leibniz_v3_wide.py
sed -i '' 's/evolution_data_v2/evolution_data_v3/g' gp_leibniz_v3_wide.py
sed -i '' 's/convergence_v2/convergence_v3/g' gp_leibniz_v3_wide.py
sed -i '' 's/results_v2/results_v3/g' gp_leibniz_v3_wide.py

# GP Hostile: k, 1, 3, -1 (NO 2 anywhere) + integers -20..20 minus 2
cp gp_leibniz_v3_wide.py gp_leibniz_v3_hostile.py
sed -i '' 's/TERM_FIXED = \["k", 1\]/TERM_FIXED = ["k", 1, 3, -1]/' gp_leibniz_v3_hostile.py
sed -i '' 's/EPHEMERALS = list(range(-20, 21))/EPHEMERALS = [x for x in range(-20, 21) if x != 2]/' gp_leibniz_v3_hostile.py

echo "  gp_leibniz_v3_wide.py created"
echo "  gp_leibniz_v3_hostile.py created"
cd ..

echo "=== Creating Entropy v3 variants ==="

# Entropy Wide
cp entropy-leibniz/entropy_leibniz.py entropy-leibniz-v3/entropy_leibniz_v3_wide.py
cd entropy-leibniz-v3
sed -i '' 's/TERM_FIXED = \["k", 1, 2, -1\]/TERM_FIXED = ["k", 1]/' entropy_leibniz_v3_wide.py
sed -i '' 's/EPHEMERALS = list(range(-5, 6))/EPHEMERALS = list(range(-20, 21))/' entropy_leibniz_v3_wide.py

# Entropy Hostile
cp entropy_leibniz_v3_wide.py entropy_leibniz_v3_hostile.py
sed -i '' 's/TERM_FIXED = \["k", 1\]/TERM_FIXED = ["k", 1, 3, -1]/' entropy_leibniz_v3_hostile.py
sed -i '' 's/EPHEMERALS = list(range(-20, 21))/EPHEMERALS = [x for x in range(-20, 21) if x != 2]/' entropy_leibniz_v3_hostile.py

echo "  entropy_leibniz_v3_wide.py created"
echo "  entropy_leibniz_v3_hostile.py created"
cd ..

echo ""
echo "=== Verification ==="
echo "GP Wide:"
grep 'TERM_FIXED\|EPHEMERALS' gp-leibniz-v3/gp_leibniz_v3_wide.py | head -2
echo "GP Hostile:"
grep 'TERM_FIXED\|EPHEMERALS' gp-leibniz-v3/gp_leibniz_v3_hostile.py | head -2
echo "Entropy Wide:"
grep 'TERM_FIXED\|EPHEMERALS' entropy-leibniz-v3/entropy_leibniz_v3_wide.py | head -2
echo "Entropy Hostile:"
grep 'TERM_FIXED\|EPHEMERALS' entropy-leibniz-v3/entropy_leibniz_v3_hostile.py | head -2

echo ""
echo "=== Run commands ==="
echo "cd gp-leibniz-v3 && python3 gp_leibniz_v3_wide.py"
echo "cd gp-leibniz-v3 && python3 gp_leibniz_v3_hostile.py"
echo "cd entropy-leibniz-v3 && python3 entropy_leibniz_v3_wide.py"
echo "cd entropy-leibniz-v3 && python3 entropy_leibniz_v3_hostile.py"
echo ""
echo "Each takes ~5 min (5 seeds x 55s). Run in parallel if you want."
