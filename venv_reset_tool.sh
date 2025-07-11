#!/bin/bash
set -e

echo "🔪 Nuking old venv..."
rm -rf venv

echo "🐍 Creating new venv with python3.10..."
PYTHON_PATH=$(which python3.10)

if [[ ! -x "$PYTHON_PATH" ]]; then
  echo "❌ python3.10 not found. Install it via Homebrew or ensure it's on PATH."
  exit 1
fi

$PYTHON_PATH -m venv venv
source venv/bin/activate

echo "🐍 Python in use: $(which python)"
echo "📁 sys.path sanity:"
python -c "import sys; print('\n'.join(sys.path))"

echo "📦 Upgrading pip + installing base packages... and grabbing some initial dependencies"
pip install --upgrade pip
pip install "numpy<2.0" torch torchvision torchaudio
pip install uvicorn fastapi python-dotenv
pip install pandas numpy scikit-learn matplotlib


echo "✅ Verifying uvicorn install..."
python -c "import uvicorn; print('Uvicorn path:', uvicorn.__file__)"

echo "Reinstalling the Detoxify requirements so the thing doesn't blow up."
pip install -r requirements.txt


echo "🚀 Starting backend with venv python..."
python -m uvicorn backend.app:app --reload