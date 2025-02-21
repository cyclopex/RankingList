import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione della Dashboard
st.set_page_config(page_title='Dashboard Ranking Judo', layout='wide')
st.title('Dashboard Ranking Judo')

# Funzione per caricare i dati
def carica_dati(filepath, sheet_name='Sheet1'):
    try:
        return pd.read_excel(filepath, sheet_name=sheet_name)
    except Exception as e:
        st.error(f"Errore nel caricamento dei dati: {e}")
        return pd.DataFrame()

# Funzione per visualizzare le pagine
def mostra_pagina_ranking(df, titolo):
    """
    Mostra tutte le funzionalità già implementate: Classifica Generale,
    Filtri e Ricerche, Andamenti Temporali, Obiettivi, ecc.
    """
    st.title(titolo)

    # -- Classifica Generale --
    st.header('Classifica Generale')
    categoria = st.selectbox('Seleziona Categoria', df['Categoria'].unique())
    df_cat = df[df['Categoria'] == categoria]
    st.dataframe(df_cat)
    fig = px.bar(df_cat, x='Nome', y='Punti', color='Società', title=f'Classifica Generale per {categoria}')
    st.plotly_chart(fig)

    # -- Filtri e Ricerche --
    st.header('Filtri e Ricerche')
    societa = st.multiselect('Seleziona Società', df['Società'].unique())
    df_filtrato = df[df['Società'].isin(societa)]
    st.dataframe(df_filtrato)

    # Puoi aggiungere tutte le funzionalità già previste qui
    # come Andamenti Temporali, Obiettivi, ecc.

# Stato corrente della pagina
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Gestione del cambio pagina tramite pulsanti
if st.session_state.current_page == "Home":
    st.header("Home Page")
    st.markdown("Benvenuto nella Dashboard! Scegli una ranking per iniziare.")

    # Bottoni per selezionare la ranking
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("RANKING U15"):
            st.session_state.current_page = "U15"
    with col2:
        if st.button("RANKING U18"):
            st.session_state.current_page = "U18"
    with col3:
        if st.button("RANKING U21"):
            st.session_state.current_page = "U21"
    with col4:
        if st.button("RANKING U36"):
            st.session_state.current_page = "U36"

# Visualizzazione delle pagine delle ranking
if st.session_state.current_page == "U15":
    df_u15 = carica_dati('data/RL_U15.xlsx')
    mostra_pagina_ranking(df_u15, "RANKING U15")

elif st.session_state.current_page == "U18":
    df_u18 = carica_dati('data/RL_U18.xlsx')
    mostra_pagina_ranking(df_u18, "RANKING U18")

elif st.session_state.current_page == "U21":
    df_u21 = carica_dati('data/RL_U21.xlsx')
    mostra_pagina_ranking(df_u21, "RANKING U21")

elif st.session_state.current_page == "U36":
    df_u36 = carica_dati('data/RL_U36.xlsx')
    mostra_pagina_ranking(df_u36, "RANKING U36")
