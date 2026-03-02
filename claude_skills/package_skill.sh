#!/bin/bash
# Package paperbanana-diagram skill and copy to ai-demos
cd /Users/brock/Documents/GitHub/census-mcp-server/paper/assets/diagrams/paperbanana
zip -r /Users/brock/Documents/GitHub/ai-demos/claude_skills/paperbanana-diagram.skill skill/ -x "*.DS_Store"
echo "Done: /Users/brock/Documents/GitHub/ai-demos/claude_skills/paperbanana-diagram.skill"
