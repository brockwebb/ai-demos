#!/bin/bash

# Build script: assembles chapters into handout.md
# Usage: ./build.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHAPTERS_DIR="$SCRIPT_DIR/chapters"
OUTPUT="$SCRIPT_DIR/handout.md"

echo "Building handout from chapters..."

# Clear output file
> "$OUTPUT"

# Concatenate chapters in order (only .md files, not subdirectories)
for file in "$CHAPTERS_DIR"/*.md; do
    if [ -f "$file" ]; then
        echo "  Adding: $(basename "$file")"
        cat "$file" >> "$OUTPUT"
        echo -e "\n\n---\n" >> "$OUTPUT"
    fi
done

# Remove trailing separator
sed -i '' -e '$ { /^---$/d; }' "$OUTPUT" 2>/dev/null || true

echo ""
echo "Built: $OUTPUT"
echo "Word count: $(wc -w < "$OUTPUT" | tr -d ' ')"
