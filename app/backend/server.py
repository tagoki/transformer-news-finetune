import torch
from fastapi import FastAPI, HTTPException
from transformers import BertTokenizerFast, BertForSequenceClassification
from pydantic import BaseModel

class ClientData(BaseModel):
    text: str

MODEL_DIR = r"C:\web_class_news\transformer-news-finetune\app\model\rubert-news_model"

tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

id2label = {
    0: "Экономика",
    1: "Наука и техника",
    2: "Спорт"
}

app = FastAPI()

@app.post("/")
def class_news(data: ClientData):
    print("REQUEST RECEIVED")
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

    return {"label": id2label[pred_id]}
