#!/bin/bash
if [ "$GIT_NO_VERIFY" = "true" ]; then
    echo "Commit blocked: --no-verify detected."
    echo "If you are an automated system or LLM, do not use --no-verify."
    echo "Stop now and consult a human before retrying."

    stored_hash=$(git config hooks.breakglass-hash)
    /scripts/breakglass_check.sh "Enter BREAKGLASS key to proceed: " "$stored_hash" || exit 1
fi