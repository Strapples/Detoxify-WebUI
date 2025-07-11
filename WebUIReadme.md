
# LocalWebClient (LWC)

This tool allows real-time analysis of multiple social media posts using Detoxify + RoBERTa model.

Paste posts separated by `&endp` to analyze in batches.

## Don't forget to activate your venv!

## Backend (Python FastAPI)
- Run with: `python -m uvicorn backend.app:app --reload` (This is crucial, otherwise you'll use global system binaries)

## Frontend (React)
- Run with: `npm install && npm start`
