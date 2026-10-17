#!/bin/zsh

PROJECT_DIR="${0:A:h}"
PID_FILE="$PROJECT_DIR/.streamlit-server.pid"

if [[ -f "$PID_FILE" ]]; then
  PID="$(cat "$PID_FILE")"
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
  fi
  rm -f "$PID_FILE"
else
  PORT_PID="$(lsof -ti tcp:8501 -sTCP:LISTEN 2>/dev/null | head -n 1)"
  if [[ -n "$PORT_PID" ]] && ps -p "$PORT_PID" -o command= | grep -q "streamlit run app.py"; then
    kill "$PORT_PID"
  fi
fi

echo "Şehrin Nabzı arayüzü durduruldu."
