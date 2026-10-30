import os
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

BASE_MODEL = os.getenv("BASE_MODEL", "Qwen/Qwen3-4B")
ADAPTER_DIR = os.getenv(
    "ADAPTER_DIR",
    "/content/drive/MyDrive/Banking_AI_Chatbot/fast_finetuned_model"
)

app = FastAPI(title="BankMate AI Inference API")

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)

tokenizer = None
model = None

@app.on_event("startup")
def load_model():
    global tokenizer, model
    if not os.path.isdir(ADAPTER_DIR):
        raise RuntimeError(f"Adapter directory not found: {ADAPTER_DIR}")
    if not torch.cuda.is_available():
        raise RuntimeError("A CUDA-enabled GPU is required for this 4-bit model server.")

    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_DIR)
    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=quant_config,
        device_map="auto",
        torch_dtype=torch.float16,
    )
    model = PeftModel.from_pretrained(base, ADAPTER_DIR)
    model.eval()

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/chat")
def chat(req: ChatRequest):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")
    messages = [
        {
            "role": "system",
            "content": (
                "You are BankMate AI, a helpful banking information assistant. "
                "Answer clearly and cautiously. Do not request or expose PINs, "
                "passwords, CVVs, OTPs, or full card/account numbers. "
                "For account-specific actions, direct users to their official bank."
            ),
        },
        {"role": "user", "content": req.question},
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=220,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )
    answer = tokenizer.decode(
        output[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    ).strip()
    return {"answer": answer}
