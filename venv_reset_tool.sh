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

echo "🌐 Checking PyPI connectivity..."
if ! curl -s --head https://pypi.org | grep "200 OK" > /dev/null; then
  echo "❌ No internet or PyPI unreachable. Exiting."
  exit 2
fi

echo "🐍 Python in use: $(which python)"
python -c "import sys; print('\n'.join(sys.path))"

echo "📦 Installing pinned packages..."
pip install --upgrade pip
pip install numpy==1.26.4 torch==2.2.2 torchvision torchaudio
pip install uvicorn fastapi python-dotenv
pip install pandas scikit-learn matplotlib
pip install -r requirements.txt

echo "✅ Uvicorn path check:"
python -c "import uvicorn; print('Uvicorn path:', uvicorn.__file__)"

echo "🚀 Running backend..."
python -m uvicorn backend.app:app --reload