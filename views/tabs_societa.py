import streamlit as st
import pandas as pd
from modules.data_loader import carica_dati
from config.settings import EXCEL_FILES, SHEET_NAME
from pathlib import Path

# Costante per il numero di risultati per pagina
RISULTATI_PER_PAGINA = 10

def classifica_societa():
    st.markdown("### 🏢 Classifica Società")
    st.divider()

    # Selettore di Ranking List con l'aggiunta di "Tutte"
    ranking_options = ['Tutte'] + list(EXCEL_FILES.keys())
    ranking_file = st.selectbox(
        '🏆 Seleziona una Ranking List', 
        ranking_options, 
        key="ranking_societa"
    )

    # Caricamento dati con gestione errori per file mancanti
    df = pd.DataFrame()
    if ranking_file == 'Tutte':
        dfs = []
        for file in EXCEL_FILES.keys():
            file_path = Path(EXCEL_FILES[file])
            if not file_path.is_file():
                st.warning(f"⚠️ Ranking {file} non presente.")
                continue
            try:
                df_temp = carica_dati(file_path, sheet_name=SHEET_NAME)
                dfs.append(df_temp)
            except FileNotFoundError:
                st.warning(f"⚠️ Ranking {file} non trovato.")
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
    else:
        file_path = Path(EXCEL_FILES[ranking_file])
        if not file_path.is_file():
            st.warning(f"⚠️ Ranking {ranking_file} non presente.")
        else:
            try:
                df = carica_dati(file_path, sheet_name=SHEET_NAME)
            except FileNotFoundError:
                st.warning(f"⚠️ Ranking {ranking_file} non trovato.")
    
    if df.empty:
        st.info("Nessun dato disponibile.")
        return

    # --- Raggruppamento per Società con Media Punti ---
    df_societa = (
        df.groupby(['Nazione', 'Società'])
        .agg({'Punti': 'sum', 'Nome': 'count'})
        .reset_index()
        .rename(columns={'Nome': 'Numero Atleti', 'Punti': 'Punti Totali'})
    )

    df_societa['Media Punti'] = (df_societa['Punti Totali'] / df_societa['Numero Atleti']).round(2)

    # --- FILTRO RICERCA SOCIETÀ ---
    ricerca_societa = st.text_input(
        '🔍 Cerca Società', 
        key="ricerca_societa", 
        on_change=lambda: st.session_state.update({"reset_pagina_societa": True})
    )
    if ricerca_societa:
        df_societa = df_societa[df_societa['Società'].str.contains(ricerca_societa, case=False, na=False)]

    # --- ORDINAMENTO CLASSIFICA ---
    ordinamento = st.selectbox(
        '🔄 Ordina per',
        ['Punti Totali', 'Media Punti', 'Numero Atleti'],
        key="ordinamento_societa",
        on_change=lambda: st.session_state.update({"reset_pagina_societa": True})
    )

    if ordinamento == 'Punti Totali':
        df_societa = df_societa.sort_values(by='Punti Totali', ascending=False)
    elif ordinamento == 'Media Punti':
        df_societa = df_societa.sort_values(by='Media Punti', ascending=False)
    elif ordinamento == 'Numero Atleti':
        df_societa = df_societa.sort_values(by='Numero Atleti', ascending=False)

    df_societa.reset_index(drop=True, inplace=True)
    df_societa['Ranking'] = df_societa.index + 1

    # --- RESET PAGINAZIONE ---
    if 'reset_pagina_societa' not in st.session_state:
        st.session_state.reset_pagina_societa = False
    if st.session_state.reset_pagina_societa:
        st.session_state.pagina_corrente_societa = 1
        st.session_state.reset_pagina_societa = False

    if 'pagina_corrente_societa' not in st.session_state:
        st.session_state.pagina_corrente_societa = 1

    totale_risultati = len(df_societa)
    totale_pagine = (totale_risultati - 1) // RISULTATI_PER_PAGINA + 1
    
    pagina_corrente = st.session_state.pagina_corrente_societa
    pagina_corrente = max(1, min(pagina_corrente, totale_pagine))

    inizio = (pagina_corrente - 1) * RISULTATI_PER_PAGINA
    fine = inizio + RISULTATI_PER_PAGINA
    df_paginato = df_societa.iloc[inizio:fine]

    # --- VISUALIZZAZIONE CLASSIFICA ---
    st.markdown("<div class='classifica-container'>", unsafe_allow_html=True)
    for _, row in df_paginato.iterrows():
        posizione = f"#{row['Ranking']}"
        nome_societa = row['Società']
        punti_totali = row['Punti Totali']
        numero_atleti = row['Numero Atleti']
        media_punti = row['Media Punti']
        nazione = row['Nazione'].lower()
        flag_url = f"https://flagcdn.com/w40/{nazione}.png"

        st.markdown(f"""
            <div class='classifica-card'>
                <div class='ranking'>{posizione}</div>
                <div class='flag'>
                    <img src='{flag_url}' alt='flag'>
                </div>
                <div class='details'>
                    <span class='name'>{nome_societa}</span><br>
                    <span class='category'>{numero_atleti} Atleti | Media punti per Atleta: {media_punti}</span>
                </div>
                <div class='points'>
                    {punti_totali} Punti
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- NAVIGAZIONE PAGINAZIONE ---
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Precedente", key="prev_societa"):
            st.session_state.pagina_corrente_societa -= 1
            st.rerun()
    with col2:
        if st.button("➡️ Successivo", key="next_societa"):
            st.session_state.pagina_corrente_societa += 1
            st.rerun()
