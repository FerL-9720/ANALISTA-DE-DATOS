import unicodedata
import pandas as pd

def limpiar_texto(texto):
    if pd.isnull(texto):
        return ""
    texto = str(texto).strip().lower()
    # Normaliza acentos y ñ
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join([c for c in texto if not unicodedata.combining(c)])
    texto = texto.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    texto = texto.replace('ü', 'u').replace('ñ', 'n')
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    texto = " ".join(texto.split())
    return texto