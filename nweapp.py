import streamlit as st

# CSS para colocar o fundo bonito sem atrapalhar o conteúdo
st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        background-image: url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/fundo-cafe-anime.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }

    /* Fundo de cada bloco de conteúdo */
    .stApp {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1rem;
        border-radius: 12px;
    }

    /* Ajuste visual dos inputs e botões */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>input,
    .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 0.3em;
        border: 1px solid #e0c3a0;
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
