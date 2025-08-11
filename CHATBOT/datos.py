import pandas as pd
import unicodedata
import streamlit as st
from config import CLIENTES_FILE, PROPIEDADES_FILE

def limpiar_texto(texto):
    if pd.isnull(texto):
        return ""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

@st.cache_data
def cargar_datos():
    clientes = pd.read_excel(CLIENTES_FILE)
    clientes.columns = clientes.columns.str.replace('`', '')
    propiedades = pd.read_excel(PROPIEDADES_FILE)
    for col in ['estado', 'municipio', 'colonia', 'razonsocial', 'contactonombre']:
        if col in clientes.columns:
            clientes[col] = clientes[col].apply(limpiar_texto)
    for col in ['estado', 'municipio', 'colonia', 'nombre']:
        if col in propiedades.columns:
            propiedades[col] = propiedades[col].apply(limpiar_texto)
    if 'created' in clientes.columns:
        clientes['created'] = pd.to_datetime(clientes['created'], errors='coerce')
    if 'created' in propiedades.columns:
        propiedades['created'] = pd.to_datetime(propiedades['created'], errors='coerce')
    return clientes, propiedades