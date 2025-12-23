import streamlit as st
import requests

st.title("Классификация новостных заголовков")
st.write("Определите тип новостной статьи по названию")

with st.form("Узнать тему статьи"):
    text = st.text_input("Введите заголовок статьи")
    submit = st.form_submit_button("Классифицировать")

if submit and text:
    data = {'text':text}
    response = requests.post(
        "http://localhost:8000/",
        json={"text": text},
        timeout=10
        )

    if response.status_code == 200:
        st.success(response.json()['label'])
    else:
        st.error(response)

