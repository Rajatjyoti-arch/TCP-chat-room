#!/bin/bash

REPO_DIR="/home/rajat/languages/python/TCP chat_room"
cd "$REPO_DIR" || exit

echo "Starting auto-push script for $REPO_DIR..."
echo "Logging to auto_push.log"

while true; do
    git add .
    
    # Check if there's anything to commit
    if ! git diff --quiet --cached; then
        # Get list of changed files
        CHANGED_FILES=$(git diff --cached --name-only | head -n 5 | paste -sd ", " -)
        FILE_COUNT=$(git diff --cached --name-only | wc -l)
        if [ "$FILE_COUNT" -gt 5 ]; then
            CHANGED_FILES="$CHANGED_FILES, and $(($FILE_COUNT - 5)) more"
        fi
        
        # Analyze the diff to generate a creative/meaningful message
        # Check if we changed Python files
        PY_CHANGES=$(git diff --cached --name-only | grep '\.py$')
        
        SUMMARY=""
        if [ -n "$PY_CHANGES" ]; then
            # Extract added functions/classes
            FUNCS=$(git diff --cached | grep -E '^\+ *(def |class )' | sed -E 's/^\+ *(def |class )//g' | cut -d '(' -f 1 | cut -d ':' -f 1 | tr '\n' ',' | sed 's/,$//' | sed 's/,/, /g')
            if [ -n "$FUNCS" ]; then
                SUMMARY="Added/Modified structures: $FUNCS"
            fi
            
            # Check for specific patterns
            if git diff --cached | grep -q -i -E 'kick|ban'; then
                SUMMARY="${SUMMARY:+$SUMMARY; }Updated admin/moderation logic (kick/ban)"
            fi
            if git diff --cached | grep -q -i -E 'socket|connect|send|recv'; then
                SUMMARY="${SUMMARY:+$SUMMARY; }Updated socket communication details"
            fi
        fi
        
        # Check if README.md changed
        if git diff --cached --name-only | grep -q 'README.md'; then
            # Extract any new markdown headers
            HEADERS=$(git diff --cached README.md | grep -E '^\+ *#+ ' | sed -E 's/^\+ *#+ //g' | tr '\n' ';' | sed 's/;$/ /' | sed 's/;/; /g')
            if [ -n "$HEADERS" ]; then
                SUMMARY="${SUMMARY:+$SUMMARY; }Updated documentation sections: $HEADERS"
            else
                SUMMARY="${SUMMARY:+$SUMMARY; }Refined README documentation"
            fi
        fi
        
        # Choose a creative prefix based on the type of change
        VERB="Update"
        if git diff --cached | grep -q -E '^[+][[:space:]]*#'; then
            VERB="Document"
        elif git diff --cached | grep -q -E 'import '; then
            VERB="Integrate"
        elif git diff --cached --name-status | grep -q '^A'; then
            VERB="Introduce"
        elif git diff --cached | grep -q -E 'def |class '; then
            VERB="Implement"
        else
            VERBS=("Polish" "Refine" "Tweak" "Enhance" "Improve" "Adjust")
            VERB=${VERBS[$RANDOM % ${#VERBS[@]}]}
        fi
        
        # Assemble message
        if [ -n "$SUMMARY" ]; then
            COMMIT_MSG="$VERB: $SUMMARY"
        else
            COMMIT_MSG="$VERB $CHANGED_FILES"
        fi
        
        # Trim message length if too long
        COMMIT_MSG=$(echo "$COMMIT_MSG" | cut -c 1-100)
        
        git commit -m "$COMMIT_MSG"
        git push origin main
        
        echo "[$(date)] Pushed: $COMMIT_MSG" >> auto_push.log
    fi
    
    # Sleep for 10 minutes (600 seconds)
    sleep 600
done
