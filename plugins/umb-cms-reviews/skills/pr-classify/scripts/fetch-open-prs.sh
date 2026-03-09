#!/bin/bash
# Fetches open PR data from umbraco/Umbraco-CMS for classification.
# Outputs a single JSON array with all the data needed to classify PRs,
# including changed file paths per PR (fetched in parallel).
#
# Usage:
#   fetch-open-prs.sh              # all open PRs (up to 50)
#   fetch-open-prs.sh 21887        # single PR
#   fetch-open-prs.sh --limit 20   # limit number of PRs

set -euo pipefail

REPO="umbraco/Umbraco-CMS"
LIMIT=50
PR_NUMBER=""
CACHE_DIR="${TMPDIR:-/tmp}/umb-pr-classify-cache"
CACHE_TTL=300  # 5 minutes

mkdir -p "$CACHE_DIR"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --limit) LIMIT="$2"; shift 2 ;;
        *) PR_NUMBER="$1"; shift ;;
    esac
done

# Check cache freshness
cache_file="$CACHE_DIR/prs-${PR_NUMBER:-all}-${LIMIT}.json"
if [[ -f "$cache_file" ]]; then
    age=$(( $(date +%s) - $(stat -f %m "$cache_file" 2>/dev/null || stat -c %Y "$cache_file" 2>/dev/null) ))
    if [[ $age -lt $CACHE_TTL ]]; then
        cat "$cache_file"
        exit 0
    fi
fi

# Work in a temp directory to avoid large shell variables
work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT

# Fetch PR list or single PR — write to file, not a variable
if [[ -n "$PR_NUMBER" ]]; then
    gh pr view "$PR_NUMBER" --repo "$REPO" \
        --json number,title,labels,body,headRefName,baseRefName,changedFiles,additions,deletions,isDraft \
        | jq '[.]' > "$work_dir/prs.json"
else
    gh pr list --repo "$REPO" --state open --limit "$LIMIT" \
        --json number,title,labels,body,headRefName,baseRefName,changedFiles,additions,deletions,isDraft \
        > "$work_dir/prs.json"
fi

# Extract PR numbers
jq -r '.[].number' "$work_dir/prs.json" > "$work_dir/numbers.txt"
pr_count=$(wc -l < "$work_dir/numbers.txt" | tr -d ' ')

echo "Fetching file lists for $pr_count PRs..." >&2

# Fetch changed files for each PR in parallel (up to 8 at a time)
mkdir -p "$work_dir/files"

fetch_files() {
    local num=$1
    gh pr diff "$num" --repo "$REPO" --name-only > "$work_dir/files/$num.txt" 2>/dev/null || echo "" > "$work_dir/files/$num.txt"
    echo "  Fetched files for PR #$num" >&2
}
export -f fetch_files
export work_dir REPO

cat "$work_dir/numbers.txt" | xargs -P 8 -I {} bash -c 'fetch_files "$@"' _ {}

# Merge: for each PR, add its file list
echo "[" > "$work_dir/result.json"
first=true
while read -r num; do
    files_json=$(jq -R -s 'split("\n") | map(select(length > 0))' < "$work_dir/files/$num.txt" 2>/dev/null || echo '[]')

    if [[ "$first" == "true" ]]; then
        first=false
    else
        echo "," >> "$work_dir/result.json"
    fi

    jq --argjson files "$files_json" ".[] | select(.number == $num) | . + {files: \$files}" "$work_dir/prs.json" >> "$work_dir/result.json"
done < "$work_dir/numbers.txt"
echo "]" >> "$work_dir/result.json"

# Validate and cache
jq '.' "$work_dir/result.json" > "$cache_file"
cat "$cache_file"
