import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from config import OPENAI_API_KEY
import streamlit as st

def extraer_lat_lon(df):
    # Extrae lat/lon de la columna googlemaps si tiene formato "lat,lon"
    def get_lat(x):
        try:
            if pd.notnull(x) and ',' in str(x) and "iframe" not in str(x) and "http" not in str(x):
                return float(str(x).split(',')[0])
        except:
            return None
        return None
    def get_lon(x):
        try:
            if pd.notnull(x) and ',' in str(x) and "iframe" not in str(x) and "http" not in str(x):
                return float(str(x).split(',')[1])
        except:
            return None
        return None
    df['lat'] = df['googlemaps'].apply(get_lat)
    df['lon'] = df['googlemaps'].apply(get_lon)
    return df

def responder_pregunta_llm(pregunta, clientes, propiedades):
    pregunta_lower = pregunta.lower()
    # Si la pregunta pide un mapa de propiedades, lo mostramos directamente
    if any(x in pregunta_lower for x in ["mapa", "ubicacion", "ubicación", "puntos"]) and ("propiedad" in pregunta_lower or "propiedades" in pregunta_lower):
        propiedades = extraer_lat_lon(propiedades)
        if 'lat' in propiedades.columns and 'lon' in propiedades.columns:
            df_map = propiedades[['lat', 'lon']].dropna()
            if not df_map.empty:
                st.success("Mapa de ubicaciones de propiedades:")
                st.map(df_map)
                return "Mapa de propiedades mostrado arriba."
            else:
                return "No hay coordenadas válidas para mostrar el mapa."
        else:
            return "No se pudieron extraer coordenadas de googlemaps."

    # Preguntas abiertas usando LLM (PandasAI)
    llm = OpenAI(api_token=OPENAI_API_KEY, model="gpt-4", temperature=0, max_tokens=800, timeout=40)
    config = {"llm": llm, "verbose": False, "enable_cache": False, "save_charts": True, "save_charts_path": "./charts"}
    sdf_clientes = SmartDataframe(clientes, config=config)
    sdf_propiedades = SmartDataframe(propiedades, config=config)

    if "cliente" in pregunta_lower or "clientes" in pregunta_lower:
        respuesta = sdf_clientes.chat(pregunta)
    elif "propiedad" in pregunta_lower or "propiedades" in pregunta_lower:
        respuesta = sdf_propiedades.chat(pregunta)
    else:
        respuesta_clientes = sdf_clientes.chat(pregunta)
        respuesta_propiedades = sdf_propiedades.chat(pregunta)
        respuesta = f"Clientes:\n{respuesta_clientes}\n\nPropiedades:\n{respuesta_propiedades}"
    return respuesta