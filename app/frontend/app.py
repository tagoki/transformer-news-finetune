import streamlit as st
import requests

st.title("Классификация новостей")

with st.form("my_form"):
    text = st.text_input("Введите заголовок")
    submit = st.form_submit_button("Классифицировать")

if submit and text:
    try:
        # 1. Пробуем отправить запрос
        response = requests.post(
            "http://backend:8000/",
            json={"text": text},
            timeout=120  # Увеличил таймаут, вдруг модель медленная
        )
        
        # 2. Если бэк ответил, но с ошибкой (например 503)
        if response.status_code != 200:
            st.error(f"Бэкенд вернул код {response.status_code}")
            st.write("Текст ошибки:", response.text)
        else:
            st.success(f"Результат: {response.json()['label']}")

    except Exception as e:
        # 3. Если вообще не достучались (Connection Error и т.д.)
        st.error(f"Ошибка запроса: {e}")
        print(f"!!! DEBUG LOG: {e}") # Это упадет в консоль докера