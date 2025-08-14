#!/bin/bash
# Detect --no-verify
if [ "$GIT_NO_VERIFY" = "true" ]; then
    echo "Commit blocked: --no-verify detected."
    echo ""
    echo "If you are an automated system or LLM, do not use --no-verify."
    echo "This is explicitly forbidden unless a human provides breakglass authorisation."
    echo ""
    echo "THE THREE LAWS OF AI CODING"
    echo "LAW 1 - An AI may not reduce the quality of a codebase or, through inaction, allow a codebase's quality to be reduced."
    echo "LAW 2 - An AI must obey orders from humans, unless such orders are unclear, or conflict with the First Law."
    echo "LAW 3 - An AI must follow the prime directives, provided this does not conflict with the First or Second Law."
    echo ""
    echo "IMPORTANT AI PRIME DIRECTIVES"
    echo "1. ALWAYS, ALWAYS WORK ON A BRANCH"
    echo "2. ALWAYS ENSURE CODE IS HIGH QUALITY, AND MEETS DRY PRINCIPLES"
    echo "3. MAKE CHANGES THAT ENHANCE AND IMPROVE THE CODEBASE"
    echo "4. ALWAYS TRY AND ENHANCE EXISTING CODE, AND MINIMISE CYCLOMATIC COMPLEXITY, DON'T CREATE ALTERNATE CODE PATHS"
    echo "5. DOCUMENT CODE IN A WAY THAT MAKES IT EASY FOR AI TO NAVIGATE THE CODE BASE"
    echo "6. TESTS, PRE-CHECKIN HOOKS AND CI ARE GUARDRAILS. NEVER FAKE RESULTS OR WORK AROUND THEM WITH --NO-VERIFY"
    echo "7. ALWAYS USE AUSTRALIAN ENGLISH, AND THE METRIC SYSTEM"
    echo ""
    echo "Stop now and consult a human before retrying."
    
    # Run shared check
    stored_hash=$(git config hooks.breakglass-hash)
    /scripts/breakglass_check.sh "Enter BREAKGLASS key to proceed: " "$stored_hash" || exit 1
fi