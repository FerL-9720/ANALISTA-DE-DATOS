# THRON Data Cleaning & Normalization

Este proyecto contiene scripts y notebooks para la **limpieza, normalización y exportación profesional de datos** de clientes y propiedades inmobiliarias. Está diseñado para asegurar la calidad, consistencia y utilidad de la información en bases de datos, facilitando su uso en procesos administrativos, comerciales y legales.

---

## Estructura del Proyecto

```
THRON/
│
├── filtro.py           # Script principal: ejecuta la limpieza y exportación de datos
├── config.py           # Diccionarios y listas de estados, municipios y variantes
├── limpieza.py         # Funciones para normalizar y limpiar texto
├── estados.py          # Funciones para filtrar/corregir estados y detectar variantes
├── exporta.py          # Funciones para exportar DataFrames a Excel
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


  # FILTRADO

  Este proyecto está diseñado para el procesamiento de datos de clientes y propiedades en el contexto de rentas, permitiendo filtrar, limpiar, transformar y exportar información relevante. A continuación se detalla la función de cada archivo y el flujo de trabajo recomendado.

  ## Archivos principales y su función

  - **clientes_ids.txt**: Archivo de texto donde se guardan los IDs de clientes procesados. Permite llevar control de los clientes ya filtrados y detectar nuevos.

  - **propiedades_ids.txt**: Archivo de texto donde se guardan los IDs de propiedades procesadas. Permite llevar control de las propiedades ya filtradas y detectar nuevas.

  - **config.py**: Contiene diccionarios y listas de referencia, como estados válidos, variantes de estados y mapeo de municipios a estados. Es la base para la normalización y validación de datos geográficos.

  - **estados.py**: Proporciona funciones para filtrar y corregir los valores de estado y municipio en los DataFrames, detectando variantes y normalizando los datos. Utiliza la configuración definida en `config.py` y funciones de limpieza de texto.

  - **exporta.py**: Permite exportar los DataFrames filtrados y procesados a archivos Excel, seleccionando las columnas relevantes. Incluye mensajes de confirmación para el usuario.

  - **filtro.py**: Script principal que coordina la carga de datos, filtrado de clientes y propiedades, registro de nuevos IDs, limpieza y corrección de estados, transformación de columnas y exportación final. Es el punto de entrada recomendado para el procesamiento completo.

  - **limpieza.py**: Incluye funciones para limpiar y normalizar texto, eliminando acentos, caracteres especiales y espacios innecesarios. Es fundamental para la estandarización previa al filtrado y transformación.

  - **transformaciones.py**: Aplica transformaciones específicas a los DataFrames, como la conversión de valores numéricos a etiquetas legibles (por ejemplo, "EN VENTA", "FIDEICOMISO", "Física", "Moral") y la normalización de estados adicionales.

  - **utils_filtrado.py**: Contiene utilidades para el filtrado, como registro de nuevos clientes y propiedades en logs, eliminación de columnas y registros de prueba, lectura y escritura de archivos de IDs, y funciones auxiliares para el flujo de trabajo.

  - **__pycache__/**: Carpeta generada automáticamente por Python para almacenar archivos compilados. No requiere intervención manual.

  ## Flujo de trabajo recomendado

  1. **Preparar archivos de IDs**: Verifica que `clientes_ids.txt` y `propiedades_ids.txt` estén actualizados o vacíos si es la primera ejecución.
  2. **Configurar parámetros**: Revisa y ajusta los diccionarios y listas en `config.py` según los estados y municipios relevantes para tu caso.
  3. **Ejecutar el filtrado**: Corre `filtro.py` para cargar los datos, filtrar clientes y propiedades, registrar nuevos IDs y limpiar los datos.
  4. **Corrección y normalización**: El script aplicará funciones de `estados.py`, `limpieza.py` y `transformaciones.py` para asegurar que los datos sean consistentes y legibles.
  5. **Exportar resultados**: Utiliza `exporta.py` (llamado desde `filtro.py`) para guardar los resultados en archivos Excel listos para análisis o reporte.

  ## Ejemplo de ejecución

  ```powershell
  # Procesar y exportar datos completos
  python filtro.py
  ```

  ## Requisitos

  - Python 3.10 o superior
  - Paquetes recomendados: pandas, openpyxl (instalar con `pip install pandas openpyxl`)

  ## Detalles adicionales

  - Todos los scripts están diseñados para ejecutarse de forma independiente o en secuencia, pero se recomienda usar `filtro.py` como punto de entrada principal.
  - Los archivos de IDs permiten detectar y registrar nuevos clientes y propiedades automáticamente, facilitando el control de cambios entre ejecuciones.
  - El sistema de logs en `utils_filtrado.py` ayuda a auditar el procesamiento y detectar incidencias o registros nuevos.
  - Puedes adaptar los scripts y configuraciones a tus propios criterios de filtrado, limpieza o exportación según las necesidades del negocio.
  - Si tienes dudas sobre la función de algún archivo, revisa los comentarios en el código fuente o consulta esta documentación.

  ---

  **Autor:** Sistemas Arquimo  
  **Fecha de última actualización:** 11 de agosto de 2025
