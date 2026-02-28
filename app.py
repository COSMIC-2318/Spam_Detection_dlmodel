import torch
import torch.nn.functional as F
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1. Initialize the Server (This was missing!)
app = FastAPI(title="Enterprise Spam Detection API")

# 2. Bypass Browser Security (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# 3. Load the AI Engine
print("Loading Transformer Model and Tokenizer into memory...")
MODEL_PATH = "./production_spam_detector"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)
model.eval() 
print(f"Model successfully loaded and running on: {device}")

# 4. Define the Expected JSON Payload
class MessageInput(BaseModel):
    text: str

# 5. The Diagnostic Inference Endpoint
@app.post("/predict")
async def predict_spam(request: MessageInput):
    raw_text = request.text
    
    # Process the text
    inputs = tokenizer(
        raw_text, 
        return_tensors="pt", 
        truncation=True, 
        padding=True, 
        max_length=512
    ).to(device)

    # Execute Neural Network Inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        
        # Calculate Probabilities
        probabilities = F.softmax(logits, dim=-1)[0]
        label_mapping = model.config.id2label
        prediction_id = torch.argmax(logits, dim=-1).item()
        
        # Print Diagnostics to VS Code Terminal
        print("\n" + "="*40)
        print("🔍 MODEL INFERENCE DIAGNOSTICS")
        print("="*40)
        print(f"Internal Label Mapping : {label_mapping}")
        print(f"Raw Logits Tensor      : {logits[0].tolist()}")
        print(f"Class 0 Probability    : {probabilities[0].item() * 100:.2f}%")
        print(f"Class 1 Probability    : {probabilities[1].item() * 100:.2f}%")
        print(f"Winning ID             : {prediction_id}")
        print("="*40 + "\n")

   # Extract the raw label from the model (e.g., "LABEL_0")
    raw_verdict = label_mapping.get(prediction_id, "UNKNOWN")
    
    # Translate Hugging Face defaults into enterprise-grade alerts
    if raw_verdict == "LABEL_0":
        final_verdict = "HAM (Legitimate)"
    elif raw_verdict == "LABEL_1":
        final_verdict = "SPAM"
    else:
        final_verdict = str(raw_verdict).upper()
        
    return {"prediction": final_verdict}