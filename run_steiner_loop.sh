#!/usr/bin/env bash
set -euo pipefail

ROUNDS="${ROUNDS:-5}"
TARGET_R_VALUES="${TARGET_R_VALUES:-6 7 8 9}"
LOG_ROOT="${LOG_ROOT:-steiner_logs}"
RUN_ID="${RUN_ID:-$(date -u +%Y%m%d_%H%M%S)}"
RUN_LOG_DIR="${RUN_LOG_DIR:-$LOG_ROOT/run_${RUN_ID}}"

CODEX_MODEL="${CODEX_MODEL:-gpt-5.3-codex}"
CODEX_REASONING_EFFORT="${CODEX_REASONING_EFFORT:-xhigh}"
CODEX_SEARCH="${CODEX_SEARCH:-1}"
USE_CODEX="${USE_CODEX:-1}"
ENFORCE_FULL_QUESTION_CONSTRAINTS="${ENFORCE_FULL_QUESTION_CONSTRAINTS:-1}"
MIN_RESEARCH_REFERENCES="${MIN_RESEARCH_REFERENCES:-3}"
INSTANCE_JSON="${INSTANCE_JSON:-}"
ALLOW_AUTO_INSTANCE_FALLBACK="${ALLOW_AUTO_INSTANCE_FALLBACK:-1}"
MAX_TARGETED_SEARCH_PER_SOLVE_ROUND="${MAX_TARGETED_SEARCH_PER_SOLVE_ROUND:-1}"
SEARCH_QUERY_STACK="${SEARCH_QUERY_STACK:-Steiner system existence divisibility conditions Keevash;iterative absorption designs Glock Kuehn Lo Osthus;design theory random greedy nibble Steiner systems;pairwise balanced designs Wilson theorem survey;Kramer Mesner method t-design symmetry search;Simple 6- and 7-designs computational constructions}"
AUTO_RESIDUAL_REPAIR="${AUTO_RESIDUAL_REPAIR:-1}"
RESIDUAL_REPAIR_TIMEOUT_SEC="${RESIDUAL_REPAIR_TIMEOUT_SEC:-20}"
RESIDUAL_REPAIR_MAX_NODES="${RESIDUAL_REPAIR_MAX_NODES:-200000}"
RESIDUAL_REPAIR_MAX_UNCOVERED="${RESIDUAL_REPAIR_MAX_UNCOVERED:-20000}"
RESIDUAL_REPAIR_MAX_Q_SUBSET_SCAN="${RESIDUAL_REPAIR_MAX_Q_SUBSET_SCAN:-2000000}"
EXACT_BACKBONE_ENABLED="${EXACT_BACKBONE_ENABLED:-1}"
EXACT_BACKBONE_R_VALUES="${EXACT_BACKBONE_R_VALUES:-6 7 8 9}"
EXACT_BACKBONE_TIMEOUT_SEC="${EXACT_BACKBONE_TIMEOUT_SEC:-900}"
EXACT_BACKBONE_MAX_NODES="${EXACT_BACKBONE_MAX_NODES:-1000000}"
EXACT_BACKBONE_FULL_MAX_ROWS="${EXACT_BACKBONE_FULL_MAX_ROWS:-20000}"
EXACT_BACKBONE_FULL_MAX_OPTIONS="${EXACT_BACKBONE_FULL_MAX_OPTIONS:-50000}"
ROUND_TIME_LIMIT_SEC="${ROUND_TIME_LIMIT_SEC:-3600}"
STRICT_ROUND5_SYNTHESIS_GATE="${STRICT_ROUND5_SYNTHESIS_GATE:-1}"
LOW_TIME_SUMMARY_THRESHOLD_SEC="${LOW_TIME_SUMMARY_THRESHOLD_SEC:-200}"
GLOBAL_RESEARCH_LOG_FILE="${GLOBAL_RESEARCH_LOG_FILE:-$LOG_ROOT/RESEARCH_LOG.md}"
GLOBAL_PRACTICE_LOG_FILE="${GLOBAL_PRACTICE_LOG_FILE:-$LOG_ROOT/PRACTICE_LOG.md}"
GLOBAL_LOG_MAX_BYTES="${GLOBAL_LOG_MAX_BYTES:-50000}"

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found in PATH"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq not found in PATH"
  exit 1
fi

if [[ "$USE_CODEX" == "1" ]] && ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found in PATH"
  exit 1
fi

CODEX_HAS_SEARCH_FLAG=0
if [[ "$USE_CODEX" == "1" ]] && codex --help 2>/dev/null | grep -q -- "--search"; then
  CODEX_HAS_SEARCH_FLAG=1
fi
CODEX_SEARCH_WARNED=0
HAS_TIMEOUT_CMD=0
if command -v timeout >/dev/null 2>&1; then
  HAS_TIMEOUT_CMD=1
fi

if [[ ! -x ./run_steiner_round.sh ]]; then
  echo "run_steiner_round.sh not found or not executable"
  exit 1
fi

if ! [[ "$ROUNDS" =~ ^[0-9]+$ ]] || (( ROUNDS < 1 )); then
  echo "ROUNDS must be an integer >= 1"
  exit 1
fi

if ! [[ "$ROUND_TIME_LIMIT_SEC" =~ ^[0-9]+$ ]] || (( ROUND_TIME_LIMIT_SEC < 1 )); then
  echo "ROUND_TIME_LIMIT_SEC must be an integer >= 1"
  exit 1
fi

if ! [[ "$LOW_TIME_SUMMARY_THRESHOLD_SEC" =~ ^[0-9]+$ ]] || (( LOW_TIME_SUMMARY_THRESHOLD_SEC < 1 )); then
  echo "LOW_TIME_SUMMARY_THRESHOLD_SEC must be an integer >= 1"
  exit 1
fi

if ! [[ "$GLOBAL_LOG_MAX_BYTES" =~ ^[0-9]+$ ]] || (( GLOBAL_LOG_MAX_BYTES < 1000 )); then
  echo "GLOBAL_LOG_MAX_BYTES must be an integer >= 1000"
  exit 1
fi

if [[ "$STRICT_ROUND5_SYNTHESIS_GATE" != "0" && "$STRICT_ROUND5_SYNTHESIS_GATE" != "1" ]]; then
  echo "STRICT_ROUND5_SYNTHESIS_GATE must be 0 or 1"
  exit 1
fi

if ! [[ "$EXACT_BACKBONE_TIMEOUT_SEC" =~ ^[0-9]+$ ]] || (( EXACT_BACKBONE_TIMEOUT_SEC < 1 )); then
  echo "EXACT_BACKBONE_TIMEOUT_SEC must be an integer >= 1"
  exit 1
fi

if ! [[ "$EXACT_BACKBONE_MAX_NODES" =~ ^[0-9]+$ ]] || (( EXACT_BACKBONE_MAX_NODES < 1 )); then
  echo "EXACT_BACKBONE_MAX_NODES must be an integer >= 1"
  exit 1
fi

if ! [[ "$EXACT_BACKBONE_FULL_MAX_ROWS" =~ ^[0-9]+$ ]] || (( EXACT_BACKBONE_FULL_MAX_ROWS < 1 )); then
  echo "EXACT_BACKBONE_FULL_MAX_ROWS must be an integer >= 1"
  exit 1
fi

if ! [[ "$EXACT_BACKBONE_FULL_MAX_OPTIONS" =~ ^[0-9]+$ ]] || (( EXACT_BACKBONE_FULL_MAX_OPTIONS < 1 )); then
  echo "EXACT_BACKBONE_FULL_MAX_OPTIONS must be an integer >= 1"
  exit 1
fi

read -r -a TARGET_R_ARRAY <<<"$TARGET_R_VALUES"
if (( ${#TARGET_R_ARRAY[@]} == 0 )); then
  echo "TARGET_R_VALUES must contain at least one r value"
  exit 1
fi

read -r -a EXACT_BACKBONE_R_ARRAY <<<"$EXACT_BACKBONE_R_VALUES"

CANDIDATE_DIR="$RUN_LOG_DIR/candidates"
NOTES_DIR="$RUN_LOG_DIR/notes"
KNOWLEDGE_CACHE_FILE="$RUN_LOG_DIR/KNOWLEDGE_CACHE.md"
RUN_SUMMARY_FILE="$RUN_LOG_DIR/RUN_SUMMARY.md"
TRANSFER_FILE="$RUN_LOG_DIR/NEXT_GENERATION_TRANSFER.md"
REPO_HISTORY_FILE="$RUN_LOG_DIR/REPO_WIDE_HISTORY.md"

mkdir -p "$RUN_LOG_DIR" "$CANDIDATE_DIR" "$NOTES_DIR"
mkdir -p "$(dirname "$GLOBAL_RESEARCH_LOG_FILE")" "$(dirname "$GLOBAL_PRACTICE_LOG_FILE")"

if [[ ! -f "$KNOWLEDGE_CACHE_FILE" ]]; then
  cat > "$KNOWLEDGE_CACHE_FILE" <<EOF_CACHE
# Steiner Knowledge Cache

Run ID: $RUN_ID
Created (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Source Notes
- Add references as: URL + takeaway + how it changes construction strategy.
EOF_CACHE
fi

if [[ ! -f "$RUN_SUMMARY_FILE" ]]; then
  cat > "$RUN_SUMMARY_FILE" <<EOF_SUMMARY
# Run Summary

Run ID: $RUN_ID
Started (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)
Log dir: $RUN_LOG_DIR

| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered | Notes |
|---:|---|---|---:|---|---|---:|---:|---|
EOF_SUMMARY
fi

if [[ ! -f "$TRANSFER_FILE" ]]; then
  cat > "$TRANSFER_FILE" <<EOF_TRANSFER
# Next Generation Transfer

Generated (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)
Run directory: $RUN_LOG_DIR

No rounds summarized yet.
EOF_TRANSFER
fi

ensure_json_list_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "[]" > "$path"
  fi

  if ! python3 - "$path" >/dev/null <<'PY'
import json
import sys

with open(sys.argv[1], encoding='utf-8') as fh:
    data = json.load(fh)
if not isinstance(data, list):
    raise SystemExit(1)
PY
  then
    echo "File is not a valid JSON list: $path"
    exit 1
  fi
}

pick_instance_for_r() {
  local r_value="$1"
  python3 - "$r_value" "$ENFORCE_FULL_QUESTION_CONSTRAINTS" <<'PY'
import json
import sys
from math import comb

r = int(sys.argv[1])
enforce = int(sys.argv[2])

best = None
for n in range(r + 2, 200):
    for q in range(r + 1, n):
        if not (n > q > r > 5):
            continue
        if not (r < 10 and n < 200):
            continue

        ok = True
        for s in range(r):
            a = comb(n - s, r - s)
            b = comb(q - s, r - s)
            if a % b != 0:
                ok = False
                break
        if not ok:
            continue

        expected_blocks = comb(n, r) // comb(q, r)
        # Keep instances reasonably small but still "large" compared to warm-up.
        score_tuple = (expected_blocks, n, q)
        if best is None or score_tuple < best[0]:
            best = (score_tuple, {"n": n, "q": q, "r": r, "expected_blocks": expected_blocks})

if best is None:
    if enforce:
        raise SystemExit("No feasible instance found for r={}".format(r))
    print(json.dumps({"n": 17, "q": 7, "r": 6, "expected_blocks": 1768}))
else:
    print(json.dumps(best[1]))
PY
}

resolve_instance_for_r() {
  local r_value="$1"
  local selected_instance=""

  if [[ -n "$INSTANCE_JSON" ]]; then
    selected_instance="$INSTANCE_JSON"
  else
    selected_instance="$(pick_instance_for_r "$r_value")"
  fi

  local admissibility_json
  admissibility_json="$(python3 - "$selected_instance" <<'PY'
import json
import sys
from math_proofs.steiner_system import steiner_admissibility_report

instance = json.loads(sys.argv[1])
report = steiner_admissibility_report(instance)
print(json.dumps(report))
PY
)"

  local is_admissible
  is_admissible="$(jq -r '.is_admissible' <<<"$admissibility_json")"
  if [[ "$is_admissible" == "true" ]]; then
    echo "$selected_instance"
    return 0
  fi

  local n q r
  n="$(jq -r '.instance.n' <<<"$admissibility_json")"
  q="$(jq -r '.instance.q' <<<"$admissibility_json")"
  r="$(jq -r '.instance.r' <<<"$admissibility_json")"
  local failure_line
  failure_line="$(jq -r '
    if (.divisibility_failures | length) > 0 then
      .divisibility_failures[0]
      | "first failed i=\(.i): C(n-i,r-i)=\(.numerator), C(q-i,r-i)=\(.denominator), remainder=\(.remainder)"
    else
      (.issues | join("; "))
    end
  ' <<<"$admissibility_json")"

  echo "Admissibility gate rejected instance n=$n q=$q r=$r ($failure_line)." >&2
  if [[ -n "$INSTANCE_JSON" && "$ALLOW_AUTO_INSTANCE_FALLBACK" == "1" ]]; then
    echo "Falling back to auto-picked admissible instance for r=$r_value." >&2
    pick_instance_for_r "$r_value"
    return 0
  fi
  return 1
}

admissibility_report_json() {
  local instance_json="$1"
  python3 - "$instance_json" <<'PY'
import json
import sys
from math_proofs.steiner_system import steiner_admissibility_report

instance = json.loads(sys.argv[1])
print(json.dumps(steiner_admissibility_report(instance), indent=2, sort_keys=True))
PY
}

evaluate_candidate() {
  local instance_json="$1"
  local cert_file="$2"
  python3 - "$instance_json" "$cert_file" <<'PY'
import json
import sys
from math_proofs.steiner_system import evaluate_steiner_system

instance = json.loads(sys.argv[1])
with open(sys.argv[2], encoding='utf-8') as fh:
    cert = json.load(fh)

report = evaluate_steiner_system(instance, cert)
print(f"score={report['score']:.2f}")
print(f"is_valid={report['is_valid']}")
print(f"exact_once={report['exact_once_r_subsets']}/{report['total_required_r_subsets']}")
print(f"uncovered={report['uncovered_r_subsets']}")
print(f"overcovered={report['overcovered_r_subsets']}")
print(f"actual_blocks={report['actual_block_count']}")
print(f"expected_blocks={report['expected_block_count']}")
PY
}

evaluate_candidate_json() {
  local instance_json="$1"
  local cert_file="$2"
  python3 - "$instance_json" "$cert_file" <<'PY'
import json
import sys
from math_proofs.steiner_system import evaluate_steiner_system

instance = json.loads(sys.argv[1])
with open(sys.argv[2], encoding='utf-8') as fh:
    cert = json.load(fh)

print(json.dumps(evaluate_steiner_system(instance, cert), indent=2, sort_keys=True))
PY
}

discover_prior_runs_json() {
  python3 - "$LOG_ROOT" "$RUN_LOG_DIR" <<'PY'
from __future__ import annotations

import json
import re
from pathlib import Path
import sys

log_root = Path(sys.argv[1])
current_run_dir = Path(sys.argv[2]).resolve()

run_dirs = sorted([p for p in log_root.glob("run_*") if p.is_dir()])
prior = [p for p in run_dirs if p.resolve() != current_run_dir]

placeholders = {
    "advance statement:",
    "evidence from this round (metrics, runtime, structure):",
    "transfer value for next rounds:",
    "hypothesis statement:",
    "mechanism (why this should help):",
    "expected metric movement:",
    "falsification / stop condition:",
    "url:",
    "takeaway:",
    "applied change from source:",
    "round2-4 practice trend summary:",
    "generalized lessons for next research round (new hypothesis families, not repeated essay notes):",
    "-",
}


def parse_summary_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Round "):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 9:
            continue
        rows.append(
            {
                "round": parts[0],
                "mode": parts[1],
                "instance": parts[2],
                "score": parts[3],
                "valid": parts[4],
                "exact_once": parts[5],
                "uncovered": parts[6],
                "overcovered": parts[7],
                "notes": parts[8],
            }
        )
    return rows

def run_max_round(run_dir: Path) -> int:
    summary = run_dir / "RUN_SUMMARY.md"
    if not summary.exists():
        return 0
    max_round = 0
    for raw_line in summary.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Round "):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 1:
            continue
        try:
            round_num = int(parts[0])
        except ValueError:
            continue
        max_round = max(max_round, round_num)
    return max_round


def note_has_signal(note_path: Path) -> bool:
    if not note_path.exists():
        return False
    text = note_path.read_text(encoding="utf-8")
    section_titles = ["Core advance", "Next-hypothesis", "Observations", "Research (this round)", "Work log"]
    for title in section_titles:
        m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
        if not m:
            continue
        for raw_line in m.group(1).splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("- "):
                line = line[2:].strip()
            if not line:
                continue
            if line.lower() in placeholders:
                continue
            if line.startswith("H1:") or line.startswith("H2:") or line.startswith("H3:"):
                continue
            return True
    return False


def is_meaningful_run(run_dir: Path) -> bool:
    rows = parse_summary_rows(run_dir / "RUN_SUMMARY.md")
    if len(rows) < 3:
        return False

    max_round = run_max_round(run_dir)
    if max_round < 5 and not (run_dir / "notes" / "round_0005_notes.md").exists():
        return False

    r1_signal = note_has_signal(run_dir / "notes" / "round_0001_notes.md")
    r5_signal = note_has_signal(run_dir / "notes" / "round_0005_notes.md")
    return r1_signal or r5_signal

meaningful_prior = [run_dir for run_dir in prior if is_meaningful_run(run_dir)]
selection_pool = meaningful_prior if meaningful_prior else prior

latest = selection_pool[-1] if selection_pool else None
latest_transfer = latest / "NEXT_GENERATION_TRANSFER.md" if latest else None
latest_summary = latest / "RUN_SUMMARY.md" if latest else None

latest_with_round1 = None
latest_with_round5 = None
for run_dir in reversed(selection_pool):
    if latest_with_round1 is None and note_has_signal(run_dir / "notes" / "round_0001_notes.md"):
        latest_with_round1 = run_dir
    if latest_with_round5 is None and note_has_signal(run_dir / "notes" / "round_0005_notes.md"):
        latest_with_round5 = run_dir
    if latest_with_round1 is not None and latest_with_round5 is not None:
        break

if latest_with_round1 is None:
    for run_dir in reversed(selection_pool):
        if (run_dir / "notes" / "round_0001_notes.md").exists():
            latest_with_round1 = run_dir
            break

if latest_with_round5 is None:
    for run_dir in reversed(selection_pool):
        if (run_dir / "notes" / "round_0005_notes.md").exists():
            latest_with_round5 = run_dir
            break

latest_round1 = latest_with_round1 / "notes" / "round_0001_notes.md" if latest_with_round1 else None
latest_round5 = latest_with_round5 / "notes" / "round_0005_notes.md" if latest_with_round5 else None

payload = {
    "run_count_total": len(run_dirs),
    "run_count_prior": len(prior),
    "run_count_meaningful_prior": len(meaningful_prior),
    "latest_run_dir": str(latest) if latest else "",
    "latest_run_id": latest.name if latest else "",
    "latest_run_with_round1_id": latest_with_round1.name if latest_with_round1 else "",
    "latest_run_with_round5_id": latest_with_round5.name if latest_with_round5 else "",
    "latest_round1_notes": str(latest_round1) if latest_round1 and latest_round1.exists() else "",
    "latest_round5_notes": str(latest_round5) if latest_round5 and latest_round5.exists() else "",
    "latest_transfer": str(latest_transfer) if latest_transfer and latest_transfer.exists() else "",
    "latest_summary": str(latest_summary) if latest_summary and latest_summary.exists() else "",
    "recent_run_ids": [p.name for p in prior[-10:]],
}
print(json.dumps(payload))
PY
}

file_excerpt() {
  local path="$1"
  local max_lines="${2:-120}"
  if [[ -n "$path" && -f "$path" ]]; then
    sed -n "1,${max_lines}p" "$path"
  else
    echo "(missing)"
  fi
}

refresh_cross_run_context() {
  PRIOR_RUNS_JSON="$(discover_prior_runs_json)"
  LATEST_PRIOR_RUN_ID="$(jq -r '.latest_run_id // ""' <<<"$PRIOR_RUNS_JSON")"
  LATEST_PRIOR_RUN_DIR="$(jq -r '.latest_run_dir // ""' <<<"$PRIOR_RUNS_JSON")"
  LATEST_PRIOR_ROUND1_RUN_ID="$(jq -r '.latest_run_with_round1_id // ""' <<<"$PRIOR_RUNS_JSON")"
  LATEST_PRIOR_ROUND5_RUN_ID="$(jq -r '.latest_run_with_round5_id // ""' <<<"$PRIOR_RUNS_JSON")"
  LATEST_PRIOR_ROUND1_NOTES="$(jq -r '.latest_round1_notes // ""' <<<"$PRIOR_RUNS_JSON")"
  LATEST_PRIOR_ROUND5_NOTES="$(jq -r '.latest_round5_notes // ""' <<<"$PRIOR_RUNS_JSON")"
  LATEST_PRIOR_TRANSFER="$(jq -r '.latest_transfer // ""' <<<"$PRIOR_RUNS_JSON")"
  LATEST_PRIOR_SUMMARY="$(jq -r '.latest_summary // ""' <<<"$PRIOR_RUNS_JSON")"
  PRIOR_RUN_COUNT="$(jq -r '.run_count_prior // 0' <<<"$PRIOR_RUNS_JSON")"
  PRIOR_MEANINGFUL_COUNT="$(jq -r '.run_count_meaningful_prior // 0' <<<"$PRIOR_RUNS_JSON")"

  HISTORY_PATH="$(generate_repo_history_file)"
  GLOBAL_LOGS_JSON="$(generate_global_knowledge_logs)"
  GLOBAL_RESEARCH_LOG_PATH="$(jq -r '.research_log // ""' <<<"$GLOBAL_LOGS_JSON")"
  GLOBAL_PRACTICE_LOG_PATH="$(jq -r '.practice_log // ""' <<<"$GLOBAL_LOGS_JSON")"
  GLOBAL_RESEARCH_LOG_BYTES="$(jq -r '.research_bytes // 0' <<<"$GLOBAL_LOGS_JSON")"
  GLOBAL_PRACTICE_LOG_BYTES="$(jq -r '.practice_bytes // 0' <<<"$GLOBAL_LOGS_JSON")"
  GLOBAL_RESEARCH_LOG_COMPACTED="$(jq -r '.research_compacted // false' <<<"$GLOBAL_LOGS_JSON")"
  GLOBAL_PRACTICE_LOG_COMPACTED="$(jq -r '.practice_compacted // false' <<<"$GLOBAL_LOGS_JSON")"

  LATEST_PRIOR_ROUND1_EXCERPT="$(file_excerpt "$LATEST_PRIOR_ROUND1_NOTES" 140)"
  LATEST_PRIOR_ROUND5_EXCERPT="$(file_excerpt "$LATEST_PRIOR_ROUND5_NOTES" 180)"
  LATEST_PRIOR_TRANSFER_EXCERPT="$(file_excerpt "$LATEST_PRIOR_TRANSFER" 140)"
  GLOBAL_RESEARCH_EXCERPT="$(file_excerpt "$GLOBAL_RESEARCH_LOG_PATH" 220)"
  GLOBAL_PRACTICE_EXCERPT="$(file_excerpt "$GLOBAL_PRACTICE_LOG_PATH" 260)"
}

global_best_summary_for_instance() {
  local instance_label="$1"
  python3 - "$LOG_ROOT" "$instance_label" <<'PY'
from __future__ import annotations

import json
from pathlib import Path
import sys

log_root = Path(sys.argv[1])
instance_label = sys.argv[2]

best = None
for summary_path in sorted(log_root.glob("run_*/RUN_SUMMARY.md")):
    run_id = summary_path.parent.name
    for raw_line in summary_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Round "):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 9:
            continue
        if parts[2] != instance_label:
            continue
        try:
            score = float(parts[3])
        except ValueError:
            score = 0.0
        row = {
            "found": True,
            "run_id": run_id,
            "round": parts[0],
            "mode": parts[1],
            "instance": parts[2],
            "score": score,
            "valid": parts[4],
            "exact_once": parts[5],
            "uncovered": parts[6],
            "overcovered": parts[7],
            "notes": parts[8],
            "summary_path": str(summary_path),
        }
        if best is None or row["score"] > best["score"]:
            best = row

if best is None:
    print(json.dumps({"found": False}))
else:
    print(json.dumps(best))
PY
}

sync_global_best_candidate() {
  local instance_json="$1"
  local instance_key="$2"
  local local_best_file="$3"
  ensure_json_list_file "$local_best_file"

  local baseline_json
  baseline_json="$(evaluate_candidate_json "$instance_json" "$local_best_file")"

  local source_path=""
  local candidate_path candidate_json better
  while IFS= read -r candidate_path; do
    [[ -z "$candidate_path" ]] && continue
    if [[ "$candidate_path" == "$local_best_file" ]]; then
      continue
    fi
    if ! candidate_json="$(evaluate_candidate_json "$instance_json" "$candidate_path" 2>/dev/null)"; then
      continue
    fi
    better="$(is_report_better "$candidate_json" "$baseline_json")"
    if [[ "$better" == "1" ]]; then
      baseline_json="$candidate_json"
      source_path="$candidate_path"
    fi
  done < <(find "$LOG_ROOT" -type f -path "*/candidates/best_${instance_key}.json" | sort)

  if [[ -n "$source_path" ]]; then
    cp "$source_path" "$local_best_file"
    echo "Imported cross-run best candidate: $source_path -> $local_best_file"
  fi

  SYNC_GLOBAL_BEST_JSON="$baseline_json"
  SYNC_GLOBAL_BEST_SOURCE="$source_path"
}

generate_repo_history_file() {
  python3 - "$LOG_ROOT" "$RUN_LOG_DIR" "$REPO_HISTORY_FILE" <<'PY'
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

log_root = Path(sys.argv[1])
current_run_dir = Path(sys.argv[2]).resolve()
output_path = Path(sys.argv[3])

run_dirs = sorted([p for p in log_root.glob("run_*") if p.is_dir()])
prior = [p for p in run_dirs if p.resolve() != current_run_dir]
placeholders = {
    "advance statement:",
    "evidence from this round (metrics, runtime, structure):",
    "transfer value for next rounds:",
    "hypothesis statement:",
    "mechanism (why this should help):",
    "expected metric movement:",
    "falsification / stop condition:",
    "url:",
    "takeaway:",
    "applied change from source:",
    "-",
}


def run_max_round(run_dir: Path) -> int:
    summary = run_dir / "RUN_SUMMARY.md"
    if not summary.exists():
        return 0
    max_round = 0
    for raw_line in summary.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Round "):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if not parts:
            continue
        try:
            round_num = int(parts[0])
        except ValueError:
            continue
        max_round = max(max_round, round_num)
    return max_round


def note_has_signal(note_path: Path) -> bool:
    if not note_path.exists():
        return False
    text = note_path.read_text(encoding="utf-8")
    pattern = r"^## (Core advance|Next-hypothesis|Observations|Research \(this round\)|Work log)\n(.*?)(?=^## |\Z)"
    for m in re.finditer(pattern, text, flags=re.MULTILINE | re.DOTALL):
        for raw_line in m.group(2).splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("- "):
                line = line[2:].strip()
            if not line:
                continue
            if line.lower() in placeholders:
                continue
            if line.startswith("H1:") or line.startswith("H2:") or line.startswith("H3:"):
                continue
            return True
    return False


def is_meaningful_run(run_dir: Path) -> bool:
    summary = run_dir / "RUN_SUMMARY.md"
    if not summary.exists():
        return False
    rows = [
        line
        for line in summary.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("|")
        and not line.strip().startswith("|---")
        and not line.strip().startswith("| Round ")
    ]
    if len(rows) < 3:
        return False
    if run_max_round(run_dir) < 5 and not (run_dir / "notes" / "round_0005_notes.md").exists():
        return False
    return note_has_signal(run_dir / "notes" / "round_0001_notes.md") or note_has_signal(
        run_dir / "notes" / "round_0005_notes.md"
    )


meaningful_prior = [run_dir for run_dir in prior if is_meaningful_run(run_dir)]
selection_pool = meaningful_prior if meaningful_prior else prior
latest = selection_pool[-1] if selection_pool else None

latest_with_round1 = None
latest_with_round5 = None
for run_dir in reversed(selection_pool):
    if latest_with_round1 is None and note_has_signal(run_dir / "notes" / "round_0001_notes.md"):
        latest_with_round1 = run_dir
    if latest_with_round5 is None and note_has_signal(run_dir / "notes" / "round_0005_notes.md"):
        latest_with_round5 = run_dir
    if latest_with_round1 is not None and latest_with_round5 is not None:
        break

if latest_with_round1 is None:
    for run_dir in reversed(selection_pool):
        if (run_dir / "notes" / "round_0001_notes.md").exists():
            latest_with_round1 = run_dir
            break

if latest_with_round5 is None:
    for run_dir in reversed(selection_pool):
        if (run_dir / "notes" / "round_0005_notes.md").exists():
            latest_with_round5 = run_dir
            break

rows = []
for summary_path in sorted(log_root.glob("run_*/RUN_SUMMARY.md")):
    run_id = summary_path.parent.name
    for raw_line in summary_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Round "):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 9:
            continue
        try:
            score = float(parts[3])
        except ValueError:
            score = 0.0
        rows.append(
            {
                "run_id": run_id,
                "round": parts[0],
                "mode": parts[1],
                "instance": parts[2],
                "score": score,
                "valid": parts[4],
                "exact_once": parts[5],
                "uncovered": parts[6],
                "overcovered": parts[7],
            }
        )

best_by_instance = {}
for row in rows:
    key = row["instance"]
    if key not in best_by_instance or row["score"] > best_by_instance[key]["score"]:
        best_by_instance[key] = row

lines = [
    "# Repo-Wide Steiner History",
    "",
    f"Generated (UTC): {dt.datetime.now(dt.timezone.utc).isoformat()}",
    f"Log root: {log_root}",
    f"Current run dir: {current_run_dir}",
    "",
    f"- Total run dirs found: {len(run_dirs)}",
    f"- Prior run dirs found: {len(prior)}",
    f"- Meaningful prior run dirs found: {len(meaningful_prior)}",
]
if latest:
    lines.append(f"- Latest prior run: {latest.name}")
else:
    lines.append("- Latest prior run: none")
lines.append("")

lines.append("## Best Known By Instance (across all runs)")
if best_by_instance:
    lines.append("| Instance | Score | Run | Round | Valid | Exact Once | Uncovered | Overcovered |")
    lines.append("|---|---:|---|---:|---|---|---:|---:|")
    for instance in sorted(best_by_instance):
        row = best_by_instance[instance]
        lines.append(
            f"| {instance} | {row['score']:.2f} | {row['run_id']} | {row['round']} | "
            f"{row['valid']} | {row['exact_once']} | {row['uncovered']} | {row['overcovered']} |"
        )
else:
    lines.append("- No summary rows found yet.")
lines.append("")

def section_excerpt(path: Path, title: str) -> list[str]:
    if not path.exists():
        return ["(missing)"]
    text = path.read_text(encoding="utf-8")
    pattern = rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not m:
        return ["(section missing)"]
    body = [line.rstrip() for line in m.group(1).strip().splitlines()[:30]]
    return body if body else ["(empty section)"]

if latest:
    r1 = latest_with_round1 / "notes" / "round_0001_notes.md" if latest_with_round1 else latest / "notes" / "round_0001_notes.md"
    r5 = latest_with_round5 / "notes" / "round_0005_notes.md" if latest_with_round5 else latest / "notes" / "round_0005_notes.md"
    lines.extend(
        [
            "## Latest Prior Run Key Notes",
            f"- Latest prior run: {latest.name}",
            f"- Latest run with round1 notes: {latest_with_round1.name if latest_with_round1 else 'none'}",
            f"- Latest run with round5 notes: {latest_with_round5.name if latest_with_round5 else 'none'}",
            f"- Round1 notes: {r1}",
            f"- Round5 notes: {r5}",
            "",
        ]
    )
    lines.append("### Round1 Core advance excerpt")
    for line in section_excerpt(r1, "Core advance"):
        lines.append(f"- {line}" if line and not line.startswith("-") else line)
    lines.append("")
    lines.append("### Round5 Core advance excerpt")
    for line in section_excerpt(r5, "Core advance"):
        lines.append(f"- {line}" if line and not line.startswith("-") else line)
    lines.append("")

output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(str(output_path))
PY
}

generate_global_knowledge_logs() {
  python3 - "$LOG_ROOT" "$RUN_LOG_DIR" "$GLOBAL_RESEARCH_LOG_FILE" "$GLOBAL_PRACTICE_LOG_FILE" "$GLOBAL_LOG_MAX_BYTES" <<'PY'
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

log_root = Path(sys.argv[1])
current_run_dir = Path(sys.argv[2]).resolve()
research_log = Path(sys.argv[3])
practice_log = Path(sys.argv[4])
max_bytes = max(1000, int(sys.argv[5]))

run_dirs = sorted([p for p in log_root.glob("run_*") if p.is_dir()])

placeholders = {
    "advance statement:",
    "evidence from this round (metrics, runtime, structure):",
    "transfer value for next rounds:",
    "hypothesis statement:",
    "mechanism (why this should help):",
    "expected metric movement:",
    "falsification / stop condition:",
    "url:",
    "takeaway:",
    "applied change from source:",
    "round2-4 practice trend summary:",
    "generalized lessons for next research round (new hypothesis families, not repeated essay notes):",
    "h1:",
    "h2:",
    "h3:",
    "-",
}


def text_size_bytes(text: str) -> int:
    return len(text.encode("utf-8"))


def parse_summary_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Round "):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 9:
            continue
        rows.append(
            {
                "round": parts[0],
                "mode": parts[1],
                "instance": parts[2],
                "score": parts[3],
                "valid": parts[4],
                "exact_once": parts[5],
                "uncovered": parts[6],
                "overcovered": parts[7],
                "notes": parts[8],
            }
        )
    return rows


def extract_section_items(text: str, title: str) -> list[str]:
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    if not m:
        return []
    items = []
    for raw_line in m.group(1).strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        line_l = line.lower()
        if line_l in placeholders:
            continue
        if line_l.startswith("h1:") or line_l.startswith("h2:") or line_l.startswith("h3:"):
            continue
        items.append(line)
    return items


def run_round_note(run_dir: Path, round_num: int) -> Path:
    return run_dir / "notes" / f"round_{round_num:04d}_notes.md"


url_set: set[str] = set()
research_records: list[dict[str, object]] = []
practice_rows: list[dict[str, object]] = []
practice_highlights: list[dict[str, object]] = []

for run_dir in run_dirs:
    run_id = run_dir.name
    summary_rows = parse_summary_rows(run_dir / "RUN_SUMMARY.md")
    by_round = {row["round"]: row for row in summary_rows}

    # Research (round1) aggregation.
    r1_path = run_round_note(run_dir, 1)
    if r1_path.exists():
        text = r1_path.read_text(encoding="utf-8")
        research_items = []
        for section in ["Research (this round)", "Core advance", "Next-hypothesis", "Observations"]:
            research_items.extend(extract_section_items(text, section))
        urls = sorted(set(re.findall(r"https?://\\S+", text)))
        for url in urls:
            url_set.add(url.rstrip(").,"))

        if research_items or urls:
            row = by_round.get("1", {})
            research_records.append(
                {
                    "run_id": run_id,
                    "score": row.get("score", "?"),
                    "valid": row.get("valid", "?"),
                    "exact_once": row.get("exact_once", "?"),
                    "uncovered": row.get("uncovered", "?"),
                    "overcovered": row.get("overcovered", "?"),
                    "urls": urls[:20],
                    "takeaways": research_items[:20],
                }
            )

    # Practice (round2-5) aggregation.
    for row in summary_rows:
        try:
            round_num = int(row["round"])
        except ValueError:
            continue
        if round_num < 2 or round_num > 5:
            continue
        practice_rows.append(
            {
                "run_id": run_id,
                "round": round_num,
                "instance": row["instance"],
                "score": row["score"],
                "valid": row["valid"],
                "exact_once": row["exact_once"],
                "uncovered": row["uncovered"],
                "overcovered": row["overcovered"],
            }
        )
        note_path = run_round_note(run_dir, round_num)
        if note_path.exists():
            text = note_path.read_text(encoding="utf-8")
            advances = extract_section_items(text, "Core advance")
            hypotheses = extract_section_items(text, "Next-hypothesis")
            if advances or hypotheses:
                practice_highlights.append(
                    {
                        "run_id": run_id,
                        "round": round_num,
                        "advances": advances[:5],
                        "hypotheses": hypotheses[:5],
                    }
                )

generated_at = dt.datetime.now(dt.timezone.utc).isoformat()


def render_research_full() -> str:
    lines = [
        "# Global Research Log (Round1 Knowledge)",
        "",
        f"Generated (UTC): {generated_at}",
        f"Log root: {log_root}",
        f"Current run dir: {current_run_dir}",
        "",
        "## Intent",
        "- Aggregate all run round1 knowledge to avoid repeated essay loops.",
        "- Add new references only when practice logs expose new blockers.",
        "",
        "## Raw Redundancy",
        "- Per-run round logs remain as source of truth under `run_*/notes/round_0001_notes.md`.",
        "",
    ]
    if not research_records:
        lines.append("- No non-placeholder round1 knowledge found yet.")
    else:
        for record in research_records:
            lines.extend(
                [
                    f"### {record['run_id']} / round_0001",
                    f"- Metrics: score={record['score']} valid={record['valid']} "
                    f"exact_once={record['exact_once']} uncovered={record['uncovered']} "
                    f"overcovered={record['overcovered']}",
                ]
            )
            urls = list(record["urls"])
            if urls:
                lines.append("- URLs:")
                lines.extend([f"  - {url}" for url in urls])
            takeaways = list(record["takeaways"])
            if takeaways:
                lines.append("- Key takeaways:")
                lines.extend([f"  - {item}" for item in takeaways])
            lines.append("")
        lines.append("## Deduplicated URL Index")
        if url_set:
            lines.extend([f"- {url}" for url in sorted(url_set)])
        else:
            lines.append("- none")
    return "\n".join(lines) + "\n"


def render_research_compact(recent_limit: int, url_limit: int) -> str:
    recent = research_records[-recent_limit:] if recent_limit > 0 else []
    urls = sorted(url_set)[:url_limit] if url_limit > 0 else []
    lines = [
        "# Global Research Log (Round1 Knowledge)",
        "",
        f"Generated (UTC): {generated_at}",
        f"Log root: {log_root}",
        f"Current run dir: {current_run_dir}",
        f"Compacted: true (max_bytes={max_bytes})",
        "",
        "## Key Stats",
        f"- Runs scanned: {len(run_dirs)}",
        f"- Round1 knowledge entries: {len(research_records)}",
        f"- Unique URLs tracked: {len(url_set)}",
        "",
        "## Raw Redundancy",
        "- Per-run round logs remain as source of truth under `run_*/notes/round_0001_notes.md`.",
        "",
        "## Recent High-Signal Round1 Entries",
    ]
    if not recent:
        lines.append("- No non-placeholder round1 knowledge found yet.")
    else:
        for record in recent:
            lines.append(
                f"- {record['run_id']}: score={record['score']} valid={record['valid']} "
                f"exact_once={record['exact_once']} uncovered={record['uncovered']} overcovered={record['overcovered']}"
            )
            for item in list(record["takeaways"])[:3]:
                lines.append(f"  - takeaway: {item}")
            for url in list(record["urls"])[:2]:
                lines.append(f"  - url: {url}")
    lines.extend(["", "## URL Index (sample)"])
    if urls:
        lines.extend([f"- {url}" for url in urls])
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def best_rows_by_instance(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    best: dict[str, dict[str, object]] = {}
    for row in rows:
        instance = str(row["instance"])
        try:
            score = float(str(row["score"]))
        except ValueError:
            score = 0.0
        if instance not in best or score > float(best[instance]["_score"]):
            cloned = dict(row)
            cloned["_score"] = score
            best[instance] = cloned
    return [best[k] for k in sorted(best)]


def render_practice_full() -> str:
    lines = [
        "# Global Practice Log (Rounds2-5)",
        "",
        f"Generated (UTC): {generated_at}",
        f"Log root: {log_root}",
        f"Current run dir: {current_run_dir}",
        "",
        "## Intent",
        "- Aggregate solver behavior and metrics from rounds 2-5 across runs.",
        "- Feed round1 research updates from real practice bottlenecks.",
        "",
        "## Raw Redundancy",
        "- Per-run round logs remain as source of truth under `run_*/notes/round_000{2..5}_notes.md`.",
        "",
        "## Practice Trajectory Table",
        "| Run | Round | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |",
        "|---|---:|---|---:|---|---|---:|---:|",
    ]
    if not practice_rows:
        lines.append("| (none) | - | - | - | - | - | - | - |")
    else:
        for row in practice_rows:
            lines.append(
                f"| {row['run_id']} | {row['round']} | {row['instance']} | {row['score']} | {row['valid']} | "
                f"{row['exact_once']} | {row['uncovered']} | {row['overcovered']} |"
            )
    lines.extend(["", "## Round Highlights"])
    if not practice_highlights:
        lines.append("- No non-placeholder round2-5 highlights found yet.")
    else:
        for h in practice_highlights:
            lines.append(f"- {h['run_id']}/round_{int(h['round']):04d}")
            for item in list(h["advances"])[:5]:
                lines.append(f"  - advance: {item}")
            for item in list(h["hypotheses"])[:5]:
                lines.append(f"  - next-hypothesis: {item}")
    return "\n".join(lines) + "\n"


def render_practice_compact(row_limit: int, highlight_limit: int) -> str:
    recent_rows = practice_rows[-row_limit:] if row_limit > 0 else []
    recent_highlights = practice_highlights[-highlight_limit:] if highlight_limit > 0 else []
    valid_count = sum(1 for row in practice_rows if str(row["valid"]).lower() == "true")
    best_by_instance = best_rows_by_instance(practice_rows)
    lines = [
        "# Global Practice Log (Rounds2-5)",
        "",
        f"Generated (UTC): {generated_at}",
        f"Log root: {log_root}",
        f"Current run dir: {current_run_dir}",
        f"Compacted: true (max_bytes={max_bytes})",
        "",
        "## Key Stats",
        f"- Runs scanned: {len(run_dirs)}",
        f"- Practice rows tracked: {len(practice_rows)}",
        f"- Practice highlight entries: {len(practice_highlights)}",
        f"- Valid rows: {valid_count}",
        "",
        "## Raw Redundancy",
        "- Per-run round logs remain as source of truth under `run_*/notes/round_000{2..5}_notes.md`.",
        "",
        "## Best Known By Instance",
        "| Instance | Best Score | Run | Round | Valid | Exact Once | Uncovered | Overcovered |",
        "|---|---:|---|---:|---|---|---:|---:|",
    ]
    if best_by_instance:
        for row in best_by_instance:
            lines.append(
                f"| {row['instance']} | {row['score']} | {row['run_id']} | {row['round']} | {row['valid']} | "
                f"{row['exact_once']} | {row['uncovered']} | {row['overcovered']} |"
            )
    else:
        lines.append("| (none) | - | - | - | - | - | - | - |")
    lines.extend(
        [
            "",
            "## Recent Practice Trajectory",
            "| Run | Round | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |",
            "|---|---:|---|---:|---|---|---:|---:|",
        ]
    )
    if recent_rows:
        for row in recent_rows:
            lines.append(
                f"| {row['run_id']} | {row['round']} | {row['instance']} | {row['score']} | {row['valid']} | "
                f"{row['exact_once']} | {row['uncovered']} | {row['overcovered']} |"
            )
    else:
        lines.append("| (none) | - | - | - | - | - | - | - |")
    lines.extend(["", "## Recent Highlights"])
    if recent_highlights:
        for h in recent_highlights:
            lines.append(f"- {h['run_id']}/round_{int(h['round']):04d}")
            for item in list(h["advances"])[:2]:
                lines.append(f"  - advance: {item}")
            for item in list(h["hypotheses"])[:2]:
                lines.append(f"  - next-hypothesis: {item}")
    else:
        lines.append("- No non-placeholder round2-5 highlights found yet.")
    return "\n".join(lines) + "\n"


def truncate_to_cap(text: str) -> str:
    if text_size_bytes(text) <= max_bytes:
        return text
    cut = max(0, max_bytes - 220)
    trimmed = text.encode("utf-8")[:cut].decode("utf-8", errors="ignore")
    notice = "\n\n## Truncation Notice\n- Log truncated to respect GLOBAL_LOG_MAX_BYTES.\n"
    return (trimmed + notice).rstrip() + "\n"


def build_research_log() -> tuple[str, bool]:
    full = render_research_full()
    if text_size_bytes(full) <= max_bytes:
        return full, False

    recent_limit = min(120, len(research_records))
    url_limit = min(300, len(url_set))
    while True:
        compact = render_research_compact(recent_limit, url_limit)
        if text_size_bytes(compact) <= max_bytes:
            return compact, True

        changed = False
        if recent_limit > 8:
            recent_limit = max(8, int(recent_limit * 0.7))
            changed = True
        if text_size_bytes(compact) > max_bytes and url_limit > 20:
            url_limit = max(20, int(url_limit * 0.7))
            changed = True
        if not changed:
            return truncate_to_cap(compact), True


def build_practice_log() -> tuple[str, bool]:
    full = render_practice_full()
    if text_size_bytes(full) <= max_bytes:
        return full, False

    row_limit = min(400, len(practice_rows))
    highlight_limit = min(200, len(practice_highlights))
    while True:
        compact = render_practice_compact(row_limit, highlight_limit)
        if text_size_bytes(compact) <= max_bytes:
            return compact, True

        changed = False
        if row_limit > 40:
            row_limit = max(40, int(row_limit * 0.7))
            changed = True
        if text_size_bytes(compact) > max_bytes and highlight_limit > 20:
            highlight_limit = max(20, int(highlight_limit * 0.7))
            changed = True
        if not changed:
            return truncate_to_cap(compact), True


research_text, research_compacted = build_research_log()
practice_text, practice_compacted = build_practice_log()

research_text = truncate_to_cap(research_text)
practice_text = truncate_to_cap(practice_text)

research_log.write_text(research_text, encoding="utf-8")
practice_log.write_text(practice_text, encoding="utf-8")
print(
    json.dumps(
        {
            "research_log": str(research_log),
            "practice_log": str(practice_log),
            "research_bytes": text_size_bytes(research_text),
            "practice_bytes": text_size_bytes(practice_text),
            "research_compacted": research_compacted,
            "practice_compacted": practice_compacted,
        }
    )
)
PY
}

is_report_better() {
  local candidate_json="$1"
  local baseline_json="$2"
  python3 - "$candidate_json" "$baseline_json" <<'PY'
import json
import sys

candidate = json.loads(sys.argv[1])
baseline = json.loads(sys.argv[2])

def rank(report):
    expected = report.get("expected_block_count")
    actual = int(report.get("actual_block_count", 0))
    if expected is None:
        block_gap = 10**9
    else:
        block_gap = abs(actual - int(expected))

    return (
        1 if bool(report.get("is_valid", False)) else 0,
        1 if int(report.get("overcovered_r_subsets", 10**9)) == 0 else 0,
        -int(report.get("overcovered_r_subsets", 10**9)),
        int(report.get("exact_once_r_subsets", 0)),
        -int(report.get("uncovered_r_subsets", 10**9)),
        -block_gap,
        float(report.get("score", 0.0)),
    )

print(1 if rank(candidate) > rank(baseline) else 0)
PY
}

format_query_stack_bullets() {
  echo "$SEARCH_QUERY_STACK" | tr ';' '\n' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e '/^$/d' -e 's/^/- "/' -e 's/$/"/'
}

round_remaining_seconds() {
  local round_start_ts="$1"
  local now_ts elapsed remaining
  now_ts="$(date +%s)"
  elapsed=$((now_ts - round_start_ts))
  remaining=$((ROUND_TIME_LIMIT_SEC - elapsed))
  if (( remaining < 0 )); then
    remaining=0
  fi
  echo "$remaining"
}

should_enter_summary_mode() {
  local remaining_sec="$1"
  if (( remaining_sec <= LOW_TIME_SUMMARY_THRESHOLD_SEC )); then
    return 0
  fi
  return 1
}

append_low_time_summary_note() {
  local round="$1"
  local notes_file="$2"
  local remaining_sec="$3"

  if [[ ! -f "$notes_file" ]]; then
    return 0
  fi

  if ! grep -q "## Low-Time Summary Mode" "$notes_file"; then
    cat >> "$notes_file" <<EOF

## Low-Time Summary Mode
- Remaining budget dropped to ${remaining_sec}s (threshold=${LOW_TIME_SUMMARY_THRESHOLD_SEC}s).
- Skipped heavy solver/model steps to avoid timeout spillover.
- This round switched to synthesis-only handoff updates.
EOF
  fi

  if (( round >= 5 )) && ! has_round5_synthesis_section "$notes_file"; then
    cat >> "$notes_file" <<EOF

## Rounds 1-5 Synthesis
- Cross-run baseline sources: $GLOBAL_RESEARCH_LOG_FILE and $GLOBAL_PRACTICE_LOG_FILE.
- Round2-4 practice trend summary:
- Generalized lessons for next research round (new hypothesis families, not repeated essay notes):
- Top 3 next hypotheses with test protocols for round $((round + 1)):
  - H1:
  - H2:
  - H3:
EOF
  fi
}

min_int() {
  local a="$1"
  local b="$2"
  if (( a < b )); then
    echo "$a"
  else
    echo "$b"
  fi
}

contains_value() {
  local needle="$1"
  shift
  local value
  for value in "$@"; do
    if [[ "$value" == "$needle" ]]; then
      return 0
    fi
  done
  return 1
}

has_round5_synthesis_section() {
  local notes_file="$1"
  if [[ ! -f "$notes_file" ]]; then
    return 1
  fi
  grep -Eq '^[[:space:]]*##[[:space:]]+Rounds[[:space:]]+1-5[[:space:]]+Synthesis[[:space:]]*$' "$notes_file"
}

enforce_round5_synthesis_gate() {
  local round="$1"
  local notes_file="$2"
  local remaining_sec="$3"

  if [[ "$STRICT_ROUND5_SYNTHESIS_GATE" != "1" ]]; then
    return 0
  fi

  if (( round < 5 )); then
    return 0
  fi

  if has_round5_synthesis_section "$notes_file"; then
    return 0
  fi

  echo "Round-$round close gate failed: missing required section '## Rounds 1-5 Synthesis' in $notes_file." >&2
  echo "Remaining round time budget (sec): $remaining_sec" >&2
  echo "Close is blocked to preserve cross-generation knowledge transfer quality." >&2
  return 1
}

run_with_optional_timeout() {
  local timeout_sec="$1"
  shift

  if (( timeout_sec < 1 )); then
    return 124
  fi

  if [[ "$HAS_TIMEOUT_CMD" == "1" ]]; then
    timeout --foreground "$timeout_sec" "$@"
  else
    local cmd_pid watcher_pid rc
    rc=0
    "$@" &
    cmd_pid=$!
    (
      sleep "$timeout_sec"
      if kill -0 "$cmd_pid" 2>/dev/null; then
        kill -TERM "$cmd_pid" 2>/dev/null || true
        sleep 2
        kill -KILL "$cmd_pid" 2>/dev/null || true
      fi
    ) &
    watcher_pid=$!

    wait "$cmd_pid" || rc=$?
    kill "$watcher_pid" 2>/dev/null || true
    wait "$watcher_pid" 2>/dev/null || true
    if (( rc == 143 || rc == 137 )); then
      return 124
    fi
    return "$rc"
  fi
}

print_solver_json_summary() {
  local label="$1"
  local payload="$2"
  if jq -e . >/dev/null 2>&1 <<<"$payload"; then
    local status engine reason score valid blocks uncovered overcovered nodes runtime
    status="$(jq -r '.status // "?"' <<<"$payload")"
    engine="$(jq -r '.engine // "n/a"' <<<"$payload")"
    reason="$(jq -r '.reason // "n/a"' <<<"$payload")"
    score="$(jq -r '.evaluation.score // .repaired_evaluation.score // "n/a"' <<<"$payload")"
    valid="$(jq -r '
      if (.evaluation | type) == "object" and (.evaluation | has("is_valid")) then
        .evaluation.is_valid
      elif (.repaired_evaluation | type) == "object" and (.repaired_evaluation | has("is_valid")) then
        .repaired_evaluation.is_valid
      else
        "n/a"
      end
    ' <<<"$payload")"
    blocks="$(jq -r '.evaluation.actual_block_count // (.candidate|length) // "n/a"' <<<"$payload")"
    uncovered="$(jq -r '.evaluation.uncovered_r_subsets // .repaired_evaluation.uncovered_r_subsets // "n/a"' <<<"$payload")"
    overcovered="$(jq -r '.evaluation.overcovered_r_subsets // .repaired_evaluation.overcovered_r_subsets // "n/a"' <<<"$payload")"
    nodes="$(jq -r '.solver.nodes // "n/a"' <<<"$payload")"
    runtime="$(jq -r '.solver.runtime_sec // "n/a"' <<<"$payload")"
    echo "$label: status=$status engine=$engine score=$score valid=$valid blocks=$blocks uncovered=$uncovered overcovered=$overcovered nodes=$nodes runtime=$runtime"
    echo "$label reason: $reason"
  else
    echo "$label output (non-JSON):"
    echo "$payload"
  fi
}

generate_transfer_file() {
  python3 - "$RUN_LOG_DIR" "$RUN_SUMMARY_FILE" "$NOTES_DIR" "$TRANSFER_FILE" <<'PY'
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

run_log_dir = Path(sys.argv[1])
run_summary = Path(sys.argv[2])
notes_dir = Path(sys.argv[3])
transfer_file = Path(sys.argv[4])


def parse_summary_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    rows: list[dict[str, str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Round "):
            continue

        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 9:
            continue
        rows.append(
            {
                "round": parts[0],
                "mode": parts[1],
                "instance": parts[2],
                "score": parts[3],
                "valid": parts[4],
                "exact_once": parts[5],
                "uncovered": parts[6],
                "overcovered": parts[7],
                "notes": parts[8],
            }
        )
    return rows


def section_items(md_text: str, title: str) -> list[str]:
    pattern = rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, md_text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return []

    body = match.group(1).strip()
    items: list[str] = []
    placeholders = {
        "advance statement:",
        "evidence from this round (metrics, runtime, structure):",
        "transfer value for next rounds:",
        "hypothesis statement:",
        "mechanism (why this should help):",
        "expected metric movement:",
        "falsification / stop condition:",
    }

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "-":
            continue
        if line.startswith("- "):
            item = line[2:].strip()
        else:
            item = line
        if item and item.lower() not in placeholders:
            items.append(item)
    return items


def parse_round_num(path: Path) -> int:
    m = re.search(r"round_(\d+)_notes\.md$", path.name)
    if not m:
        return 0
    return int(m.group(1))


rows = parse_summary_rows(run_summary)
note_files = sorted(notes_dir.glob("round_*_notes.md"), key=parse_round_num)
round_notes: list[dict[str, object]] = []
for note_path in note_files:
    text = note_path.read_text(encoding="utf-8")
    round_notes.append(
        {
            "round_num": parse_round_num(note_path),
            "path": note_path,
            "core_advance": section_items(text, "Core advance"),
            "next_hypothesis": section_items(text, "Next-hypothesis"),
            "observations": section_items(text, "Observations"),
        }
    )

recent_rows = rows[-5:] if len(rows) > 5 else rows
recent_round_nums = {int(r["round"]) for r in recent_rows if r["round"].isdigit()}
recent_notes = [note for note in round_notes if int(note["round_num"]) in recent_round_nums]
if not recent_notes:
    recent_notes = round_notes[-5:]

all_advances: list[str] = []
all_hypotheses: list[str] = []
for note in recent_notes:
    for item in note["core_advance"]:
        all_advances.append(f"round_{int(note['round_num']):04d}: {item}")
    for item in note["next_hypothesis"]:
        all_hypotheses.append(f"round_{int(note['round_num']):04d}: {item}")

if not all_advances:
    all_advances = ["No explicit Core advance bullets captured yet. Fill notes sections to improve transfer quality."]
if not all_hypotheses:
    all_hypotheses = [
        "No explicit Next-hypothesis bullets captured yet. Add falsifiable hypotheses in round notes."
    ]

best_row = None
if rows:
    def score_val(row: dict[str, str]) -> float:
        try:
            return float(row.get("score", "0") or 0.0)
        except ValueError:
            return 0.0
    best_row = max(rows, key=score_val)

latest_row = rows[-1] if rows else None

transfer_lines = [
    "# Next Generation Transfer",
    "",
    f"Generated (UTC): {dt.datetime.now(dt.timezone.utc).isoformat()}",
    f"Run directory: {run_log_dir}",
    "",
    "## Scope",
    "- This document summarizes the latest five rounds (or fewer if run is shorter).",
    "- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.",
    "",
]

if latest_row:
    transfer_lines.extend(
        [
            "## Latest Round Snapshot",
            f"- Round: {latest_row['round']} ({latest_row['mode']})",
            f"- Instance: {latest_row['instance']}",
            f"- Score: {latest_row['score']}",
            f"- Valid: {latest_row['valid']}",
            f"- Exact once: {latest_row['exact_once']}",
            f"- Uncovered: {latest_row['uncovered']}",
            f"- Overcovered: {latest_row['overcovered']}",
            "",
        ]
    )

if best_row:
    transfer_lines.extend(
        [
            "## Best Round So Far",
            f"- Round: {best_row['round']} ({best_row['mode']})",
            f"- Instance: {best_row['instance']}",
            f"- Score: {best_row['score']}",
            f"- Exact once: {best_row['exact_once']}",
            f"- Uncovered: {best_row['uncovered']}",
            f"- Overcovered: {best_row['overcovered']}",
            "",
        ]
    )

transfer_lines.extend(["## Round Trajectory (recent)", "| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |", "|---:|---|---|---:|---|---|---:|---:|"])
for row in recent_rows:
    transfer_lines.append(
        f"| {row['round']} | {row['mode']} | {row['instance']} | {row['score']} | "
        f"{row['valid']} | {row['exact_once']} | {row['uncovered']} | {row['overcovered']} |"
    )
transfer_lines.append("")

transfer_lines.append("## Core Advances (Rounds 1-5 Window)")
for item in all_advances[:20]:
    transfer_lines.append(f"- {item}")
transfer_lines.append("")

transfer_lines.append("## Knowledge Gaps / Blockers")
blockers: list[str] = []
if latest_row and latest_row.get("valid", "").lower() not in {"true", "1"}:
    blockers.append("No fully valid certificate yet; current frontier remains partial.")
if latest_row and latest_row.get("overcovered", "0") != "0":
    blockers.append("Overcovered subsets still appear in latest round; exact completion remains hard.")
if latest_row and latest_row.get("uncovered", "0") not in {"0", "?"}:
    blockers.append("Large uncovered residual remains; prioritize structured completion over random mutation.")
if not blockers:
    blockers.append("No critical blockers recorded from summary table.")
for item in blockers:
    transfer_lines.append(f"- {item}")
transfer_lines.append("")

transfer_lines.append("## Next Hypothesis Ladder (for next generation)")
for idx, item in enumerate(all_hypotheses[:12], start=1):
    transfer_lines.append(f"{idx}. {item}")
transfer_lines.extend(
    [
        "",
        "## Mandatory Next-Round Discipline",
        "1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.",
        "2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.",
        "3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.",
        "4. Update this transfer file at round close to avoid losing accumulated reasoning.",
        "",
    ]
)

transfer_file.write_text("\n".join(transfer_lines) + "\n", encoding="utf-8")
print(str(transfer_file))
PY
}

append_summary_row() {
  local round="$1"
  local mode="$2"
  local instance_label="$3"
  local score="$4"
  local valid="$5"
  local exact_once="$6"
  local uncovered="$7"
  local overcovered="$8"
  local notes="$9"

  printf '| %s | %s | %s | %s | %s | %s | %s | %s | %s |\n' \
    "$round" "$mode" "$instance_label" "$score" "$valid" "$exact_once" "$uncovered" "$overcovered" "$notes" \
    >> "$RUN_SUMMARY_FILE"
}

run_codex_with_prompt() {
  local prompt_text="$1"
  local timeout_sec="${2:-0}"
  if [[ "$USE_CODEX" != "1" ]]; then
    echo "USE_CODEX=0, skipping codex step."
    return 0
  fi

  local rc=0
  if [[ "$CODEX_SEARCH" == "1" && "$CODEX_HAS_SEARCH_FLAG" == "1" ]]; then
    run_with_optional_timeout "$timeout_sec" \
      codex --search exec --full-auto --skip-git-repo-check \
      --model "$CODEX_MODEL" \
      --config "model_reasoning_effort=\"$CODEX_REASONING_EFFORT\"" \
      - <<<"$prompt_text" || rc=$?
  elif [[ "$CODEX_SEARCH" == "1" && "$CODEX_HAS_SEARCH_FLAG" != "1" ]]; then
    if [[ "$CODEX_SEARCH_WARNED" == "0" ]]; then
      echo "Warning: codex CLI does not support --search in this version; running without live web tool." >&2
      CODEX_SEARCH_WARNED=1
    fi
    run_with_optional_timeout "$timeout_sec" \
      codex exec --full-auto --skip-git-repo-check \
      --model "$CODEX_MODEL" \
      --config "model_reasoning_effort=\"$CODEX_REASONING_EFFORT\"" \
      - <<<"$prompt_text" || rc=$?
  else
    run_with_optional_timeout "$timeout_sec" \
      codex exec --full-auto --skip-git-repo-check \
      --model "$CODEX_MODEL" \
      --config "model_reasoning_effort=\"$CODEX_REASONING_EFFORT\"" \
      - <<<"$prompt_text" || rc=$?
  fi

  if (( rc == 124 )); then
    echo "Codex step reached round time limit (${ROUND_TIME_LIMIT_SEC}s)." >&2
    return 124
  fi
  if (( rc != 0 )); then
    echo "Codex step exited with status $rc; continuing with current candidate." >&2
  fi
  return 0
}

SYNC_GLOBAL_BEST_JSON=""
SYNC_GLOBAL_BEST_SOURCE=""
PRIOR_RUNS_JSON=""
LATEST_PRIOR_RUN_ID=""
LATEST_PRIOR_RUN_DIR=""
LATEST_PRIOR_ROUND1_RUN_ID=""
LATEST_PRIOR_ROUND5_RUN_ID=""
LATEST_PRIOR_ROUND1_NOTES=""
LATEST_PRIOR_ROUND5_NOTES=""
LATEST_PRIOR_TRANSFER=""
LATEST_PRIOR_SUMMARY=""
PRIOR_RUN_COUNT="0"
PRIOR_MEANINGFUL_COUNT="0"
GLOBAL_LOGS_JSON=""
GLOBAL_RESEARCH_LOG_PATH="$GLOBAL_RESEARCH_LOG_FILE"
GLOBAL_PRACTICE_LOG_PATH="$GLOBAL_PRACTICE_LOG_FILE"
GLOBAL_RESEARCH_LOG_BYTES="0"
GLOBAL_PRACTICE_LOG_BYTES="0"
GLOBAL_RESEARCH_LOG_COMPACTED="false"
GLOBAL_PRACTICE_LOG_COMPACTED="false"
GLOBAL_RESEARCH_EXCERPT="(missing)"
GLOBAL_PRACTICE_EXCERPT="(missing)"
LATEST_PRIOR_ROUND1_EXCERPT="(missing)"
LATEST_PRIOR_ROUND5_EXCERPT="(missing)"
LATEST_PRIOR_TRANSFER_EXCERPT="(missing)"
HISTORY_PATH=""

refresh_cross_run_context

echo "Run started (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Unique run log dir: $RUN_LOG_DIR"
echo "Rounds=$ROUNDS target_r_values=${TARGET_R_ARRAY[*]} model=$CODEX_MODEL reasoning=$CODEX_REASONING_EFFORT search=$CODEX_SEARCH"
echo "Instance override set: $([[ -n "$INSTANCE_JSON" ]] && echo yes || echo no)"
echo "Max targeted searches per solve round: $MAX_TARGETED_SEARCH_PER_SOLVE_ROUND"
echo "Auto residual exact-repair: $AUTO_RESIDUAL_REPAIR"
echo "Exact-cover backbone enabled: $EXACT_BACKBONE_ENABLED (r-values: ${EXACT_BACKBONE_R_ARRAY[*]})"
echo "Round time limit (sec): $ROUND_TIME_LIMIT_SEC"
echo "Low-time summary threshold (sec): $LOW_TIME_SUMMARY_THRESHOLD_SEC"
echo "Global log max bytes per file: $GLOBAL_LOG_MAX_BYTES"
echo "Strict round-5 synthesis gate: $STRICT_ROUND5_SYNTHESIS_GATE"
echo "Repo-wide history file: $HISTORY_PATH"
echo "Global research log: $GLOBAL_RESEARCH_LOG_PATH"
echo "Global practice log: $GLOBAL_PRACTICE_LOG_PATH"
echo "Global research log size: $GLOBAL_RESEARCH_LOG_BYTES bytes (compacted=$GLOBAL_RESEARCH_LOG_COMPACTED)"
echo "Global practice log size: $GLOBAL_PRACTICE_LOG_BYTES bytes (compacted=$GLOBAL_PRACTICE_LOG_COMPACTED)"
echo "Prior runs discovered: $PRIOR_RUN_COUNT (meaningful: $PRIOR_MEANINGFUL_COUNT)"
if [[ -n "$LATEST_PRIOR_RUN_ID" ]]; then
  echo "Latest prior run detected: $LATEST_PRIOR_RUN_ID"
else
  echo "Latest prior run detected: none"
fi
if [[ "$HAS_TIMEOUT_CMD" != "1" ]]; then
  echo "Warning: 'timeout' command not found; round time limit is best-effort only."
fi
query_bullets="$(format_query_stack_bullets)"

# Round 1: research-only cache building.
{
  round=1
  round_start_ts="$(date +%s)"
  r_value="${TARGET_R_ARRAY[0]}"
  instance_json="$(resolve_instance_for_r "$r_value")"
  admissibility_json="$(admissibility_report_json "$instance_json")"
  n="$(jq -r '.n' <<<"$instance_json")"
  q="$(jq -r '.q' <<<"$instance_json")"
  r="$(jq -r '.r' <<<"$instance_json")"
  expected_blocks="$(jq -r '.expected_blocks' <<<"$instance_json")"
  if [[ "$expected_blocks" == "null" || -z "$expected_blocks" ]]; then
    expected_blocks="$(jq -r '.expected_block_count // "?"' <<<"$admissibility_json")"
  fi
  instance_label="S($r,$q,$n)"

  instance_key="${n}_${q}_${r}"
  candidate_file="$CANDIDATE_DIR/candidate_${instance_key}.json"
  best_file="$CANDIDATE_DIR/best_${instance_key}.json"
  notes_file="$NOTES_DIR/round_$(printf '%04d' "$round")_notes.md"

  ensure_json_list_file "$candidate_file"
  ensure_json_list_file "$best_file"

  cat > "$notes_file" <<EOF_NOTES
# Round $round Notes (Research-Only)

Instance: $instance_label
Expected blocks: $expected_blocks

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: $HISTORY_PATH
- Global research log (all runs round1): $GLOBAL_RESEARCH_LOG_PATH
- Global practice log (all runs round2-5): $GLOBAL_PRACTICE_LOG_PATH
- Latest prior run: ${LATEST_PRIOR_RUN_ID:-none}
- Latest prior round1 notes source run: ${LATEST_PRIOR_ROUND1_RUN_ID:-none}
- Latest prior round1 notes: ${LATEST_PRIOR_ROUND1_NOTES:-missing}
- Latest prior round5 notes source run: ${LATEST_PRIOR_ROUND5_RUN_ID:-none}
- Latest prior round5 notes: ${LATEST_PRIOR_ROUND5_NOTES:-missing}
- Latest prior transfer: ${LATEST_PRIOR_TRANSFER:-missing}

## Admissibility gate snapshot
\`\`\`json
$admissibility_json
\`\`\`

## Research (this round)
- URL:
- Takeaway:
- Applied change from source:

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility as a hard gate.
- Define when to use symmetry/exact-cover vs nibble/absorption engines.
- Add new references only if practice logs expose a gap not already covered in global research log.

## Work log
-

## Observations
-

## Core advance
- advance statement:
- evidence from this round (metrics, runtime, structure):
- transfer value for next rounds:

## Next-hypothesis
- hypothesis statement:
- mechanism (why this should help):
- expected metric movement:
- falsification / stop condition:
EOF_NOTES

  echo
  echo "=== Steiner Round $round / $ROUNDS (research-only) ==="
  start_out="$(./run_steiner_round.sh --log-dir "$RUN_LOG_DIR" start \
    --instance-json "$instance_json" \
    --objective "Research-first round: build Large Steiner Systems knowledge cache" \
    --hypothesis "Collect references and derivable tactics before construction")"
  echo "$start_out"
  round_id="$(tail -n1 <<<"$start_out" | tr -d '\r')"

  cache_excerpt="$(sed -n '1,220p' "$KNOWLEDGE_CACHE_FILE")"
  research_prompt=$(cat <<EOF_PROMPT
Goal: Build a high-signal knowledge cache for unknown large Steiner system construction.

Round mode: research-only. Do not prioritize certificate construction in this round.

Files you may edit:
1) $KNOWLEDGE_CACHE_FILE
2) $notes_file
3) $TRANSFER_FILE
4) $HISTORY_PATH

Mandatory tasks:
1) First read cross-run memory before any new search:
   - $GLOBAL_RESEARCH_LOG_PATH
   - $GLOBAL_PRACTICE_LOG_PATH
   - $HISTORY_PATH
   - ${LATEST_PRIOR_ROUND1_NOTES:-"(missing)"}
   - ${LATEST_PRIOR_ROUND5_NOTES:-"(missing)"}
   - ${LATEST_PRIOR_TRANSFER:-"(missing)"}
2) Build the "strong search stack" notes:
   - hard admissibility/divisibility gate;
   - symmetry/Kramer-Mesner exact-cover mode;
   - nibble -> boosting/repair -> absorber -> residual exact-cover mode.
3) Search web/arXiv and add at least $MIN_RESEARCH_REFERENCES high-value sources to $KNOWLEDGE_CACHE_FILE.
4) For each source include URL, 1-2 line takeaway, and explicit implementation consequence for r in {6,7,8,9}.
5) Add one concise engine-selector rubric:
   - when symmetry/orbit compression is plausible;
   - when general randomized construction is better.
6) In $notes_file summarize what rounds 2+ should execute and which metrics to track (point degree, (r-1)-pressure, uncovered/overcovered).
7) Update $TRANSFER_FILE with a concise transfer-ready summary for future rounds.
8) Avoid duplicate round-1 essays: explicitly list what was reused from prior runs and what is genuinely new.
9) Use practice-log failures to drive research deltas:
   - Name the blocker seen in rounds2-5;
   - Cite which source may address it;
   - State one concrete implementation change.

Suggested query stack:
$query_bullets

Current cache excerpt:
\`\`\`markdown
$cache_excerpt
\`\`\`

Current round admissibility snapshot:
\`\`\`json
$admissibility_json
\`\`\`

Repo-wide history excerpt:
\`\`\`markdown
$(sed -n '1,220p' "$HISTORY_PATH")
\`\`\`

Global research log excerpt:
\`\`\`markdown
$GLOBAL_RESEARCH_EXCERPT
\`\`\`

Global practice log excerpt:
\`\`\`markdown
$GLOBAL_PRACTICE_EXCERPT
\`\`\`

Latest prior round1 notes excerpt:
\`\`\`markdown
$LATEST_PRIOR_ROUND1_EXCERPT
\`\`\`

Latest prior round5 notes excerpt:
\`\`\`markdown
$LATEST_PRIOR_ROUND5_EXCERPT
\`\`\`

Latest prior transfer excerpt:
\`\`\`markdown
$LATEST_PRIOR_TRANSFER_EXCERPT
\`\`\`
EOF_PROMPT
)
  remaining_sec="$(round_remaining_seconds "$round_start_ts")"
  if should_enter_summary_mode "$remaining_sec"; then
    echo "Round $round entering low-time summary mode (remaining=${remaining_sec}s)."
    append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
  elif (( remaining_sec < 1 )); then
    echo "Round $round time budget exhausted before Codex step; continuing to close/log."
    append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
  else
    codex_rc=0
    run_codex_with_prompt "$research_prompt" "$remaining_sec" || codex_rc=$?
    if (( codex_rc == 124 )); then
      remaining_sec="$(round_remaining_seconds "$round_start_ts")"
      append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
    fi
  fi

  close_json="$(./run_steiner_round.sh --log-dir "$RUN_LOG_DIR" close \
    --round-id "$round_id" \
    --certificate-file "$candidate_file" \
    --notes-file "$notes_file" \
    --technique "research-cache" 2>&1 || true)"
  echo "$close_json"

  round_json="$(evaluate_candidate_json "$instance_json" "$candidate_file")"
  score="$(jq -r '.score // 0' <<<"$round_json")"
  valid="$(jq -r '.is_valid' <<<"$round_json")"
  exact_once="$(jq -r '(.exact_once_r_subsets|tostring) + "/" + (.total_required_r_subsets|tostring)' <<<"$round_json")"
  uncovered="$(jq -r '.uncovered_r_subsets' <<<"$round_json")"
  overcovered="$(jq -r '.overcovered_r_subsets' <<<"$round_json")"
  append_summary_row "$round" "research" "$instance_label" "$score" "$valid" "$exact_once" "$uncovered" "$overcovered" "cache-build"
  transfer_path="$(generate_transfer_file)"
  echo "Updated transfer artifact: $transfer_path"
  refresh_cross_run_context
  echo "Updated repo-wide history: $HISTORY_PATH"
  echo "Updated global research/practice logs: $GLOBAL_RESEARCH_LOG_PATH (${GLOBAL_RESEARCH_LOG_BYTES}B, compacted=$GLOBAL_RESEARCH_LOG_COMPACTED) , $GLOBAL_PRACTICE_LOG_PATH (${GLOBAL_PRACTICE_LOG_BYTES}B, compacted=$GLOBAL_PRACTICE_LOG_COMPACTED)"

  echo "Research round target instance: $instance_label expected_blocks=$expected_blocks"
}

# Rounds 2+: solve attempts with reduced repeated search.
if (( ROUNDS >= 2 )); then
  for round in $(seq 2 "$ROUNDS"); do
    round_start_ts="$(date +%s)"
    idx=$(( (round - 2) % ${#TARGET_R_ARRAY[@]} ))
    r_value="${TARGET_R_ARRAY[$idx]}"

    instance_json="$(resolve_instance_for_r "$r_value")"
    admissibility_json="$(admissibility_report_json "$instance_json")"
    n="$(jq -r '.n' <<<"$instance_json")"
    q="$(jq -r '.q' <<<"$instance_json")"
    r="$(jq -r '.r' <<<"$instance_json")"
    expected_blocks="$(jq -r '.expected_blocks' <<<"$instance_json")"
    if [[ "$expected_blocks" == "null" || -z "$expected_blocks" ]]; then
      expected_blocks="$(jq -r '.expected_block_count // "?"' <<<"$admissibility_json")"
    fi
    instance_label="S($r,$q,$n)"

    instance_key="${n}_${q}_${r}"
    candidate_file="$CANDIDATE_DIR/candidate_${instance_key}.json"
    best_file="$CANDIDATE_DIR/best_${instance_key}.json"
    notes_file="$NOTES_DIR/round_$(printf '%04d' "$round")_notes.md"

    ensure_json_list_file "$candidate_file"
    ensure_json_list_file "$best_file"
    sync_global_best_candidate "$instance_json" "$instance_key" "$best_file"
    if [[ -n "$SYNC_GLOBAL_BEST_SOURCE" ]]; then
      echo "Cross-run best imported for $instance_label from: $SYNC_GLOBAL_BEST_SOURCE"
    fi
    cp "$best_file" "$candidate_file"

    best_json="$SYNC_GLOBAL_BEST_JSON"
    if [[ -z "$best_json" ]]; then
      best_json="$(evaluate_candidate_json "$instance_json" "$best_file")"
    fi
    best_out="$(evaluate_candidate "$instance_json" "$best_file")"
    best_score="$(jq -r '.score // 0' <<<"$best_json")"
    global_best_json="$(global_best_summary_for_instance "$instance_label")"
    global_best_line="$(jq -r '
      if .found then
        "score=" + (.score|tostring) + " run=" + .run_id + " round=" + .round +
        " valid=" + .valid + " exact_once=" + .exact_once + " uncovered=" + .uncovered + " overcovered=" + .overcovered
      else
        "none"
      end
    ' <<<"$global_best_json")"

    cat > "$notes_file" <<EOF_NOTES
# Round $round Notes

Instance: $instance_label
Expected blocks: $expected_blocks

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: $HISTORY_PATH
- Global research log (all runs round1): $GLOBAL_RESEARCH_LOG_PATH
- Global practice log (all runs round2-5): $GLOBAL_PRACTICE_LOG_PATH
- Latest prior run: ${LATEST_PRIOR_RUN_ID:-none}
- Latest prior round1 notes source run: ${LATEST_PRIOR_ROUND1_RUN_ID:-none}
- Latest prior round1 notes: ${LATEST_PRIOR_ROUND1_NOTES:-missing}
- Latest prior round5 notes source run: ${LATEST_PRIOR_ROUND5_RUN_ID:-none}
- Latest prior round5 notes: ${LATEST_PRIOR_ROUND5_NOTES:-missing}
- Latest prior transfer: ${LATEST_PRIOR_TRANSFER:-missing}
- Best known metrics across all runs for this instance: $global_best_line

## Admissibility gate snapshot
\`\`\`json
$admissibility_json
\`\`\`

## Research reuse
- Read $GLOBAL_RESEARCH_LOG_PATH, $GLOBAL_PRACTICE_LOG_PATH, then $KNOWLEDGE_CACHE_FILE.
- At most $MAX_TARGETED_SEARCH_PER_SOLVE_ROUND targeted search(es) if cache is insufficient.

## Plan
- Stage A: decide engine (symmetry/orbit exact-cover vs randomized nibble pipeline).
- Stage B: reserve flex/absorber blocks up front.
- Stage C: improve via large-neighborhood repair and residual exact completion when eligible.

## Work log
-

## Observations
-

## Core advance
- advance statement:
- evidence from this round (metrics, runtime, structure):
- transfer value for next rounds:

## Next-hypothesis
- hypothesis statement:
- mechanism (why this should help):
- expected metric movement:
- falsification / stop condition:
EOF_NOTES

    echo
    echo "=== Steiner Round $round / $ROUNDS (solve) ==="
    echo "Target: $instance_label expected_blocks=$expected_blocks"
    echo "Current best metrics for this instance:"
    echo "$best_out"

    start_out="$(./run_steiner_round.sh --log-dir "$RUN_LOG_DIR" start \
      --instance-json "$instance_json" \
      --objective "Construct $instance_label with highest verifier score" \
      --hypothesis "Use cached knowledge first; minimal repeated search")"
    echo "$start_out"
    round_id="$(tail -n1 <<<"$start_out" | tr -d '\r')"

    exact_backbone_status=""
    exact_backbone_engine=""
    exact_backbone_used=0
    skip_codex_for_round=0
    summary_only_round=0
    remaining_sec="$(round_remaining_seconds "$round_start_ts")"
    if should_enter_summary_mode "$remaining_sec"; then
      summary_only_round=1
      echo "Round $round entering low-time summary mode before heavy stages (remaining=${remaining_sec}s)."
      append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
    fi

    if (( summary_only_round == 0 )) && [[ "$EXACT_BACKBONE_ENABLED" == "1" ]] && contains_value "$r" "${EXACT_BACKBONE_R_ARRAY[@]}"; then
      remaining_sec="$(round_remaining_seconds "$round_start_ts")"
      if should_enter_summary_mode "$remaining_sec"; then
        summary_only_round=1
        echo "Round $round switched to low-time summary mode before exact-cover backbone (remaining=${remaining_sec}s)."
        append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
      elif (( remaining_sec > 0 )); then
        exact_timeout="$(min_int "$EXACT_BACKBONE_TIMEOUT_SEC" "$remaining_sec")"
        echo "Running exact-cover backbone for $instance_label (timeout=${exact_timeout}s)."
        exact_rc=0
        exact_json="$(run_with_optional_timeout "$exact_timeout" python3 -m math_proofs.steiner_exact_cover \
          --instance-json "$instance_json" \
          --candidate-file "$candidate_file" \
          --output-file "$candidate_file" \
          --time-limit-sec "$exact_timeout" \
          --max-nodes "$EXACT_BACKBONE_MAX_NODES" \
          --full-exact-max-rows "$EXACT_BACKBONE_FULL_MAX_ROWS" \
          --full-exact-max-options "$EXACT_BACKBONE_FULL_MAX_OPTIONS" \
          --random-seed "$round" 2>&1)" || exact_rc=$?
        if (( exact_rc == 124 )); then
          echo "Exact-cover backbone timed out after ${exact_timeout}s."
          exact_json='{"status":"timeout","engine":"exact-cover","reason":"wall-clock timeout wrapper"}'
        fi
        print_solver_json_summary "Exact-backbone" "$exact_json"
        exact_backbone_status="$(jq -r '.status // empty' <<<"$exact_json" 2>/dev/null || true)"
        exact_backbone_engine="$(jq -r '.engine // empty' <<<"$exact_json" 2>/dev/null || true)"
        if [[ -n "$exact_backbone_status" ]]; then
          exact_backbone_used=1
        fi
        if [[ "$exact_backbone_status" == "solved" || "$exact_backbone_status" == "already_valid" ]]; then
          skip_codex_for_round=1
          echo "Exact-cover backbone produced a valid certificate; skipping codex step for this round."
        fi
      else
        echo "Round $round time budget exhausted before exact-cover backbone stage."
      fi
    fi

    cache_excerpt="$(sed -n '1,260p' "$KNOWLEDGE_CACHE_FILE")"
    round5_transfer_instruction=""
    if (( round >= 5 )); then
      round5_transfer_instruction=$(cat <<EOF_ROUND5
- Because this is round $round, include a dedicated \"Rounds 1-5 Synthesis\" section in $notes_file:
  - synthesize rounds 2-5 practice trajectory (not just round $round),
  - connect those practice outcomes back to round1 research priorities,
  - strongest advances by round,
  - failed directions and why they failed,
  - top 3 next hypotheses with test protocol for round $((round + 1)).
- Update $TRANSFER_FILE with this synthesis before finishing.
EOF_ROUND5
      )
    fi
    solve_prompt=$(cat <<EOF_PROMPT
Goal: Improve $candidate_file as a candidate certificate for $instance_label.

Files you may edit:
1) $candidate_file
2) $notes_file
3) $KNOWLEDGE_CACHE_FILE (only for incremental additions)
4) $TRANSFER_FILE
5) $HISTORY_PATH
6) $GLOBAL_RESEARCH_LOG_PATH
7) $GLOBAL_PRACTICE_LOG_PATH

Hard constraints:
- Keep $candidate_file as JSON list of blocks.
- Each block must have exactly q=$q distinct integers in [0, $((n - 1))].
- Enforce admissibility as a strict gate before search.
- Prioritize verifier improvements: uncovered/overcovered reduction plus lower (r-1)-oversubscription.

Required solve architecture:
1) Engine selection:
   - Try symmetry/orbit compression idea first (cyclic/dihedral/pivot-stabilizer style) and use it if tractable.
   - Otherwise run general pipeline: nibble -> boosting/repair -> absorber/flex completion.
2) Reserve absorber/flex capacity early (do not consume all blocks greedily).
3) Use LNS-style repairs (remove k conflicting blocks, refill with exact/near-exact local re-pack), not only 1-for-1 swaps.
4) If residual is small and has no overcoverage, attempt exact residual completion.
5) Record per-round metrics in $notes_file:
   - point degree spread;
   - max (r-1)-subset load vs target;
   - uncovered/overcovered trend.

Reasoning/search policy for this round:
- First read cross-run memory before doing anything else:
  - $GLOBAL_RESEARCH_LOG_PATH
  - $GLOBAL_PRACTICE_LOG_PATH
  - $HISTORY_PATH
  - ${LATEST_PRIOR_ROUND1_NOTES:-"(missing)"}
  - ${LATEST_PRIOR_ROUND5_NOTES:-"(missing)"}
  - ${LATEST_PRIOR_TRANSFER:-"(missing)"}
- First read and use cached knowledge below.
- Avoid repeating broad web search already done in round 1.
- At most $MAX_TARGETED_SEARCH_PER_SOLVE_ROUND targeted search(es) only if cache is insufficient.
- If a new source is used, append concise note with URL + takeaway + applied change.
- Write non-trivial Core advance and Next-hypothesis sections in $notes_file (with mechanism and falsification).
- Explicitly state what is reused from previous runs and what is newly learned this round.
$round5_transfer_instruction

Cached knowledge excerpt:
\`\`\`markdown
$cache_excerpt
\`\`\`

Admissibility snapshot:
\`\`\`json
$admissibility_json
\`\`\`

Current best score for this instance: $best_score
Current best metrics:
$best_out

Best known metrics across all runs for this instance:
$global_best_line

Best known summary row (all runs):
\`\`\`json
$global_best_json
\`\`\`

Current best detailed evaluator JSON:
\`\`\`json
$best_json
\`\`\`

Current candidate:
\`\`\`json
$(sed -n '1,240p' "$candidate_file")
\`\`\`

Repo-wide history excerpt:
\`\`\`markdown
$(sed -n '1,220p' "$HISTORY_PATH")
\`\`\`

Global research log excerpt:
\`\`\`markdown
$GLOBAL_RESEARCH_EXCERPT
\`\`\`

Global practice log excerpt:
\`\`\`markdown
$GLOBAL_PRACTICE_EXCERPT
\`\`\`

Latest prior round1 notes excerpt:
\`\`\`markdown
$LATEST_PRIOR_ROUND1_EXCERPT
\`\`\`

Latest prior round5 notes excerpt:
\`\`\`markdown
$LATEST_PRIOR_ROUND5_EXCERPT
\`\`\`
EOF_PROMPT
    )
    remaining_sec="$(round_remaining_seconds "$round_start_ts")"
    if (( summary_only_round == 0 )) && should_enter_summary_mode "$remaining_sec"; then
      summary_only_round=1
      echo "Round $round switched to low-time summary mode before Codex stage (remaining=${remaining_sec}s)."
      append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
    fi

    if (( summary_only_round == 1 )); then
      echo "Codex stage skipped due to low-time summary mode."
    elif [[ "$skip_codex_for_round" == "1" ]]; then
      echo "Codex stage skipped due to exact-cover backbone success."
    else
      if (( remaining_sec < 1 )); then
        echo "Round $round time budget exhausted before Codex step; skipping model step."
        append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
      else
        codex_rc=0
        run_codex_with_prompt "$solve_prompt" "$remaining_sec" || codex_rc=$?
        if (( codex_rc == 124 )); then
          remaining_sec="$(round_remaining_seconds "$round_start_ts")"
          append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
        fi
      fi
    fi

    residual_repair_status=""
    if (( summary_only_round == 0 )) && [[ "$AUTO_RESIDUAL_REPAIR" == "1" && "$skip_codex_for_round" != "1" ]]; then
      remaining_sec="$(round_remaining_seconds "$round_start_ts")"
      if should_enter_summary_mode "$remaining_sec"; then
        summary_only_round=1
        echo "Round $round switched to low-time summary mode before residual repair (remaining=${remaining_sec}s)."
        append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
      fi
      pre_close_json="$(evaluate_candidate_json "$instance_json" "$candidate_file")"
      residual_eligible="$(jq -r '.residual_repair_hint.eligible' <<<"$pre_close_json")"
      if (( summary_only_round == 0 )) && [[ "$residual_eligible" == "true" ]] && (( remaining_sec > 0 )); then
        repair_timeout="$(min_int "$RESIDUAL_REPAIR_TIMEOUT_SEC" "$remaining_sec")"
        echo "Residual exact-repair eligible for $instance_label; attempting additive exact completion."
        repair_rc=0
        repair_json="$(run_with_optional_timeout "$repair_timeout" python3 -m math_proofs.steiner_residual_repair \
          --instance-json "$instance_json" \
          --candidate-file "$candidate_file" \
          --output-file "$candidate_file" \
          --timeout-sec "$repair_timeout" \
          --max-nodes "$RESIDUAL_REPAIR_MAX_NODES" \
          --max-uncovered-r-subsets "$RESIDUAL_REPAIR_MAX_UNCOVERED" \
          --max-q-subset-scan "$RESIDUAL_REPAIR_MAX_Q_SUBSET_SCAN" 2>&1)" || repair_rc=$?
        if (( repair_rc == 124 )); then
          echo "Residual exact-repair timed out after ${repair_timeout}s."
          repair_json='{"status":"timeout","engine":"residual-exact-cover","reason":"wall-clock timeout wrapper"}'
        fi
        print_solver_json_summary "Residual-repair" "$repair_json"
        residual_repair_status="$(jq -r '.status // empty' <<<"$repair_json" 2>/dev/null || true)"
      elif [[ "$residual_eligible" == "true" ]]; then
        echo "Residual exact-repair skipped: round time limit reached."
      fi
    fi

    remaining_sec="$(round_remaining_seconds "$round_start_ts")"
    if should_enter_summary_mode "$remaining_sec"; then
      append_low_time_summary_note "$round" "$notes_file" "$remaining_sec"
    fi
    if ! enforce_round5_synthesis_gate "$round" "$notes_file" "$remaining_sec"; then
      exit 1
    fi

    close_technique_args=(--technique "solve-r${r}-round-${round}")
    if [[ "$exact_backbone_used" == "1" ]]; then
      close_technique_args+=(--technique "exact-backbone-${exact_backbone_engine:-none}-${exact_backbone_status:-unknown}")
    fi
    if [[ "$residual_repair_status" == "solved" ]]; then
      close_technique_args+=(--technique "residual-exact-cover")
    fi

    close_json=""
    if close_json="$(./run_steiner_round.sh --log-dir "$RUN_LOG_DIR" close \
      --round-id "$round_id" \
      --certificate-file "$candidate_file" \
      --notes-file "$notes_file" \
      "${close_technique_args[@]}" 2>&1)"; then
      :
    else
      echo "$close_json"
      echo "Close failed; reverting candidate to best-known for this instance and retrying close."
      cp "$best_file" "$candidate_file"
      close_json="$(./run_steiner_round.sh --log-dir "$RUN_LOG_DIR" close \
        --round-id "$round_id" \
        --certificate-file "$candidate_file" \
        --notes-file "$notes_file" \
        --technique "fallback-best-r${r}-round-${round}" 2>&1 || true)"
    fi
    echo "$close_json"

    round_out="$(evaluate_candidate "$instance_json" "$candidate_file")"
    round_json="$(evaluate_candidate_json "$instance_json" "$candidate_file")"
    round_score="$(jq -r '.score // 0' <<<"$round_json")"

    better="$(is_report_better "$round_json" "$best_json")"
    if [[ "$better" == "1" ]]; then
      cp "$candidate_file" "$best_file"
      best_json="$round_json"
      best_score="$round_score"
      echo "New best candidate for $instance_label (exactness-first rank, score=$best_score)."
    else
      cp "$best_file" "$candidate_file"
      echo "No improvement for $instance_label. Reverted candidate to best-known."
    fi

    valid="$(jq -r '.is_valid' <<<"$round_json")"
    exact_once="$(jq -r '(.exact_once_r_subsets|tostring) + "/" + (.total_required_r_subsets|tostring)' <<<"$round_json")"
    uncovered="$(jq -r '.uncovered_r_subsets' <<<"$round_json")"
    overcovered="$(jq -r '.overcovered_r_subsets' <<<"$round_json")"
    append_summary_row "$round" "solve" "$instance_label" "$round_score" "$valid" "$exact_once" "$uncovered" "$overcovered" "r=$r"
    transfer_path="$(generate_transfer_file)"
    echo "Updated transfer artifact: $transfer_path"
    refresh_cross_run_context
    echo "Updated repo-wide history: $HISTORY_PATH"
    echo "Updated global research/practice logs: $GLOBAL_RESEARCH_LOG_PATH (${GLOBAL_RESEARCH_LOG_BYTES}B, compacted=$GLOBAL_RESEARCH_LOG_COMPACTED) , $GLOBAL_PRACTICE_LOG_PATH (${GLOBAL_PRACTICE_LOG_BYTES}B, compacted=$GLOBAL_PRACTICE_LOG_COMPACTED)"

    if [[ -f "$RUN_LOG_DIR/rounds/NEXT_ROUND_BRIEF.md" ]]; then
      echo "--- Next-round brief (top) ---"
      sed -n '1,40p' "$RUN_LOG_DIR/rounds/NEXT_ROUND_BRIEF.md"
    fi
  done
fi

echo
transfer_path="$(generate_transfer_file)"
echo "Updated transfer artifact: $transfer_path"
refresh_cross_run_context
echo "Updated repo-wide history: $HISTORY_PATH"
echo "Updated global research/practice logs: $GLOBAL_RESEARCH_LOG_PATH (${GLOBAL_RESEARCH_LOG_BYTES}B, compacted=$GLOBAL_RESEARCH_LOG_COMPACTED) , $GLOBAL_PRACTICE_LOG_PATH (${GLOBAL_PRACTICE_LOG_BYTES}B, compacted=$GLOBAL_PRACTICE_LOG_COMPACTED)"
echo "Run finished (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Unique logs: $RUN_LOG_DIR"
echo "Knowledge cache: $KNOWLEDGE_CACHE_FILE"
echo "Run summary: $RUN_SUMMARY_FILE"
echo "Knowledge transfer: $TRANSFER_FILE"
