#!/bin/zsh

set -e

PROJECT_DIR="${0:A:h}"
cd "$PROJECT_DIR"

if [[ ! -x ".venv/bin/python" ]]; then
  python3 -m venv .venv
fi

if ! .venv/bin/python -c "import streamlit" >/dev/null 2>&1; then
  .venv/bin/python -m pip install -r requirements.txt
fi

if curl -fsS "http://localhost:8501/_stcore/health" >/dev/null 2>&1; then
  open "http://localhost:8501"
  exit 0
fi

nohup .venv/bin/python -m streamlit run app.py \
  --server.headless true \
  --server.port 8501 \
  > /tmp/sehrin-nabzi-streamlit.log 2>&1 &

echo $! > .streamlit-server.pid

for _ in {1..40}; do
  if curl -fsS "http://localhost:8501/_stcore/health" >/dev/null 2>&1; then
    open "http://localhost:8501"
    exit 0
  fi
  sleep 0.25
done

echo "Arayüz başlatılamadı. Günlük: /tmp/sehrin-nabzi-streamlit.log"
read -k 1 "?Kapatmak için bir tuşa basın."
exit 1
