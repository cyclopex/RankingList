# app.py

import streamlit as st
from views.tabs import classifica_generale
from views.tabs_societa import classifica_societa

# --- CONFIGURAZIONE GENERALE ---
st.set_page_config(
    page_title='FIJLKAM - Dashboard Ranking Judo',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# --- STILE CSS PER RIMUOVERE MARGINE SUPERIORE ---
st.markdown("""
    <style>
        /* Rimuove il margine superiore */
        .css-18e3th9 {
            padding-top: 0 !important;
        }

        /* Titolo */
        .main-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #F4F4F9;
            margin: 0;
        }

        /* Descrizioni */
        .description {
            font-size: 1.2em;
            color: #A6A9B6;
            margin-bottom: 30px;
        }

        /* Etichette dei filtri */
        .filter-label {
            font-size: 1em;
            font-weight: bold;
            color: #F4F4F9;
            margin-bottom: 5px;
        }

        /* Link */
        .dashboard-link {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1em;
            color: #FFD700;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.3s;
        }
        .dashboard-link:hover {
            color: #FFB700;
        }

        /* Stile generale per il testo */
        body {
            font-family: 'Arial', sans-serif;
            color: #F4F4F9;
        }

        /* Stile per le Tabs */
        .stTabs [data-baseweb="tab"] {
            font-family: 'Arial', sans-serif;
            font-size: 1.1em;
            font-weight: bold;
            color: #F4F4F9;
        }

        /* Stile per i contenuti delle Tabs */
        .stTabs [data-baseweb="tab"]:hover {
            color: #FFD700;
        }
    </style>
""", unsafe_allow_html=True)

# --- TITOLO PRINCIPALE ---
st.markdown("""
    <h1 class="main-title">FIJLKAM - Dashboard Ranking Judo</h1>
""", unsafe_allow_html=True)

# --- DESCRIZIONE ---
st.markdown("""
    <div class="description">Esplora le tue classifiche in modo interattivo</div>
""", unsafe_allow_html=True)

# --- MENU A TABS ---
tab1, tab2 = st.tabs(
    [
        "🏆 Classifica Generale", 
        "🏢 Classifica Società"
    ]
)

# --- CONTENUTO DELLE SCHEDE ---
with tab1:
    classifica_generale()

with tab2:
    classifica_societa()

