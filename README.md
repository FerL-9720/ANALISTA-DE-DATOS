# ANALISTA-DE-DATOS
Paso a paso de como llevar el proceso de análisis de datos hasta la creación de un Chat-GPT con la información ya limpia.

# Data Cleaning & Normalization

Este proyecto contiene scripts y notebooks para la **limpieza, normalización y exportación profesional de datos** de clientes y propiedades inmobiliarias. Está diseñado para asegurar la calidad, consistencia y utilidad de la información en bases de datos, facilitando su uso en procesos administrativos, comerciales y legales.

---

## Estructura del Proyecto

```
THRON/
│
├── filter.py           # Script principal: ejecuta la limpieza y exportación de datos
├── config.py           # Diccionarios y listas de estados, municipios y variantes
├── limpieza.py         # Funciones para normalizar y limpiar texto
├── estados.py          # Funciones para filtrar/corregir estados y detectar variantes
├── exporta.py          # Funciones para exportar DataFrames a Excel
├── CLEANING.ipynb      # Jupyter Notebook para exploración y análisis interactivo
└── README.md           # Documentación del proyecto
```

---

## ¿Qué hace este proyecto?

- **Carga y limpia datos** de clientes y propiedades desde archivos CSV.
- **Normaliza nombres de estados** y municipios, corrigiendo errores comunes, variantes, acentos y abreviaturas.
- **Detecta y reporta valores no identificados** para revisión y mejora continua del diccionario.
- **Exporta los datos limpios** a archivos Excel listos para uso administrativo.
- **Identifica duplicados** y columnas con datos faltantes.
- **Modulariza el código** para facilitar mantenimiento y escalabilidad.

---

## ¿Cómo usarlo?

1. **Coloca tus archivos CSV** en la carpeta `RENTAS` con los nombres `clientes.csv` y `propiedades.csv`.
2. **Configura los diccionarios** en `config.py` si necesitas agregar nuevos estados, municipios o variantes.
3. **Ejecuta el script principal**:

   ```bash
   python filter.py
   ```

   Esto generará los archivos `clientes_filtrados.xlsx` y `propiedades_filtradas.xlsx` con los datos limpios.

4. **Explora y analiza** los datos con el notebook `CLEANING.ipynb` para tareas interactivas y reportes personalizados.

---

## Principales módulos y funciones

- **config.py**  
  Define listas y diccionarios de estados válidos, municipios y variantes para la normalización.

- **limpieza.py**  
  Funciones para limpiar y normalizar texto (acentos, espacios, mayúsculas/minúsculas).

- **estados.py**  
  Funciones para identificar, corregir y reportar estados y municipios en los datos.

- **exporta.py**  
  Funciones para exportar DataFrames a archivos Excel.

- **filter.py**  
  Script principal que coordina la limpieza, corrección, exportación y reportes.

---

## Buenas prácticas implementadas

- **Modularización:** Cada archivo tiene una responsabilidad clara.
- **Normalización robusta:** Corrige acentos, errores de dedo, variantes y municipios.
- **Reportes automáticos:** Imprime en consola los registros no identificados con su ID para fácil revisión.
- **Exportación profesional:** Archivos Excel listos para uso administrativo.
- **Facilidad de mantenimiento:** Solo actualiza los diccionarios para mejorar la limpieza.

---

## Ejemplo de reporte de registros no identificados

Al ejecutar el script, verás en consola:

```
--- Registros NO identificados en columna 'estado' ---
ID: 714 | Valor original: 'houston texas' | Normalizado: 'no identificado (houston texas)'
ID: 715 | Valor original: 'nan' | Normalizado: 'no identificado'
--- Fin de registros no identificados ---
```

Esto te permite identificar rápidamente qué registros requieren revisión manual o actualización de los diccionarios.

---

## Requisitos

- Python 3.8+
- pandas
- unicodedata (incluido en la librería estándar)

Instala dependencias con:

```bash
pip install pandas
```

---

## Contribuciones

Si tienes nuevos estados, municipios o variantes, agrega al diccionario correspondiente en `config.py` y envía tu pull request.

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

---

## Autor

Desarrollado por Sistemas Arquimo para la gestión profesional
