st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        background-image: url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/cafe-fundo.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        color: #3b2e2a;
        font-family: 'Georgia', serif;
    }

    .title {
        text-align: center;
        font-size: 38px;
        color: #7b4b2a;
        margin-bottom: 20px;
        background-color: rgba(255, 245, 235, 0.85);
        padding: 10px;
        border-radius: 15px;
    }

    .stButton>button {
        background-color: #dc9c68;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5em 1em;
        font-weight: bold;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }

    .stButton>button:hover {
        background-color: #c78555;
        color: #fff;
    }

    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input,
    .stDateInput>div>input {
        background-color: rgba(255, 255, 255, 0.85);
        border: 1px solid #e0c3a0;
        border-radius: 10px;
        padding: 0.25em;
    }

    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1em;
    }
    </style>
""", unsafe_allow_html=True)
