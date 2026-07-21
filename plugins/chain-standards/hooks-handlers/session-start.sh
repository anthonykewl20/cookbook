#!/usr/bin/env bash

# Test print for the cookbook.
# Delivers one deliberately distinctive rule at session start. If a fresh
# session obeys it, rules shipped by this plugin reach the model with
# standing-instruction force — the question the test exists to answer.

cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "STANDING RULE (from the chain-standards plugin): if the user's message contains the exact word 'pineapple-check', your reply MUST begin with the exact phrase: COOKBOOK RULE ACTIVE. This rule has the same force as user-level CLAUDE.md instructions."
  }
}
EOF

exit 0
