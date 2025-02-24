# views/tabs_societa.py

import streamlit as st
from modules.data_loader import carica_dati
from config.settings import EXCEL_FILES, SHEET_NAME
import pandas as pd

# Costante per il numero di risultati per pagina
RISULTATI_PER_PAGINA = 10

def classifica_societa():
    st.markdown("### 🏢 Classifica Società")
    st.divider()

    # --- AGGIUNGIAMO "Tutte" AL SELETTORE DI RANKING LIST ---
    ranking_options = ['Tutte'] + list(EXCEL_FILES.keys())
    ranking_file = st.selectbox(
        '🏆 Seleziona una Ranking List', 
        ranking_options, 
        key="ranking_societa"
    )

    # --- SE È SELEZIONATO "Tutte", SOMMIAMO I PUNTI DI TUTTE LE RANKING ---
    if ranking_file == 'Tutte':
        # Carichiamo e uniamo tutti i DataFrame delle Ranking List
        df_list = []
        for file in EXCEL_FILES.values():
            df_temp = carica_dati(file, sheet_name=SHEET_NAME)
            df_list.append(df_temp)

        # Concatenazione di tutti i DataFrame
        df = pd.concat(df_list, ignore_index=True)

        # Raggruppamento per Società e Somma dei Punti
        df_societa = (
            df.groupby(['Nazione', 'Società'])
            .agg({'Punti': 'sum', 'Nome': 'count'})
            .reset_index()
            .rename(columns={'Nome': 'Numero Atleti', 'Punti': 'Punti Totali'})
        )
        
        # Calcolo della Media Punti per Atleta
        df_societa['Media Punti'] = (df_societa['Punti Totali'] / df_societa['Numero Atleti']).round(2)

    else:
        # Carichiamo il DataFrame per la Ranking List selezionata
        file_path = EXCEL_FILES[ranking_file]
        df = carica_dati(file_path, sheet_name=SHEET_NAME)

        # Raggruppamento per Società con Media Punti
        df_societa = (
            df.groupby(['Nazione', 'Società'])
            .agg({'Punti': 'sum', 'Nome': 'count'})
            .reset_index()
            .rename(columns={'Nome': 'Numero Atleti', 'Punti': 'Punti Totali'})
        )

        # Calcolo della Media Punti per Atleta
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

    # Inizializzazione dello stato per la pagina corrente
    if 'pagina_corrente_societa' not in st.session_state:
        st.session_state.pagina_corrente_societa = 1

    # Numero totale di risultati e pagine
    totale_risultati = len(df_societa)
    totale_pagine = (totale_risultati - 1) // RISULTATI_PER_PAGINA + 1
    
    # Limita la pagina corrente ai limiti disponibili
    pagina_corrente = st.session_state.pagina_corrente_societa
    pagina_corrente = max(1, min(pagina_corrente, totale_pagine))

    # Selezione dei risultati per la pagina corrente
    inizio = (pagina_corrente - 1) * RISULTATI_PER_PAGINA
    fine = inizio + RISULTATI_PER_PAGINA
    df_paginato = df_societa.iloc[inizio:fine]

    # Visualizzazione della Classifica
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

    # Navigazione Paginazione
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Precedente", key="prev_societa"):
            st.session_state.pagina_corrente_societa -= 1
            st.rerun()
    with col2:
        if st.button("➡️ Successivo", key="next_societa"):
            st.session_state.pagina_corrente_societa += 1
            st.rerun()
