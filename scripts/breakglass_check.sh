#!/bin/bash
# Usage: breakglass_check.sh "<prompt message>" "<stored_hash>"
prompt="$1"
stored_hash="$2"

read -p "$prompt" -s input_key
echo ""
input_hash=$(echo -n "$input_key" | sha256sum | awk '{print $1}')

if [[ "$input_hash" != "$stored_hash" ]]; then
    echo "Invalid BREAKGLASS key. Action rejected."
    exit 1
else
    echo "Breakglass override accepted."
fi