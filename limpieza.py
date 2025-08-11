import unicodedata
import pandas as pd

def limpiar_texto(texto):
    if pd.isnull(texto):
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = " ".join(texto.split())
    return texto