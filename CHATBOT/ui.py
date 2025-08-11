import streamlit as st
from datos import cargar_datos
from preguntas import responder_pregunta_llm
from config import CLIENTES_TO_SHOW, PROPIEDADES_TO_SHOW

def mostrar_interfaz():
    st.set_page_config(page_title="PRADERAS GPT", page_icon="🤖", layout="wide")
    st.title("🤖 PRADERAS GPT")
    st.markdown("""
    Pregunta lo que quieras sobre tus datos de clientes y propiedades.
    Ejemplo: ¿Cuántos clientes fueron registrados en 2014?
    Ejemplo: ¿Cuál es el promedio de m2 de construcción por estado?
    Ejemplo: ¿Gráfica de propiedades en venta por estado?
    """)

    clientes, propiedades = cargar_datos()

    pregunta = st.text_input("Escribe tu pregunta:")
    if pregunta:
        with st.spinner("Pensando..."):
            respuesta = responder_pregunta_llm(pregunta, clientes, propiedades)
        st.write(respuesta)

    with st.expander("Ver datos de clientes"):
        st.dataframe(clientes[CLIENTES_TO_SHOW].head(20))
    with st.expander("Ver datos de propiedades"):
        st.dataframe(propiedades[PROPIEDADES_TO_SHOW].head(20))