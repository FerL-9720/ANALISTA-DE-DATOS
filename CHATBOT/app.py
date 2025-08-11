import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import unicodedata
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="PRADOS GPT", page_icon="🤖", layout="wide")

st.title("🤖 PRADOS GPT")
st.markdown("""
Pregunta lo que quieras sobre tus datos de clientes y propiedades. Puedes pedir gráficas, predicciones y mapas.
- Ejemplo: **¿Cuántos clientes fueron registrados en 2014?**
- Ejemplo: **¿Cuál es el promedio de m2 de construcción por estado?**
- Ejemplo: **¿En qué año hubo más registros de clientes?**
- Ejemplo: **¿Gráfica de propiedades en venta por estado?**
- Ejemplo: **Top 5 estados con más clientes y su gráfica de barras**
- Ejemplo: **¿Cuántas propiedades tiene cada propietario? (y gráfica de pastel)**
- Ejemplo: **¿Cuál es la tendencia de registros de clientes por mes este año? (y gráfica)**
- Ejemplo: **¿Cuál es la proyección de clientes para el cierre de este año si sigue la tendencia actual? (y gráfica)**
- Ejemplo: **¿Puedes mostrarme un mapa de las propiedades?**
- Ejemplo: **¿Quién es el propietario con más m2 de terreno?**
- Ejemplo: **¿Quién tiene más propiedades?**
- Ejemplo: **¿Cuál es el estado con más m2 de construcción?**
""")

def limpiar_texto(texto):
    if pd.isnull(texto):
        return ""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

@st.cache_data
def cargar_datos():
    clientes = pd.read_excel(r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\clientes_filtrados.xlsx')
    clientes.columns = clientes.columns.str.replace('`', '')
    propiedades = pd.read_excel(r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\propiedades_filtradas.xlsx')
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

clientes, propiedades = cargar_datos()

OPENAI_API_KEY = "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"  # Reemplaza con tu clave real
llm = OpenAI(
    api_token=OPENAI_API_KEY,
    model="gpt-4",
    temperature=0,
    max_tokens=800,
    timeout=40
)
config = {
    "llm": llm,
    "verbose": False,
    "enable_cache": False,
    "save_charts": True,
    "save_charts_path": "./charts"
}
sdf_clientes = SmartDataframe(clientes, config=config)
sdf_propiedades = SmartDataframe(propiedades, config=config)

# --- Conversación (historial) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def fallback_respuesta(pregunta, clientes, propiedades):
    pregunta_l = pregunta.lower()

    # Ejemplo 1: Promedio de m2 de construcción por estado (con gráfica)
    if ("promedio" in pregunta_l or "media" in pregunta_l) and ("m2" in pregunta_l or "metros" in pregunta_l) and "estado" in pregunta_l:
        propiedades['m2construccion'] = pd.to_numeric(propiedades['m2construccion'], errors='coerce')
        promedio = propiedades.groupby('estado')['m2construccion'].mean().reset_index()
        st.success("Promedio de m2 de construcción por estado:")
        st.dataframe(promedio)
        if any(x in pregunta_l for x in ["grafica", "gráfica", "plot", "barras"]):
            fig, ax = plt.subplots()
            promedio.plot(kind='bar', x='estado', y='m2construccion', ax=ax, legend=False)
            plt.ylabel("Promedio m2 construcción")
            plt.xlabel("Estado")
            plt.title("Promedio de m2 de construcción por estado")
            st.pyplot(fig)
        return "Promedio de m2 de construcción por estado mostrado arriba."

    # Ejemplo 2: Año con más registros de clientes (con gráfica)
    if ("clientes" in pregunta_l and ("año" in pregunta_l or "registrados" in pregunta_l) and ("más" in pregunta_l or "mayor" in pregunta_l)):
        if 'created' in clientes.columns:
            clientes['anio'] = clientes['created'].dt.year
            conteo = clientes.groupby('anio').size().reset_index(name='cantidad')
            max_anio = conteo.loc[conteo['cantidad'].idxmax()]
            st.success(f"El año con más registros de clientes fue {int(max_anio['anio'])} con {int(max_anio['cantidad'])} clientes.")
            st.dataframe(conteo)
            if any(x in pregunta_l for x in ["grafica", "gráfica", "plot", "barras"]):
                fig, ax = plt.subplots()
                conteo.plot(kind='bar', x='anio', y='cantidad', ax=ax, legend=False)
                plt.ylabel("Clientes")
                plt.xlabel("Año")
                plt.title("Clientes registrados por año")
                st.pyplot(fig)
        else:
            st.warning("No hay columna 'created' para calcular el año de registro.")
        return "Año con más registros mostrado arriba."

    # Ejemplo 3: Propiedades en venta por estado (con gráfica)
    if ("propiedades" in pregunta_l and "venta" in pregunta_l and "estado" in pregunta_l):
        if 'enventa' in propiedades.columns:
            en_venta = propiedades[propiedades['enventa'] == 1]
            conteo = en_venta.groupby('estado').size().reset_index(name='propiedades_en_venta')
            st.success("Propiedades en venta por estado:")
            st.dataframe(conteo)
            if any(x in pregunta_l for x in ["grafica", "gráfica", "plot", "barras"]):
                fig, ax = plt.subplots()
                conteo.plot(kind='bar', x='estado', y='propiedades_en_venta', ax=ax, legend=False)
                plt.ylabel("Propiedades en venta")
                plt.xlabel("Estado")
                plt.title("Propiedades en venta por estado")
                st.pyplot(fig)
        else:
            st.warning("No hay columna 'enventa' para calcular propiedades en venta.")
        return "Propiedades en venta por estado mostrado arriba."

    # Ejemplo 4: Top 5 estados con más clientes (con gráfica)
    if ("estados" in pregunta_l and "clientes" in pregunta_l and ("más" in pregunta_l or "top" in pregunta_l)):
        if 'estado' in clientes.columns:
            conteo = clientes.groupby('estado').size().reset_index(name='cantidad').sort_values('cantidad', ascending=False).head(5)
            st.success("Top 5 estados con más clientes:")
            st.dataframe(conteo)
            if any(x in pregunta_l for x in ["grafica", "gráfica", "plot", "barras"]):
                fig, ax = plt.subplots()
                conteo.plot(kind='bar', x='estado', y='cantidad', ax=ax, legend=False)
                plt.ylabel("Clientes")
                plt.xlabel("Estado")
                plt.title("Top 5 estados con más clientes")
                st.pyplot(fig)
        else:
            st.warning("No hay columna 'estado' para calcular el top de clientes.")
        return "Top 5 estados con más clientes mostrado arriba."

    # Ejemplo 5: Propiedades por propietario (gráfica de pastel)
    if ("propiedades" in pregunta_l and "propietario" in pregunta_l and ("pastel" in pregunta_l or "pie" in pregunta_l)):
        if 'propietarioid' in propiedades.columns:
            conteo = propiedades.groupby('propietarioid').size().reset_index(name='cantidad')
            st.success("Propiedades por propietario:")
            st.dataframe(conteo)
            fig, ax = plt.subplots()
            ax.pie(conteo['cantidad'], labels=conteo['propietarioid'], autopct='%1.1f%%')
            plt.title("Distribución de propiedades por propietario")
            st.pyplot(fig)
        else:
            st.warning("No hay columna 'propietarioid' para calcular la gráfica.")
        return "Propiedades por propietario mostrado arriba."

    # Ejemplo 6: Predicción de clientes al cierre del año (con gráfica)
    if ("predic" in pregunta_l or "proye" in pregunta_l or "cierre" in pregunta_l) and "cliente" in pregunta_l:
        if 'created' in clientes.columns:
            clientes['anio'] = clientes['created'].dt.year
            clientes['mes'] = clientes['created'].dt.month
            df = clientes.groupby(['anio', 'mes']).size().reset_index(name='cantidad')
            anio_actual = pd.Timestamp.now().year
            df = df[df['anio'] == anio_actual]
            X = df['mes'].values.reshape(-1, 1)
            y = df['cantidad'].values
            if len(X) > 1:
                model = LinearRegression()
                model.fit(X, y)
                meses_futuros = np.arange(df['mes'].max()+1, 13+1).reshape(-1, 1)
                prediccion = model.predict(meses_futuros)
                total_predicho = int(y.sum() + prediccion.sum())
                st.success(f"Predicción de clientes al cierre del año: {total_predicho}")
                # Gráfica
                fig, ax = plt.subplots()
                ax.bar(df['mes'], y, label="Clientes reales")
                ax.bar(meses_futuros.flatten(), prediccion, color='orange', alpha=0.5, label="Predicción")
                plt.xlabel("Mes")
                plt.ylabel("Clientes")
                plt.title("Predicción de clientes al cierre del año")
                plt.legend()
                st.pyplot(fig)
            else:
                st.warning("No hay suficientes datos para predecir.")
        else:
            st.warning("No hay columna 'created' para calcular la predicción.")
        return "Predicción de clientes al cierre del año mostrada arriba."

    # Ejemplo 7: Mapa de propiedades/rentas usando columna 'googlemaps'
    if ("mapa" in pregunta_l or "ubicacion" in pregunta_l or "ubicación" in pregunta_l or "puntos" in pregunta_l) and ("propiedad" in pregunta_l or "renta" in pregunta_l):
        def extraer_lat_lon(valor):
            try:
                if isinstance(valor, str) and "," in valor and "iframe" not in valor and "http" not in valor:
                    lat, lon = valor.split(",")
                    return float(lat), float(lon)
            except:
                return None, None
            return None, None

        if 'googlemaps' in propiedades.columns:
            coords = propiedades['googlemaps'].apply(extraer_lat_lon)
            df_coords = pd.DataFrame(coords.tolist(), columns=["lat", "lon"])
            df_coords = df_coords.dropna()
            if not df_coords.empty:
                st.success("Mapa de ubicaciones de propiedades/rentas:")
                st.map(df_coords)
                return "Mapa de ubicaciones mostrado arriba."
            else:
                st.warning("No se encontraron coordenadas válidas en los datos de propiedades.")
                return "No se encontraron coordenadas válidas en los datos de propiedades."
        else:
            st.warning("No se encontró la columna 'googlemaps' en los datos de propiedades.")
            return "No se encontró la columna 'googlemaps' en los datos de propiedades."

    # Ejemplo 8: Propietario con más m2 de terreno
    if ("propietario" in pregunta_l and ("más" in pregunta_l or "mayor" in pregunta_l) and ("m2" in pregunta_l or "terreno" in pregunta_l)):
        if 'propietarioid' in propiedades.columns and 'm2terreno' in propiedades.columns:
            propiedades['m2terreno'] = pd.to_numeric(propiedades['m2terreno'], errors='coerce')
            resumen = propiedades.groupby('propietarioid')['m2terreno'].sum().reset_index()
            resumen = resumen.sort_values('m2terreno', ascending=False)
            top = resumen.iloc[0]
            st.success(f"El propietario con más m2 de terreno es: {top['propietarioid']} con {top['m2terreno']:.2f} m2.")
            st.dataframe(resumen)
            return f"El propietario con más m2 de terreno es: {top['propietarioid']} con {top['m2terreno']:.2f} m2."
        else:
            st.warning("No se encontraron las columnas necesarias ('propietarioid' y 'm2terreno').")
            return "No se encontraron las columnas necesarias ('propietarioid' y 'm2terreno')."

    # Ejemplo 9: Propietario con más propiedades
    if ("propietario" in pregunta_l and ("más" in pregunta_l or "mayor" in pregunta_l) and "propiedad" in pregunta_l):
        if 'propietarioid' in propiedades.columns:
            conteo = propiedades.groupby('propietarioid').size().reset_index(name='cantidad')
            conteo = conteo.sort_values('cantidad', ascending=False)
            top = conteo.iloc[0]
            st.success(f"El propietario con más propiedades es: {top['propietarioid']} con {top['cantidad']} propiedades.")
            st.dataframe(conteo)
            return f"El propietario con más propiedades es: {top['propietarioid']} con {top['cantidad']} propiedades."
        else:
            st.warning("No se encontró la columna 'propietarioid'.")
            return "No se encontró la columna 'propietarioid'."

    # Ejemplo 10: Estado con más m2 de construcción
    if ("estado" in pregunta_l and ("más" in pregunta_l or "mayor" in pregunta_l) and ("m2" in pregunta_l or "construccion" in pregunta_l)):
        if 'estado' in propiedades.columns and 'm2construccion' in propiedades.columns:
            propiedades['m2construccion'] = pd.to_numeric(propiedades['m2construccion'], errors='coerce')
            resumen = propiedades.groupby('estado')['m2construccion'].sum().reset_index()
            resumen = resumen.sort_values('m2construccion', ascending=False)
            top = resumen.iloc[0]
            st.success(f"El estado con más m2 de construcción es: {top['estado']} con {top['m2construccion']:.2f} m2.")
            st.dataframe(resumen)
            return f"El estado con más m2 de construcción es: {top['estado']} con {top['m2construccion']:.2f} m2."
        else:
            st.warning("No se encontraron las columnas necesarias ('estado' y 'm2construccion').")
            return "No se encontraron las columnas necesarias ('estado' y 'm2construccion')."

    # Ejemplo 11: Clientes registrados por mes este año (gráfica)
    if ("clientes" in pregunta_l and ("tendencia" in pregunta_l or "evolucion" in pregunta_l or "evolución" in pregunta_l or "mes" in pregunta_l)):
        if 'created' in clientes.columns:
            clientes['anio'] = clientes['created'].dt.year
            clientes['mes'] = clientes['created'].dt.month
            anio_actual = pd.Timestamp.now().year
            df = clientes[clientes['anio'] == anio_actual]
            conteo = df.groupby('mes').size().reset_index(name='cantidad')
            st.success(f"Tendencia de registros de clientes por mes en {anio_actual}:")
            st.dataframe(conteo)
            fig, ax = plt.subplots()
            conteo.plot(kind='bar', x='mes', y='cantidad', ax=ax, legend=False)
            plt.ylabel("Clientes")
            plt.xlabel("Mes")
            plt.title(f"Tendencia de registros de clientes por mes en {anio_actual}")
            st.pyplot(fig)
            return f"Tendencia de registros de clientes por mes en {anio_actual} mostrada arriba."
        else:
            st.warning("No hay columna 'created' para calcular la tendencia por mes.")
            return "No hay columna 'created' para calcular la tendencia por mes."

    return None

# --- Interfaz de usuario tipo chat ---
st.sidebar.header("Opciones")
st.sidebar.write("Puedes cargar nuevos archivos si lo deseas.")

# Input de usuario
with st.form(key="chat_form", clear_on_submit=True):
    pregunta = st.text_input("Escribe tu pregunta:", key="input_pregunta")
    enviar = st.form_submit_button("Enviar")

if enviar and pregunta:
    st.session_state.chat_history.append({"role": "user", "content": pregunta})
    with st.spinner("Pensando..."):
        # Si la pregunta es de mapa, usa solo el fallback para evitar error de PandasAI con folium
        if any(x in pregunta.lower() for x in ["mapa", "ubicacion", "ubicación", "puntos"]):
            fallback = fallback_respuesta(pregunta, clientes, propiedades)
            if fallback:
                st.session_state.chat_history.append({"role": "bot", "content": fallback})
            else:
                st.session_state.chat_history.append({"role": "bot", "content": "No se pudo mostrar el mapa."})
        else:
            try:
                if "propiedad" in pregunta.lower() or "predial" in pregunta.lower():
                    respuesta = sdf_propiedades.chat(pregunta)
                else:
                    respuesta = sdf_clientes.chat(pregunta)
                # Si PandasAI no responde o da error, usa el fallback
                if not respuesta or "No code found" in str(respuesta):
                    fallback = fallback_respuesta(pregunta, clientes, propiedades)
                    if fallback:
                        st.session_state.chat_history.append({"role": "bot", "content": fallback})
                    else:
                        st.session_state.chat_history.append({"role": "bot", "content": "No se pudo responder la pregunta."})
                else:
                    st.session_state.chat_history.append({"role": "bot", "content": str(respuesta)})
            except Exception as e:
                fallback = fallback_respuesta(pregunta, clientes, propiedades)
                if fallback:
                    st.session_state.chat_history.append({"role": "bot", "content": fallback})
                else:
                    st.session_state.chat_history.append({"role": "bot", "content": f"Error: {e}"})

# Mostrar historial tipo chat (después de procesar la pregunta)
chat_placeholder = st.container()
with chat_placeholder:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(
                f"""
                <div style='background-color:#DCF8C6; border-radius:10px; padding:10px; margin-bottom:5px; text-align:right;'>
                    <b>🧑‍💼 Tú:</b> {chat['content']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                f"""
                <div style='background-color:#F1F0F0; border-radius:10px; padding:10px; margin-bottom:5px; text-align:left;'>
                    <b>🤖 Bot:</b> {chat['content']}
                </div>
                """, unsafe_allow_html=True)

# --- Visualización de datos ---
with st.expander("Ver datos de clientes"):
    st.dataframe(clientes.head(20))
with st.expander("Ver datos de propiedades"):
    st.dataframe(propiedades.head(20))