# views/tabs.py

import streamlit as st
import pandas as pd
from modules.data_loader import carica_dati
from config.settings import EXCEL_FILES, SHEET_NAME
from io import BytesIO


# Costante per il numero di risultati per pagina
RISULTATI_PER_PAGINA = 10

def classifica_generale():
    st.markdown("### 🏆 Classifica Generale")
    st.divider()

# Selettore di Ranking List con l'aggiunta di "Tutte"
    ranking_options = ['Tutte'] + list(EXCEL_FILES.keys())
    ranking_file = st.selectbox(
        '🏆 Seleziona una Ranking List', 
        ranking_options, 
        key="ranking_generale"
    )

    # Caricamento dati
    if ranking_file == 'Tutte':
        # Se viene selezionato "Tutte", concatena tutti i DataFrame
        dfs = [carica_dati(EXCEL_FILES[file], sheet_name=SHEET_NAME) for file in EXCEL_FILES.keys()]
        df = pd.concat(dfs, ignore_index=True)
    else:
        # Altrimenti carica solo la RL selezionata
        file_path = EXCEL_FILES[ranking_file]
        df = carica_dati(file_path, sheet_name=SHEET_NAME)


# --- FILTRO SESSO (PRIMA SCELTA) ---
    sesso = st.selectbox(
        '👫 Seleziona Sesso',
        ['Tutti', 'Maschi', 'Femmine'],
        key="sesso_generale",
        on_change=lambda: st.session_state.update({"reset_pagina_generale": True})
    )

    # Filtra in base al sesso selezionato
    if sesso == 'Maschi':
        df = df[df['Sesso'] == 'M']
    elif sesso == 'Femmine':
        df = df[df['Sesso'] == 'F']

    # --- FILTRO CATEGORIA (SINCRONIZZATO CON SESSO) ---
    if sesso == 'Maschi':
        categorie = ['Tutte'] + sorted(df[df['Sesso'] == 'M']['Categoria'].unique().tolist())
    elif sesso == 'Femmine':
        categorie = ['Tutte'] + sorted(df[df['Sesso'] == 'F']['Categoria'].unique().tolist())
    else:
        categorie = ['Tutte'] + sorted(df['Categoria'].unique().tolist())

    categoria = st.selectbox(
        '📂 Seleziona Categoria', 
        categorie,
        key="categoria_generale",
        on_change=lambda: st.session_state.update({"reset_pagina_generale": True})
    )
    if categoria != 'Tutte':
        df = df[df['Categoria'] == categoria]

    # --- FILTRO RICERCA ATLETA (TERZA SCELTA) ---
    ricerca_nome = st.text_input(
        '🔍 Cerca Atleta', 
        key="ricerca_atleta", 
        on_change=lambda: st.session_state.update({"reset_pagina_generale": True})
    )
    if ricerca_nome:
        df = df[df['Nome'].str.contains(ricerca_nome, case=False, na=False)]

    # --- FILTRO SOCIETÀ (ULTIMA SCELTA) ---
    if 'Società' in df.columns:
        societa_options = ['Tutte'] + sorted(df['Società'].unique().tolist())
        societa = st.selectbox(
            '🏢 Seleziona Società',
            societa_options,
            key="societa_generale",
            on_change=lambda: st.session_state.update({"reset_pagina_generale": True})
        )
        if societa != 'Tutte':
            df = df[df['Società'] == societa]
            df = df.sort_values(by='Ranking', ascending=True)  # ORDINA PER RANK
    else:
        st.warning("❗ La colonna 'Società' non è presente in questa Ranking List.")

    # --- RESET PAGINAZIONE ---
    if 'reset_pagina_generale' not in st.session_state:
        st.session_state.reset_pagina_generale = False
    if st.session_state.reset_pagina_generale:
        st.session_state.pagina_corrente_generale = 1
        st.session_state.reset_pagina_generale = False

    # Inizializzazione dello stato per la pagina corrente
    if 'pagina_corrente_generale' not in st.session_state:
        st.session_state.pagina_corrente_generale = 1

    # Numero totale di risultati e pagine
    totale_risultati = len(df)
    totale_pagine = (totale_risultati - 1) // RISULTATI_PER_PAGINA + 1
    
    # Limita la pagina corrente ai limiti disponibili
    pagina_corrente = st.session_state.pagina_corrente_generale
    pagina_corrente = max(1, min(pagina_corrente, totale_pagine))

    # Selezione dei risultati per la pagina corrente
    inizio = (pagina_corrente - 1) * RISULTATI_PER_PAGINA
    fine = inizio + RISULTATI_PER_PAGINA
    df_paginato = df.iloc[inizio:fine]

    # --- STILE CSS ---
    st.markdown("""
        <style>
            .classifica-container {
                display: flex;
                flex-direction: column;
                gap: 10px;
                padding: 10px;
            }
            .classifica-card {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background-color: #1C1E2F;
                color: #F4F4F9;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease-in-out;
                border: 1px solid transparent;
                cursor: pointer;
            }
            .classifica-card:hover {
                background-color: #2A2C3E;
                transform: scale(1.02);
            }
            .ranking {
                color: #FFD700;
                font-weight: bold;
                font-size: 1.5em;
                margin-right: 15px;
            }
            .flag img {
                width: 35px;
                border-radius: 5px;
                margin-right: 15px;
            }
            .details {
                flex: 1;
                text-align: left;
            }
            .name {
                font-size: 1.2em;
                font-weight: bold;
                color: #F4F4F9;
            }
            .category {
                color: #A6A9B6;
                font-size: 0.9em;
            }
            .points {
                color: #FFD700;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- VISUALIZZAZIONE CLASSIFICA ---
    st.markdown("<div class='classifica-container'>", unsafe_allow_html=True)
    for _, row in df_paginato.iterrows():
        posizione = f"#{row['Ranking']}"
        nome = row['Nome']
        categoria = row['Categoria']
        societa = row['Società'] if 'Società' in row else "N/A"
        punti = row['Punti']
        nazione = row['Nazione'].lower()
        flag_url = f"https://flagcdn.com/w40/{nazione}.png"

        st.markdown(f"""
            <div class='classifica-card'>
                <div class='ranking'>{posizione}</div>
                <div class='flag'>
                    <img src='{flag_url}' alt='flag'>
                </div>
                <div class='details'>
                    <span class='name'>{nome}</span><br>
                    <span class='category'>{categoria} kg - {societa}</span>
                </div>
                <div class='points'>
                    {punti} Punti
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

        # --- NAVIGAZIONE PAGINAZIONE ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Precedente", disabled=(pagina_corrente == 1)):
            st.session_state.pagina_corrente_generale -= 1
            st.rerun()
            st.set_query_params(pagina=st.session_state.pagina_corrente_generale)
    with col2:
        st.markdown(f"<div style='text-align: center;'>Pagina {pagina_corrente} di {totale_pagine}</div>", unsafe_allow_html=True)
    with col3:
        if st.button("➡️ Successivo", disabled=(pagina_corrente == totale_pagine)):
            st.session_state.pagina_corrente_generale += 1
            st.rerun()

