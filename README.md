# Enterprise Spam Detection Engine (DistilBERT)

An end-to-end, full-stack NLP architecture designed to intercept sophisticated spear-phishing and spam payloads. This project utilizes a fine-tuned Hugging Face Transformer model integrated with a high-performance FastAPI backend and an asynchronous JavaScript frontend.

## 🧠 Model Architecture & Training

- **Core Engine:** `distilbert-base-uncased` (66 Million Parameters)
- **Frameworks:** PyTorch, Hugging Face `transformers`, FastAPI, Uvicorn.
- **Hardware Acceleration:** Trained natively on Apple Silicon (Mac mini M4) utilizing PyTorch Metal Performance Shaders (MPS) for optimized GPU matrix multiplication.
- **Evaluation Metric:** Achieved high F1-Score and validation accuracy (99.99%) during the evaluation phase.

## 📊 Data Engineering

The training corpus was engineered by aggregating three distinct, high-quality open-source datasets from Kaggle. 
- Conducted rigorous preprocessing to resolve a 50% data duplication rate inherent in merged open-source corpora.
- Balanced the class distribution between standard corporate "Ham" and sophisticated "Spam/Phishing" payloads to optimize the self-attention mechanism's contextual mapping.

## ⚙️ System Architecture

1. **The Backend (`app.py`):** A RESTful API built with FastAPI. It loads the `.safetensors` matrix into RAM and exposes a `/predict` webhook. It utilizes `CORSMiddleware` to securely handle cross-origin browser requests.
2. **The Frontend (`index.html`):** A lightweight, zero-dependency HTML interface utilizing asynchronous JavaScript (`fetch()`) to pass text payloads to the active inference engine.

## 🚀 Local Deployment Instructions

*Note: Due to GitHub's
