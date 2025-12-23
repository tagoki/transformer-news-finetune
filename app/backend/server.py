import torch
from fastapi import FastAPI, HTTPException
from transformers import BertTokenizerFast, BertForSequenceClassification
from pydantic import BaseModel
from pathlib import Path


class ClientData(BaseModel):
    text: str

BASE_DIR = Path(__file__).resolve().parents[1]  
MODEL_DIR = BASE_DIR / "model" / "rubert-news_model"

tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

id2label = {0: "Экономика", 1: "Наука и техника", 2: "Спорт"}

app = FastAPI()

@app.post("/")
def class_news(data: ClientData):
    text = data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Пустой текст")

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        pred_id = torch.argmax(logits, dim=-1).item()

    label = id2label[pred_id]
    return {"label": label}
