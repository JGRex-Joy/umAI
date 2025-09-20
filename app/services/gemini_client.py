import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyBA7N2zWeSrlrFxR-a68F-zz89w_D9HH4U")

def ask_gemini(query: str, context: str):
    prompt = f"Контекст:\n{context}\n\nВопрос: {query}\nОтвет:"
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text
