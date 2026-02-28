# Enterprise Spam Detection Engine (DistilBERT)

An end-to-end, full-stack NLP architecture designed to intercept sophisticated spear-phishing and spam payloads. This project utilizes a fine-tuned Hugging Face Transformer model integrated with a high-performance FastAPI backend and an asynchronous JavaScript frontend.

## 🧠 Model Architecture & Hardware

- **Core Engine:** `distilbert-base-uncased` (66 Million Parameters)
- **Frameworks:** PyTorch, Hugging Face `transformers`, FastAPI, Uvicorn.
- **Hardware Acceleration:** Trained natively on Apple Silicon (Mac mini M4) utilizing PyTorch Metal Performance Shaders (MPS) for optimized GPU matrix multiplication.
- **Evaluation Metric:** Achieved high F1-Score and validation accuracy (99.99%) during the evaluation phase.

## ☁️ MLOps & Remote Model Registry

To comply with strict version control constraints (GitHub's 100 MB limit), the heavy 285 MB Deep Learning artifacts are decoupled from this repository and hosted on the Hugging Face Model Hub.

The FastAPI backend is configured to dynamically resolve the Hub API. Upon the first server boot, it will automatically download the pre-trained `.safetensors` matrix and tokenizer configurations directly into the active RAM.
* **View the Model Registry Here:** [https://huggingface.co/COSMIC-2318/Distilbert-enterprise-spam-detector]

## 📊 Data Engineering & The 70MB Merged Corpus

To train a highly resilient Transformer, a custom training corpus was engineered by manually merging three distinct open-source datasets from Kaggle. The final 70 MB dataset is included directly in the `data/` directory of this repository for full reproducibility.

**The Merging Pipeline:**
1. **Aggregation:** Extracted and combined raw text payloads from three separate CSV files to create a diverse distribution of spam topologies (legacy spam, modern spear-phishing, and corporate Ham).
2. **Deduplication:** The merging process natively introduced a 50% data duplication rate due to overlapping Kaggle sources. Rigorous pandas preprocessing was applied to drop identical rows, ensuring the DistilBERT model did not overfit by memorizing duplicate strings.
3. **Class Balancing:** Finalized the dataset by balancing the legitimate and malicious labels prior to feeding the tensors into the Apple Silicon GPU.

**Dataset Sources:**
* **Dataset 1:** [https://www.kaggle.com/datasets/gouravkimarif/spam-ham-500000-rows-38-3-mb]
* **Dataset 2:** [https://www.kaggle.com/datasets/shu998866/spam-detection-for-email-filtering-system]
* **Dataset 3:** [https://www.kaggle.com/datasets/amineipad/phishingemaildataset]

## ⚙️ System Architecture

1. **The Backend (`app.py`):** A RESTful API built with FastAPI. It maps the Hugging Face Repository ID, loads the remote matrix into memory, and exposes a `/predict` webhook. It utilizes `CORSMiddleware` to securely handle cross-origin browser requests.
2. **The Frontend (`index.html`):** A lightweight, zero-dependency HTML interface utilizing asynchronous JavaScript (`fetch()`) to pass text payloads to the active inference engine.

## 🚀 Local Deployment Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/COSMIC-2318/Spam_Detection_dlmodel.git](https://github.com/COSMIC-2318/Spam_Detection_dlmodel.git)
   cd Spam_Detection_dlmodel
