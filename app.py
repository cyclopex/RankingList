import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione della Dashboard
st.set_page_config(
    page_title='Dashboard Ranking Judo',
    layout='wide',
    initial_sidebar_state='expanded'  # Sidebar aperta al caricamento
)

# Titolo principale con emoji e stile visivo
st.title('🏅 Dashboard Ranking Judo')
st.markdown(
    """
    ## 🎮 Benvenuto nella tua dashboard interattiva
    **Naviga e analizza le tue classifiche in modo semplice!**
    """
)

# Funzioni
def carica_dati(filepath, sheet_name='Sheet1'):
    """
    Carica i dati dal file Excel specificato.
    """
    try:
        data = pd.read_excel(filepath, sheet_name=sheet_name)
        st.success("Dati caricati con successo.")
        return data
    except Exception as e:
        st.error(f"Errore nel caricamento dei dati: {e}")
        return None

def crea_grafico(data, x, y, color, title, graph_type="bar"):
    """
    Crea un grafico basato sui dati e i parametri forniti.
    """
    if graph_type == "bar":
        return px.bar(data, x=x, y=y, color=color, title=title)
    elif graph_type == "line":
        return px.line(data, x=x, y=y, color=color, title=title)
    elif graph_type == "scatter":
        return px.scatter(data, x=x, y=y, size=y, color=color, title=title)
    else:
        st.warning("Tipo di grafico non riconosciuto. Utilizzo di un grafico a barre come predefinito.")
        return px.bar(data, x=x, y=y, color=color, title=title)

# Selettore di ranking
st.sidebar.header('Ranking List')
ranking_file = st.sidebar.selectbox(
    'Seleziona una Ranking List',
    ['RL_U15.xlsx', 'RL_U18.xlsx', 'RL_U21.xlsx', 'RL_U36.xlsx']
)

# Carica il file selezionato
file_path = f'data/{ranking_file}'
df = carica_dati(file_path, sheet_name='Sheet1')

# Navigazione tra le pagine
page = st.sidebar.radio('Seleziona una Pagina', 
                        ['Classifica Generale', 
                         'Filtri e Ricerche', 
                         'Andamenti Temporali',
                         'Confronto Atleti', 
                         'Confronto Società',
                         'Classifica Generale per Società',
                         'TOP TEN'])

# --- Classifica Generale ---
if page == 'Classifica Generale':
    st.header('📊 Classifica Generale')
    if df is not None:
        categoria = st.selectbox('Categoria', df['Categoria'].unique())
        df_cat = df[df['Categoria'] == categoria]
        st.dataframe(df_cat, use_container_width=True)
        fig = crea_grafico(df_cat, x='Nome', y='Punti', color='Ranking', title=f'Classifica {categoria}')
        st.plotly_chart(fig)

# --- Filtri e Ricerche ---
if page == 'Filtri e Ricerche':
    st.header('🔍 Ricerca Avanzata')
    if df is not None:
        societa = st.multiselect('Società', df['Società'].unique())
        categoria = st.multiselect('Categoria', df['Categoria'].unique())
        atleti_selezionati = st.multiselect('Atleti', df['Nome'].unique())

        filtered_df = df.copy()
        if societa:
            filtered_df = filtered_df[filtered_df['Società'].isin(societa)]
        if categoria:
            filtered_df = filtered_df[filtered_df['Categoria'].isin(categoria)]
        if atleti_selezionati:
            filtered_df = filtered_df[filtered_df['Nome'].isin(atleti_selezionati)]

        st.dataframe(filtered_df, use_container_width=True)

        if not filtered_df.empty:
            fig = crea_grafico(filtered_df, x='Nome', y='Punti', color='Società', title='Filtri Avanzati')
            st.plotly_chart(fig)
        else:
            st.warning("Nessun dato corrisponde ai criteri selezionati.")

# --- Andamenti Temporali ---
if page == 'Andamenti Temporali':
    st.header('📈 Andamenti Temporali')
    if df is not None:
        atleti_selezionati = st.multiselect('Atleti', df['Nome'].unique())
        if atleti_selezionati:
            df_atleti = df[df['Nome'].isin(atleti_selezionati)]
            fig = px.line(
                df_atleti,
                x='Data Nascita',  # Supponiamo che questa colonna rappresenti date temporali
                y='Punti',
                color='Nome',
                title='Andamento Temporale'
            )
            st.plotly_chart(fig)

# --- Confronto Atleti ---
if page == 'Confronto Atleti':
    st.header('🆚 Confronto Atleti')
    if df is not None:
        atleti_selezionati = st.multiselect('Atleti', df['Nome'].unique())
        if atleti_selezionati:
            df_atleti = df[df['Nome'].isin(atleti_selezionati)]
            fig = px.line(
                df_atleti,
                x='Categoria',
                y='Punti',
                color='Nome',
                markers=True,
                title='Confronto Atleti'
            )
            st.plotly_chart(fig)

# --- Confronto Società ---
if page == 'Confronto Società':
    st.header('🏢 Confronto Società')
    if df is not None:
        societa_selezionate = st.multiselect('Società', df['Società'].unique())
        if societa_selezionate:
            df_societa = df[df['Società'].isin(societa_selezionate)]
            st.dataframe(df_societa, use_container_width=True)
            fig = px.bar(
                df_societa,
                x='Società',
                y='Punti',
                color='Società',
                title='Confronto Società'
            )
            st.plotly_chart(fig)

# --- Classifica Generale per Società ---
if page == 'Classifica Generale per Società':
    st.header('📊 Classifica per Società')
    if df is not None:
        classifica_societa = (df.groupby('Società', as_index=False)
                                .agg(PuntiTotali=('Punti', 'sum'), NumeroAtleti=('Nome', 'count')))

        classifica_societa['MediaPuntiPerAtleta'] = classifica_societa['PuntiTotali'] / classifica_societa['NumeroAtleti']
        st.dataframe(classifica_societa, use_container_width=True)

# --- TOP TEN ---
if page == 'TOP TEN':
    st.header('🏆 TOP TEN')
    if df is not None:
        # Mostra solo la TOP TEN Totale
        st.subheader('TOP TEN Totale')
        df_top_ten_totale = df.sort_values(by='Punti', ascending=False).head(10)

        # Mostra solo le colonne desiderate
        colonne_da_mostrare = ['Categoria', 'Nome', 'Data Nascita', 'Società', 'Ranking', 'Punti']
        if all(col in df_top_ten_totale.columns for col in colonne_da_mostrare):
            df_top_ten_filtrato = df_top_ten_totale[colonne_da_mostrare]
            # Rimuovi eventuali zeri finali dai dati numerici
            df_top_ten_filtrato = df_top_ten_filtrato.fillna('')
            st.dataframe(df_top_ten_filtrato, use_container_width=True)
        else:
            st.warning("Le colonne necessarie non sono presenti nel dataset.")
