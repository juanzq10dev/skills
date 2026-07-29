#!/usr/bin/env bash
# Mechanical evidence checks for skill-review. Usage: evidence-checks.sh <path-to-skill-root>
# Prints one labeled section per check; references/evidence-checks.md explains how to read each.
set -uo pipefail

ROOT="${1:?Usage: evidence-checks.sh <path-to-skill-root>}"
ROOT="$(cd "$ROOT" 2>/dev/null && pwd)" || { echo "ERROR: $1 is not a directory" >&2; exit 1; }
[ -f "$ROOT/SKILL.md" ] || { echo "ERROR: no SKILL.md found in $1" >&2; exit 1; }

section() { printf '\n=== %s ===\n' "$1"; }

section "Setup — file inventory"
find "$ROOT" -type f | sort

section "C1 — front matter"
awk '/^---$/{n++; next} n==1' "$ROOT/SKILL.md"

section "C1 — name format"
NAME=$(awk '/^name:/{print $2; exit}' "$ROOT/SKILL.md")
echo "${#NAME} chars: $NAME"
echo "$NAME" | grep -Eq '^[a-z0-9-]{1,64}$' && echo "format OK" || echo "FORMAT VIOLATION"
echo "$NAME" | grep -Eiq 'anthropic|claude' && echo "RESERVED WORD" || echo "no reserved words"
[ "$NAME" = "$(basename "$ROOT")" ] && echo "matches dir" || echo "NAME/DIR MISMATCH"

section "C1 — description length (max 1024) and person"
awk '/^---$/{n++; next} n==1' "$ROOT/SKILL.md" |
  awk '/^description:/{f=1;print;next} f&&/^[[:space:]]/{print;next} f{exit}' | wc -c
grep -nEi '\b(I can|I will|you can use this|let me)\b' "$ROOT/SKILL.md" | head

section "C2 — placeholder examples"
grep -rnE '\b(foo|bar|baz|TODO|FIXME|your_[a-z]+_here|do the thing)\b' "$ROOT" | head -20

section "C2 — time-keyed instructions"
grep -rnEi '\b(as of|before [A-Z][a-z]+ 20[0-9]{2}|after [A-Z][a-z]+ 20[0-9]{2}|currently|at the time of writing)\b' "$ROOT" | head -20

section "C2 — terminology drift (edit the word list below for this skill's own vocabulary)"
for t in field box element column; do printf '%-10s %s\n' "$t" "$(grep -rowi "$t" "$ROOT" | wc -l)"; done

section "C3 — SKILL.md line count (500-line limit)"
wc -l "$ROOT/SKILL.md"

section "C3 — reference-to-reference chains"
grep -oE '\]\([^)]+\.md[^)]*\)' "$ROOT/SKILL.md" | sort -u
grep -rnoE '\]\([^)]+\.md[^)]*\)' "$ROOT/references" 2>/dev/null | grep -v '](http'

section "C3 — dead links"
grep -rn -oE '\]\([A-Za-z0-9_./#-]+\)' "$ROOT" --include='*.md' | while IFS= read -r hit; do
  file=${hit%%:*}; rest=${hit#*:}; link=${rest#*:}
  link=${link#](}; link=${link%)}
  case "$link" in http*|\#*) continue;; esac
  dir=$(dirname "$file")
  [ -e "$dir/${link%%#*}" ] || echo "DEAD: $link (in $file)"
done

section "C3 — orphaned reference files"
find "$ROOT" -type f -name '*.md' -not -name 'SKILL.md' 2>/dev/null | while read -r f; do
  grep -rqF "$(basename "$f")" "$ROOT" --include='*.md' --exclude="$(basename "$f")" || echo "ORPHAN: $f"
done

section "C3 — long reference files missing a table of contents (100-line threshold)"
find "$ROOT" -name '*.md' -not -name SKILL.md | while read -r f; do
  n=$(wc -l < "$f")
  [ "$n" -gt 100 ] && ! grep -qiE '^#+ (contents|table of contents)' "$f" && echo "NO TOC ($n lines): $f"
done

section "C3 — Windows-style paths"
grep -rnE '[A-Za-z0-9_-]+\\[A-Za-z0-9_-]+\.(md|py|sh|json)' "$ROOT" | head

section "C3 — non-descriptive filenames"
find "$ROOT" -type f | grep -E '/(doc|file|notes?|misc|temp|untitled)[0-9]*\.[a-z]+$'

section "C4 — numbered or checklist-driven procedures"
grep -rnE '^[[:space:]]*(Step [0-9]|[0-9]+\.|- \[ \])' "$ROOT" | head -20

section "C4 — option buffets with no stated default"
grep -rnEi '\b(or you can|alternatively|you could also|there are many)\b' "$ROOT" | head

section "C4 — validation loops"
grep -rnEi '\b(validate|verify|re-?run|if .* fails?|until it passes)\b' "$ROOT" | head -20

section "C5 — script files on disk (does not decide N/A by itself — see rubric.md)"
find "$ROOT" -type f \( -name '*.py' -o -name '*.sh' -o -name '*.js' -o -perm -u+x \) -not -name '*.md'

section "C5 — unjustified constants"
grep -rnE '^[A-Z_]+ *= *[0-9]+' "$ROOT" | grep -v '#' | head

section "C5 — bare open/subprocess calls with no visible error handling"
grep -rnE '\b(open\(|subprocess\.|requests\.(get|post)\()' "$ROOT" --include='*.py' | head -20

section "C5 — scripts never referenced from SKILL.md or references/"
find "$ROOT" \( -name '*.py' -o -name '*.sh' \) | while read -r s; do
  grep -rqF "$(basename "$s")" "$ROOT"/*.md "$ROOT"/references/*.md 2>/dev/null || echo "UNREFERENCED: $s"
done

section "C5 — MCP tools named without server prefix (inspect each hit)"
grep -rnE '\b(tool|use the) [a-z_]+_[a-z_]+\b' "$ROOT" | head

section "C6 — evaluation scenarios, expected behaviors, baselines"
grep -rniE '\b(evaluation|eval|expected_behavior|expected behaviou?r|baseline|test (case|scenario))\b' "$ROOT" | head -20
find "$ROOT" -iname '*eval*' -o -iname '*test*'

section "C6 — provenance for version- and source-dependent claims"
grep -rnE 'https?://|\bv?[0-9]+\.[0-9]+\.[0-9]+\b' "$ROOT" | head -20

exit 0
