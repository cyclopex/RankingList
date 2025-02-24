# modules/data_loader.py

import pandas as pd

def carica_dati(file_path, sheet_name='Sheet1'):
    """
    Funzione per caricare i dati dal file Excel
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df
