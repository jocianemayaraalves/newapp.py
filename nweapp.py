import streamlit as st

st.markdown("""
    <style>
    /* BACKGROUND FIX - imagem de fundo no body sem sobrepor o conteúdo */
    body {
        background-image: url('https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/fundo-cafe-anime.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }

    /* Cria uma camada semi-transparente no app para leitura */
    [data-testid="stAppViewContainer"] {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1rem;
        border-radius: 0.5rem;
    }

    /* Melhora campos de entrada */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>input,
    .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 0.3em;
        border: 1px solid #dcbfa8;
    }

    .stButton>button {
        background-color: #dc9c68;
        color: white;
        border-radius: 12px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #c78555;
    }
    </style>
""", unsafe_allow_html=True)
