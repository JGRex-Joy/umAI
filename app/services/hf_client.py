# app/services/hf_client.py
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

HF_MODEL_MISTRAL = "UlutSoftLLC/Mistral-7B-v0.1-kyrgyz-text-completion"
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_with_context(context, query, max_new_tokens=300, retry=3):
    prompt = f"""
Контекст:
{context}

Суроо:
{query}

Жооп бериңиз:
"""
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_new_tokens}}

    for attempt in range(retry):
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{HF_MODEL_MISTRAL}",
                headers=HEADERS,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            return response.json()[0]["generated_text"]
        except Exception as e:
            print(f"[hf_client] Error: {e}, attempt {attempt+1}/{retry}")
            time.sleep(2)
    return "Ошибка генерации текста"
