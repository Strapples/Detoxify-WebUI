FROM python:3.10.13-slim

WORKDIR /app

# Install basic dependencies
RUN pip install --upgrade pip && \
    pip install numpy==1.26.4 torch==2.2.2 torchvision torchaudio detoxify transformers fastapi uvicorn pandas scikit-learn matplotlib

# Copy your app
COPY . .

# Expose port if running API
EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]