# modules/business_logic.py

def applica_filtri(df, sesso='All', categoria='All', ricerca_nome=''):
    """
    Applica i filtri di Sesso, Categoria e Nome Atleta
    """
    if sesso != 'All':
        df = df[df['Sesso'] == ('M' if sesso == 'Maschi' else 'F')]
    if categoria != 'All':
        df = df[df['Categoria'] == categoria]
    if ricerca_nome:
        df = df[df['Nome'].str.contains(ricerca_nome, case=False, na=False)]
    return df

def paginazione(df, pagina_corrente, risultati_per_pagina):
    """
    Funzione per la paginazione dei risultati
    """
    totale_pagine = (len(df) - 1) // risultati_per_pagina + 1
    inizio = (pagina_corrente - 1) * risultati_per_pagina
    fine = inizio + risultati_per_pagina
    return df.iloc[inizio:fine], totale_pagine
