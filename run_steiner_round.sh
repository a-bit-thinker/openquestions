#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
LOG_DIR="${LOG_DIR:-steiner_logs}"

usage() {
  cat <<USAGE
Usage:
  ./run_steiner_round.sh [--log-dir DIR] start --instance-json '{"n":17,"q":7,"r":6}' --objective 'Construct S(6,7,17)' [--hypothesis '...'] [--parent-round-id round_0001]
  ./run_steiner_round.sh [--log-dir DIR] close --certificate-file candidate.json [--round-id round_0001] [--notes-file notes.md] [--technique name ...]
  ./run_steiner_round.sh [--log-dir DIR] report
  ./run_steiner_round.sh [--log-dir DIR] brief

Notes:
  - Run 'start' first for each round.
  - Run 'close' after you have candidate.json.
  - If --round-id is omitted in close, it uses DIR/LAST_ROUND_ID.
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

# Global options (must come before command)
while [[ $# -gt 0 ]]; do
  case "$1" in
    --log-dir)
      LOG_DIR="$2"
      shift 2
      ;;
    -h|--help|help)
      usage
      exit 0
      ;;
    start|close|report|brief)
      break
      ;;
    *)
      echo "Unknown option or command: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

LAST_ROUND_FILE="$LOG_DIR/LAST_ROUND_ID"
cmd="$1"
shift

case "$cmd" in
  start)
    rid="$($PYTHON_BIN -m math_proofs.steiner_round_logger start --log-dir "$LOG_DIR" "$@")"
    mkdir -p "$LOG_DIR"
    printf '%s\n' "$rid" > "$LAST_ROUND_FILE"
    echo "Started $rid"
    echo "$rid"
    ;;

  close)
    round_id=""
    close_args=()

    while [[ $# -gt 0 ]]; do
      case "$1" in
        --round-id)
          round_id="$2"
          close_args+=("$1" "$2")
          shift 2
          ;;
        *)
          close_args+=("$1")
          shift
          ;;
      esac
    done

    if [[ -z "$round_id" ]]; then
      if [[ ! -f "$LAST_ROUND_FILE" ]]; then
        echo "No --round-id provided and $LAST_ROUND_FILE not found." >&2
        echo "Run start first or pass --round-id." >&2
        exit 1
      fi
      round_id="$(cat "$LAST_ROUND_FILE")"
      close_args=(--round-id "$round_id" "${close_args[@]}")
    fi

    $PYTHON_BIN -m math_proofs.steiner_round_logger close --log-dir "$LOG_DIR" "${close_args[@]}"
    ;;

  report)
    $PYTHON_BIN -m math_proofs.steiner_round_logger report --log-dir "$LOG_DIR"
    ;;

  brief)
    brief_path="$LOG_DIR/rounds/NEXT_ROUND_BRIEF.md"
    if [[ ! -f "$brief_path" ]]; then
      echo "Brief not found at $brief_path. Run report or close a round first." >&2
      exit 1
    fi
    cat "$brief_path"
    ;;

  *)
    echo "Unknown command: $cmd" >&2
    usage
    exit 1
    ;;
esac
