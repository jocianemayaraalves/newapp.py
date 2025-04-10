import streamlit as st
from PIL import Image
import base64

# 👉 Função para fundo via URL
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://i.imgur.com/1F6oWnM.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()

# 👉 Centraliza e aumenta a logo (substituindo o título antigo)
st.markdown(
    """
    <div style='text-align: center; margin-top: -60px; margin-bottom: 10px;'>
        <img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png' width='300'/>
    </div>
    """,
    unsafe_allow_html=True
)
