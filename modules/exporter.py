# modules/exporter.py
import pandas as pd   # <-- AGGIUNGI QUESTO IMPORT
import io

def esporta_excel(df, file_name='classifica_judo.xlsx'):
    """
    Esporta il DataFrame in formato Excel
    """
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()
