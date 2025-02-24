import streamlit as st
import pandas as pd
import plotly.express as px
from utils import carica_dati, crea_grafico, esporta_excel, grafico_combinato

# Configurazione della Dashboard
st.set_page_config(
    page_title='Dashboard Ranking Judo',
    layout='wide',  # Mantiene la larghezza wide ma sarà limitata da CSS
    initial_sidebar_state='collapsed'
)

# --- Rilevamento Dispositivo (Desktop vs Mobile) ---
if 'device' not in st.session_state:
    st.session_state.device = 'desktop'  # Valore predefinito

# JavaScript per rilevare la larghezza dello schermo
detect_device = """
    <script>
        const screenWidth = window.innerWidth;
        if (screenWidth < 768) {
            window.localStorage.setItem("device", "mobile");
        } else {
            window.localStorage.setItem("device", "desktop");
        }
    </script>
"""
st.markdown(detect_device, unsafe_allow_html=True)

# Recupero della variabile dal localStorage
device = st.session_state.device
if st.session_state.device == 'desktop':
    device = st.query_params.get("device", ["desktop"])[0]
else:
    device = 'mobile'
st.session_state.device = device

# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
        @import url('./styles.css');
    </style>
""", unsafe_allow_html=True)

# Titolo principale con emoji e stile visivo
st.title('🏅 Dashboard Ranking Judo')
st.markdown(
    """
    ## 🎮 Benvenuto nella tua dashboard interattiva
    **Naviga e analizza le tue classifiche in modo semplice!**
    """
)

# Selettore di ranking in alto
ranking_file = st.selectbox(
    '🏆 Seleziona una Ranking List',
    ['RL_U15.xlsx', 'RL_U18.xlsx', 'RL_U21.xlsx', 'RL_U36.xlsx']
)

# Carica il file selezionato
file_path = f'data/{ranking_file}'
df = carica_dati(file_path, sheet_name='Sheet1')

# --- Menu Adattivo ---
if st.session_state.device == 'desktop':
    # Menu a Schede (Tabs) per Desktop e Tablet
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🏆 Classifica Generale", 
         "🏆 Classifica Società",
         "🏅 Top 10 Atleti",
         "🔍 Confronti"]
    )

    # --- Classifica Generale ---
    with tab1:
        st.header('📊 Classifica Generale')
        if df is not None:
            categoria = st.selectbox('Categoria', df['Categoria'].unique())
            df_cat = df[df['Categoria'] == categoria]

            colonne_mostrate = ['Categoria', 'Ranking', 'Nome', 'Società', 'Punti']
            df_cat_selezionato = df_cat[colonne_mostrate]

            st.dataframe(df_cat_selezionato.reset_index(drop=True), use_container_width=True)

            fig = crea_grafico(df_cat, x='Nome', y='Punti', color='Ranking', title=f'Classifica {categoria}')
            st.plotly_chart(fig)

            esporta_excel(df_cat_selezionato, file_name=f"classifica_{categoria}.xlsx")

    # --- Classifica Società ---
    with tab2:
        st.header('🏆 Classifica Società')
        if df is not None:
            classifica_societa = df.groupby('Società')['Punti'].sum().reset_index().sort_values(by='Punti', ascending=False)
            st.dataframe(classifica_societa.reset_index(drop=True), use_container_width=True)

            fig = px.bar(classifica_societa, x='Società', y='Punti', color='Società', title='Classifica per Società')
            st.plotly_chart(fig)

            st.subheader('📊 Media Punti per Atleta')
            numero_atleti = df.groupby('Società')['Nome'].nunique().reset_index().rename(columns={'Nome': 'Numero Atleti'})
            media_punti = classifica_societa.merge(numero_atleti, on='Società')
            media_punti['Media Punti per Atleta'] = media_punti['Punti'] / media_punti['Numero Atleti']
            media_punti = media_punti[['Società', 'Media Punti per Atleta']].sort_values(by='Media Punti per Atleta', ascending=False)
            st.dataframe(media_punti.reset_index(drop=True), use_container_width=True)

            fig_media = px.bar(media_punti, 
                               x='Società', 
                               y='Media Punti per Atleta', 
                               color='Società', 
                               title='Media Punti per Atleta',
                               text_auto=True)
            st.plotly_chart(fig_media)

    # --- Top 10 Atleti ---
    with tab3:
        st.header('🏅 Top 10 Atleti')
        if df is not None:
            top_ten = df.sort_values(by='Punti', ascending=False).head(10)
            st.dataframe(top_ten.reset_index(drop=True), use_container_width=True)

            fig = px.bar(top_ten, x='Nome', y='Punti', color='Società', title='Top 10 Atleti')
            st.plotly_chart(fig)

            st.subheader('📊 Media Punti per Atleta nei Top 10')
            media_top_ten = top_ten.copy()
            media_top_ten['Media Punti per Atleta'] = media_top_ten['Punti'] / media_top_ten['Ranking']
            st.dataframe(media_top_ten[['Nome', 'Media Punti per Atleta']].reset_index(drop=True), use_container_width=True)

            fig_media_top = px.bar(media_top_ten, 
                                   x='Nome', 
                                   y='Media Punti per Atleta', 
                                   color='Società', 
                                   title='Media Punti per Atleta nei Top 10',
                                   text_auto=True)
            st.plotly_chart(fig_media_top)

    # --- Confronti ---
    with tab4:
        st.header('🔍 Confronti')
        if df is not None:
            societa = st.multiselect('Seleziona Società', df['Società'].unique())
            categoria = st.multiselect('Seleziona Categorie', df['Categoria'].unique())
            atleti_selezionati = st.multiselect('Seleziona Atleti', df['Nome'].unique())

            filtered_df = df.copy()
            if societa:
                filtered_df = filtered_df[filtered_df['Società'].isin(societa)]
            if categoria:
                filtered_df = filtered_df[filtered_df['Categoria'].isin(categoria)]
            if atleti_selezionati:
                filtered_df = filtered_df[filtered_df['Nome'].isin(atleti_selezionati)]

            st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

            if not filtered_df.empty:
                st.subheader('📊 Punti Totali per Società')
                punti_per_societa = filtered_df.groupby('Società')['Punti'].sum().reset_index()
                fig1 = px.bar(punti_per_societa, 
                              x='Società', 
                              y='Punti', 
                              color='Società', 
                              title='Punti Totali per Società',
                              text_auto=True)
                st.plotly_chart(fig1)

                st.subheader('📊 Punti Totali per Categoria')
                punti_per_categoria = filtered_df.groupby('Categoria')['Punti'].sum().reset_index()
                fig2 = px.bar(punti_per_categoria, 
                              x='Categoria', 
                              y='Punti', 
                              color='Categoria', 
                              title='Punti Totali per Categoria',
                              text_auto=True)
                st.plotly_chart(fig2)
