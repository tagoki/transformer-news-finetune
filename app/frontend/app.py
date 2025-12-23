# app/frontend/app.py
import streamlit as st
import requests

import sys
import os

st.title("Классификация новостных заголовков")
st.write("Определите тип новостной статьи по названию")

with st.form("Узнать тему статьи"):
    text = st.text_input("Введите заголовок статьи")
    submit = st.form_submit_button("Классифицировать")

if submit and text:
    data = {"text": text}
    try:
        response = requests.post(
            "http://localhost:8000/",  
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            label = response.json()["label"]
            st.success(label)
        else:
            st.error(response)
    except Exception as e:
        st.error(f"Ошибка: {e}")

