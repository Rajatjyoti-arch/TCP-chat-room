#!/bin/bash

REPO_DIR="/home/rajat/languages/python/TCP chat_room"
cd "$REPO_DIR" || exit

echo "Starting auto-push script for $REPO_DIR..."
echo "Logging to auto_push.log"

# Check if inotifywait is installed
if ! command -v inotifywait &> /dev/null; then
    echo "inotifywait is not installed. Please install it using: sudo apt-get install inotify-tools"
    echo "Falling back to 60-second polling..."
    USE_INOTIFY=false
else
    USE_INOTIFY=true
fi

while true; do
    if [ "$USE_INOTIFY" = true ]; then
        # Wait for file changes, ignoring the .git folder
        inotifywait -q -r -e modify,create,delete,move --exclude "\.git|auto_push.log|auto_push_output.log" "$REPO_DIR" > /dev/null 2>&1
        # Give a small buffer in case multiple files are saved at once
        sleep 2
    fi

    git add .
    
    # Check if there's anything to commit
    if ! git diff --quiet --cached; then
        # Get list of changed files, up to 5 files
        CHANGED_FILES=$(git diff --cached --name-only | head -n 5 | paste -sd ", " -)
        
        # Check if there are more than 5 files
        FILE_COUNT=$(git diff --cached --name-only | wc -l)
        if [ "$FILE_COUNT" -gt 5 ]; then
            CHANGED_FILES="$CHANGED_FILES, and $(($FILE_COUNT - 5)) more"
        fi
        
        # Select a human-sounding verb for the commit message
        VERBS=("Updated" "Modified" "Tweaked" "Refined" "Adjusted" "Worked on" "Improved" "Restructured")
        VERB=${VERBS[$RANDOM % ${#VERBS[@]}]}
        
        COMMIT_MSG="$VERB $CHANGED_FILES"
        
        git commit -m "$COMMIT_MSG"
        git push origin main
        
        echo "[$(date)] Pushed: $COMMIT_MSG" >> auto_push.log
    fi
    
    if [ "$USE_INOTIFY" = false ]; then
        # Wait 1 minute (60 seconds) before next check
        sleep 60
    fi
done
