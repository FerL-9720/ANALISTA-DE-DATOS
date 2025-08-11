
# PRADOS GPT - Chatbot Inteligente para Datos Inmobiliarios

Bienvenido a **PRADOS GPT**, un asistente conversacional que utiliza inteligencia artificial para analizar, visualizar y responder preguntas sobre tus datos de clientes y propiedades inmobiliarias. Este proyecto está construido con **Streamlit**, **PandasAI** y **OpenAI GPT-4**, permitiendo consultas naturales, generación de gráficas, mapas y predicciones automáticas.

---

## Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Ejemplos de Preguntas](#ejemplos-de-preguntas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Detalles Técnicos](#detalles-técnicos)
- [Personalización](#personalización)
- [Preguntas Frecuentes](#preguntas-frecuentes)
- [Créditos](#créditos)

---

## Características

- **Chatbot conversacional**: Pregunta en lenguaje natural sobre tus datos.
- **Visualización automática**: Gráficas de barras, pastel y mapas interactivos.
- **Predicciones**: Proyección de tendencias usando regresión lineal.
- **Integración con OpenAI GPT-4**: Respuestas inteligentes y análisis avanzado.
- **Carga dinámica de datos**: Soporta archivos Excel filtrados de clientes y propiedades.
- **Interfaz moderna**: Basada en Streamlit, fácil de usar y personalizar.

---

## Instalación

1. **Clona o descarga este repositorio** en tu computadora.
2. **Instala las dependencias** necesarias ejecutando en tu terminal (PowerShell en Windows):

   ```powershell
   pip install streamlit pandas pandasai openai scikit-learn matplotlib numpy
   ```

3. **Coloca tus archivos Excel** filtrados en la carpeta `FILES` (ver configuración).

---

## Configuración

Edita el archivo `config.py` para definir:

- Tu clave de OpenAI (`OPENAI_API_KEY`)
- Rutas de los archivos de clientes y propiedades (`CLIENTES_FILE`, `PROPIEDADES_FILE`)
- Columnas a mostrar en la interfaz

Ejemplo:

```python
OPENAI_API_KEY = "tu_clave_openai"
CLIENTES_FILE = r'c:\ruta\a\clientes_filtrados.xlsx'
PROPIEDADES_FILE = r'c:\ruta\a\propiedades_filtradas.xlsx'
```

---

## Ejecución

Para iniciar el chatbot, ejecuta:

```powershell
streamlit run app.py
```

Se abrirá una interfaz web donde podrás escribir preguntas y visualizar respuestas, gráficas y mapas.

---

## Ejemplos de Preguntas

Puedes preguntar cosas como:

- ¿Cuántos clientes fueron registrados en 2014?
- ¿Cuál es el promedio de m2 de construcción por estado?
- ¿En qué año hubo más registros de clientes?
- ¿Gráfica de propiedades en venta por estado?
- Top 5 estados con más clientes y su gráfica de barras
- ¿Cuántas propiedades tiene cada propietario? (y gráfica de pastel)
- ¿Cuál es la tendencia de registros de clientes por mes este año? (y gráfica)
- ¿Cuál es la proyección de clientes para el cierre de este año si sigue la tendencia actual? (y gráfica)
- ¿Puedes mostrarme un mapa de las propiedades?
- ¿Quién es el propietario con más m2 de terreno?
- ¿Quién tiene más propiedades?
- ¿Cuál es el estado con más m2 de construcción?

---

## Estructura del Proyecto

- `app.py`: Interfaz principal y lógica de chat.
- `ui.py`: Interfaz Streamlit y visualización de datos.
- `datos.py`: Carga, limpieza y preprocesamiento de datos.
- `preguntas.py`: Lógica de preguntas, integración con PandasAI y OpenAI.
- `config.py`: Configuración de claves, rutas y columnas.
- `charts/`: Carpeta donde se guardan las gráficas generadas.
- `FILES/`: Carpeta donde debes colocar tus archivos Excel filtrados.

---

## Detalles Técnicos

- **Streamlit**: Framework para crear interfaces web interactivas en Python.
- **PandasAI**: Permite consultas en lenguaje natural sobre DataFrames.
- **OpenAI GPT-4**: Motor de IA para respuestas avanzadas.
- **scikit-learn**: Usado para regresión lineal en predicciones.
- **matplotlib/numpy**: Para generación de gráficas.

El sistema incluye lógica de fallback para responder preguntas comunes y generar visualizaciones incluso si la IA no responde.

---

## Personalización

Puedes modificar los archivos de configuración y las funciones en `preguntas.py` para adaptar el chatbot a tus necesidades, agregar nuevas visualizaciones, columnas o tipos de análisis.

---

## Preguntas Frecuentes

**¿Qué pasa si cambio el formato de mis archivos Excel?**
- Asegúrate de que las columnas principales estén presentes y actualiza `config.py` si es necesario.

**¿Puedo usar otro modelo de OpenAI?**
- Sí, modifica el parámetro `model` en la configuración de OpenAI.

**¿Dónde se guardan las gráficas?**
- En la carpeta `charts/` dentro del proyecto.

---

## Créditos

Desarrollado por **Sistemas Arquimo**.

---

¿Tienes dudas o quieres mejorar el chatbot? ¡Modifica el código y experimenta!
