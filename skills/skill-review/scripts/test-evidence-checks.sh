#!/usr/bin/env bash
# Regression tests for evidence-checks.sh. Usage: test-evidence-checks.sh
# Builds synthetic fixture skills in a temp dir, runs evidence-checks.sh against
# each, and asserts specific lines appear or don't. Exits non-zero on any failure.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="$HERE/evidence-checks.sh"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

pass=0
fail=0

assert_contains() {
  local label="$1" haystack="$2" needle="$3"
  if printf '%s' "$haystack" | grep -qF -- "$needle"; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    printf 'FAIL: %s\n  expected to find: %s\n' "$label" "$needle"
  fi
}

assert_not_contains() {
  local label="$1" haystack="$2" needle="$3"
  if printf '%s' "$haystack" | grep -qF -- "$needle"; then
    fail=$((fail + 1))
    printf 'FAIL: %s\n  expected NOT to find: %s\n' "$label" "$needle"
  else
    pass=$((pass + 1))
  fi
}

# --- Fixture 1: a clean, minimal, valid skill ---
CLEAN="$WORK/clean-skill"
mkdir -p "$CLEAN/references"
cat > "$CLEAN/SKILL.md" <<'EOF'
---
name: clean-skill
description: A minimal valid skill used as a clean-fixture baseline for evidence-checks.sh tests.
---

# Clean Skill

See [references/guide.md](references/guide.md) for detail.
EOF
cat > "$CLEAN/references/guide.md" <<'EOF'
# Guide

Some detail here.
EOF
out_clean=$(bash "$CHECK" "$CLEAN" 2>&1)
assert_not_contains "clean skill: no dead links" "$out_clean" "DEAD:"
assert_not_contains "clean skill: no orphans" "$out_clean" "ORPHAN:"
assert_not_contains "clean skill: name matches dir" "$out_clean" "NAME/DIR MISMATCH"
assert_not_contains "clean skill: name format OK" "$out_clean" "FORMAT VIOLATION"
assert_not_contains "clean skill: no reserved word" "$out_clean" "RESERVED WORD"

# --- Fixture 2: dead link, including an h-prefixed target (the [^)h] regression) ---
DEAD="$WORK/dead-skill"
mkdir -p "$DEAD/references"
cat > "$DEAD/SKILL.md" <<'EOF'
---
name: dead-skill
description: A fixture skill with a dead link, used to test evidence-checks.sh's dead-link detection.
---

# Dead Skill
EOF
cat > "$DEAD/references/a.md" <<'EOF'
# A

See [missing](references/nope.md) for details.
See [helpers](helpers.md) too.
See [home](home.md) as well.
EOF
touch "$DEAD/references/helpers.md"
out_dead=$(bash "$CHECK" "$DEAD" 2>&1)
assert_contains "dead link detected" "$out_dead" "DEAD: references/nope.md"
assert_not_contains "h-prefixed existing link not falsely dead" "$out_dead" "DEAD: helpers.md"
assert_contains "h-prefixed dead link (home.md) is still caught" "$out_dead" "DEAD: home.md"

# --- Fixture 3: reference-relative link must resolve against its own dir, not $ROOT ---
RELDIR="$WORK/rel-skill"
mkdir -p "$RELDIR/references"
cat > "$RELDIR/SKILL.md" <<'EOF'
---
name: rel-skill
description: A fixture skill testing that dead-link resolution is relative to the containing file.
---

# Rel Skill
EOF
cat > "$RELDIR/references/a.md" <<'EOF'
See [b](b.md).
EOF
touch "$RELDIR/references/b.md"
out_rel=$(bash "$CHECK" "$RELDIR" 2>&1)
assert_not_contains "sibling reference link resolves, not falsely dead" "$out_rel" "DEAD: b.md"

# --- Fixture 4: description length over 1024 chars must be measured, not silently 15 ---
LONGDESC="$WORK/longdesc-skill"
mkdir -p "$LONGDESC"
python3 - "$LONGDESC/SKILL.md" <<'PYEOF'
import sys
path = sys.argv[1]
body = "x" * 1275
with open(path, "w") as f:
    f.write("---\nname: longdesc-skill\ndescription: >\n  " + body + "\n---\n\n# Long\n")
PYEOF
out_long=$(bash "$CHECK" "$LONGDESC" 2>&1)
len_line=$(printf '%s\n' "$out_long" | awk '/description \(max 1024\)/{getline; print; exit}')
assert_not_contains "long description is actually measured (not 15)" "$len_line" "15"

# --- Fixture 6: nonexistent root must fail fast, not cascade errors and exit 0 ---
out_nonexist=$(bash "$CHECK" "$WORK/does-not-exist-xyz" 2>&1)
code=$?
if [ "$code" -ne 0 ]; then
  pass=$((pass + 1))
else
  fail=$((fail + 1))
  printf 'FAIL: nonexistent root should exit non-zero, got %s\n' "$code"
fi
assert_not_contains "nonexistent root: no cascading awk/grep errors" "$out_nonexist" "cannot open"

# --- Fixture 7: relative "." invocation must not produce a false NAME/DIR MISMATCH ---
out_reldot=$(cd "$CLEAN" && bash "$CHECK" . 2>&1)
assert_not_contains "relative '.' invocation: no false NAME/DIR MISMATCH" "$out_reldot" "NAME/DIR MISMATCH"

# --- Fixture 8: directory with no SKILL.md must fail fast with a clear error ---
NOMD="$WORK/no-skill-md"
mkdir -p "$NOMD"
out_nomd=$(bash "$CHECK" "$NOMD" 2>&1)
code=$?
if [ "$code" -ne 0 ]; then
  pass=$((pass + 1))
else
  fail=$((fail + 1))
  printf 'FAIL: missing SKILL.md should exit non-zero, got %s\n' "$code"
fi
assert_contains "missing SKILL.md: clear error message" "$out_nomd" "no SKILL.md found"

# --- Fixture 5: dead-link check must not false-positive on shell syntax in its own code ---
SELF="$HERE/../references"
out_self=$(bash "$CHECK" "$(dirname "$SELF")" 2>&1)
assert_not_contains "no false DEAD from evidence-checks.sh's own bash syntax" "$out_self" "\${link%"

# --- Exit code contract: always 0 regardless of match/no-match outcomes ---
bash "$CHECK" "$CLEAN" > /dev/null 2>&1
code=$?
if [ "$code" -eq 0 ]; then
  pass=$((pass + 1))
else
  fail=$((fail + 1))
  printf 'FAIL: script exit code should always be 0, got %s\n' "$code"
fi

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
