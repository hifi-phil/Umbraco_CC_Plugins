#!/bin/bash
# Fetches starter kits from the Umbraco Marketplace and filters for v17 compatibility.
# Caches results for 24 hours to avoid slow repeated lookups.
#
# Usage: ./get-compatible-starter-kits.sh [umbraco-major-version]
# Default: 17
#
# Output: JSON array of compatible packages, e.g.:
#   [{"packageId":"Clean","title":"Clean Starter Kit for Umbraco","version":"7.0.5"}]

set -euo pipefail

TARGET_MAJOR="${1:-17}"
CACHE_DIR="${HOME}/.cache/umbraco-pr-tools"
CACHE_FILE="${CACHE_DIR}/starter-kits-v${TARGET_MAJOR}.json"
CACHE_MAX_AGE=86400  # 24 hours in seconds

mkdir -p "$CACHE_DIR"

# Return cache if fresh
if [ -f "$CACHE_FILE" ]; then
  if [ "$(uname)" = "Darwin" ]; then
    file_age=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE") ))
  else
    file_age=$(( $(date +%s) - $(stat -c %Y "$CACHE_FILE") ))
  fi
  if [ "$file_age" -lt "$CACHE_MAX_AGE" ]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

MARKETPLACE_API="https://api.marketplace.umbraco.com/api/v1"
STARTER_KIT_CATEGORY_ID="b239f1b7-31f6-4665-bf03-2ab985c64ac0"

# Fetch marketplace packages
marketplace_json=$(curl -sf "${MARKETPLACE_API}/packages?categoryId=${STARTER_KIT_CATEGORY_ID}&pageSize=10&orderBy=MostDownloads" 2>/dev/null || echo '{"results":[]}')

# Extract package IDs and titles
packages=$(echo "$marketplace_json" | jq -r '.results[] | "\(.packageId)\t\(.title)"')

results="[]"

while IFS=$'\t' read -r pkg_id title; do
  [ -z "$pkg_id" ] && continue

  # Skip themes
  if echo "$title" | grep -qi "theme"; then
    continue
  fi

  # Look up latest version on NuGet
  lower=$(echo "$pkg_id" | tr '[:upper:]' '[:lower:]')
  latest=$(curl -sf "https://api.nuget.org/v3-flatcontainer/${lower}/index.json" 2>/dev/null | jq -r '.versions[-1]' 2>/dev/null || echo "")
  [ -z "$latest" ] || [ "$latest" = "null" ] && continue

  # Fetch nuspec and extract Umbraco dependency version
  nuspec=$(curl -sf "https://api.nuget.org/v3-flatcontainer/${lower}/${latest}/${lower}.nuspec" 2>/dev/null || echo "")
  [ -z "$nuspec" ] && continue

  # Extract version from first Umbraco.Cms or Umbraco.Core dependency
  umbraco_ver=$(echo "$nuspec" | grep -i 'id="Umbraco\.C' | grep -i 'version=' | head -1 | sed 's/.*version="\([^"]*\)".*/\1/')
  [ -z "$umbraco_ver" ] && continue

  # Check compatibility: version must start with target major or be a range including it
  is_compatible=false

  # Exact version like "17.1.0"
  if echo "$umbraco_ver" | grep -qE "^${TARGET_MAJOR}\."; then
    is_compatible=true
  fi

  # Range like "[17.1.0, 18.0.0)"
  if echo "$umbraco_ver" | grep -qE "^\[${TARGET_MAJOR}\."; then
    is_compatible=true
  fi

  if [ "$is_compatible" = true ]; then
    results=$(echo "$results" | jq --arg id "$pkg_id" --arg t "$title" --arg v "$latest" \
      '. + [{"packageId": $id, "title": $t, "version": $v}]')
  fi
done <<< "$packages"

echo "$results" | jq '.' > "$CACHE_FILE"
cat "$CACHE_FILE"
