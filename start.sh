#!/bin/bash
set -e

# Start FastAPI in the background
uvicorn app.main:app --host 0.0.0.0 --port 80 &
FASTAPI_PID=$!

# Start Streamlit in the background
streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

# Handle termination signals
trap "kill $FASTAPI_PID $STREAMLIT_PID" SIGINT SIGTERM

# Keep the script running
wait $FASTAPI_PID $STREAMLIT_PID