
# Guía **profundizada**: Entender el *Concentrado Rentas* y migrarlo a un **Data Warehouse en SQL Server**  
**Fecha:** 2025-08-13

> Esta guía explica con máximo detalle cómo **leer**, **estudiar** y **analizar** el Concentrado Rentas (incluyendo el módulo **Fotovoltaico**) y cómo **diseñar** y **automatizar** su migración hacia un **Data Warehouse (DW)** en **Microsoft SQL Server**, con **diagramas Mermaid**, scripts **T‑SQL**, y **pipelines en Python** con programación a las **06:00** y **15:00**.

---

## Tabla de contenido
- [Parte I. Cómo entender el Concentrado](#parte-i-cómo-entender-el-concentrado)
  - [1. Mapa mental del dominio](#1-mapa-mental-del-dominio)
  - [2. Glosario mínimo](#2-glosario-mínimo)
  - [3. Entidades y relaciones](#3-entidades-y-relaciones)
  - [4. Flujo de negocio extremo a extremo](#4-flujo-de-negocio-extremo-a-extremo)
  - [5. Checklist de estudio y calidad de datos](#5-checklist-de-estudio-y-calidad-de-datos)
- [Parte II. Diseño del Data Warehouse](#parte-ii-diseño-del-data-warehouse)
  - [6. Modelo dimensional (estrella)](#6-modelo-dimensional-estrella)
  - [7. Mapeo Origen → DW](#7-mapeo-origen--dw)
  - [8. DDL base y patrones SCD](#8-ddl-base-y-patrones-scd)
- [Parte III. Proceso ETL/ELT](#parte-iii-proceso-etlelt)
  - [9. Staging, limpieza y normalización](#9-staging-limpieza-y-normalización)
  - [10. Cargas iniciales e incrementales](#10-cargas-iniciales-e-incrementales)
  - [11. Gobierno de datos y pruebas](#11-gobierno-de-datos-y-pruebas)
- [Parte IV. Automatización con Python](#parte-iv-automatización-con-python)
  - [12. Opciones de programación (cron, Task Scheduler, APScheduler)](#12-opciones-de-programación-cron-task-scheduler-apscheduler)
  - [13. Pipeline Python ejemplo (incremental por watermark)](#13-pipeline-python-ejemplo-incremental-por-watermark)
  - [14. Programar la extracción a las 06:00 y 15:00](#14-programar-la-extracción-a-las-0600-y-1500)
- [Apéndices](#apéndices)
  - [A. Estructura de repositorio](#a-estructura-de-repositorio)
  - [B. Scripts ejemplo (T-SQL y Python)](#b-scripts-ejemplo-t-sql-y-python)

---

## Parte I. Cómo entender el Concentrado

### 1. Mapa mental del dominio
El **núcleo** del sistema es **Rentas**: por cada contrato (`rentas`) se conectan **Cliente** ↔ **Propietario** ↔ **Propiedad** ↔ **Local**. A partir de allí se generan **Cargos**, luego **Facturas** (con **UUID** CFDI), después **Pagos** (con **Complementos de pago**), y se registran **Notas** de ajuste.  
El módulo **Fotovoltaico** replica ese patrón con sus propias **lecturas**, **cargos**, **facturas/UUID**, **pagos/complementos** y **notas**.

> Esta estructura y nombres de tablas/columnas se observan en el diagrama del PDF.

### 2. Glosario mínimo
- **Renta (Contrato):** vínculo que define quién renta qué local de qué propiedad y a quién se factura/cobra.
- **Cargo:** monto generado por la renta (p. ej., renta mensual). Puede ser base para **facturar**.
- **Factura & UUID:** documento fiscal (CFDI) y su identificador único (`UUID`).
- **Pago & Complemento:** abono recibido y su CFDI de complemento.
- **Nota:** ajuste (p. ej., crédito) sobre factura/pago.
- **FV (Fotovoltaico):** sub‑módulo de energía con lecturas, cargos y documentos propios.

### 3. Entidades y relaciones
A continuación, una lista de **tablas principales** detectadas en el diagrama (nombres/llaves claves tal como aparecen). Completar tipos/longitudes finales con el diccionario real del origen.

- **Clientes y representantes**: `clientes`, `pmoral`, `representantes`, `representantes_clientes`.  
- **Inventario**: `propiedades` (`id_propietario`, `tipo_propietario`), `locales`, `localeslocales` (posible tabla puente/jerarquía).  
- **Contratos**: `rentas` (`id_cliente`, `tipo_cliente`, `propiedad_id`, `local_id`, `id_propietario`, `tipo_propietario`, `tipo_local`).  
- **Cobranza/Facturación**: `rentascargo` (`id_cargo`, `renta_id`), `rentasFacturacionFacturas` (tiene `refIdCargo`), `rentasFacturacionUUID` (liga `id_cargo`, `id_renta`), `rentaspago` (`id_pago`, `id_renta`, `id_cargo`, `complemento`), `rentasPagosComplementos`, `cfdi_complementosPago`, `rentasFacturacionNotas`.  
- **Fotovoltaico**: `rentas_fotovoltaico`, `fotovoltaico_lecturas_pdbt`, `fotovoltaico_cargos`, `fotovoltaico_facturas`, `fotovolt_facturas_uuid`, `facturas_pagos_fotovolt`, `cfdi_complementos_pagos_fotovolt`, `facturas_notas_credito_fotovolt`.

#### 3.1 Diagrama ER (resumen) — *Mermaid*
```mermaid
erDiagram
  CLIENTES ||--o{ RENTAS : "contrata"
  PROPIEDADES ||--o{ LOCALES : "contiene"
  PROPIEDADES ||--o{ RENTAS : "hospeda"
  LOCALES ||--o{ RENTAS : "se_rentan_en"
  RENTAS ||--o{ RENTASCARGO : "genera"
  RENTASCARGO ||--o{ RENTASFACTURAS : "se_factura_en"
  RENTASFACTURAS ||--o{ RENTASUUID : "tiene"
  RENTAS ||--o{ RENTASPAGO : "recibe"
  RENTASPAGO ||--o{ PAGOSCOMPLEMENTOS : "complementa"
  PAGOSCOMPLEMENTOS }o--|| CFDICOMPLEMENTOS : "CFDI"

  RENTASFV ||--o{ FV_LECTURAS : "registra"
  RENTASFV ||--o{ FV_CARGOS : "genera"
  FV_CARGOS ||--o{ FV_FACTURAS : "se_factura_en"
  FV_FACTURAS ||--o{ FV_UUID : "tiene"
  RENTASFV ||--o{ FV_PAGOS : "recibe"
  FV_PAGOS }o--|| FV_CFDI_COMPLEMENTOS : "CFDI"
  FV_FACTURAS ||--o{ FV_NOTAS : "ajustes"

  CLIENTES {
int id_cliente
}
  PROPIEDADES {
int id_propiedad
    int id_propietario
    varchar tipo_propietario
}
  LOCALES {
int id_local
    int id_propiedad
}
  RENTAS {
int id_rentas
    int id_cliente
    int propiedad_id
    int local_id
    int id_propietario
    varchar tipo_propietario
    tinyint tipo_cliente
    varchar tipo_local
}
  RENTASCARGO {
int id_cargo
    int renta_id
}
  RENTASFACTURAS {
int id_factura
    int refIdCargo
    smallint folio
}
  RENTASUUID {
int id_uuid
    int id_prop
    int id_cargo
    int id_renta
}
  RENTASPAGO {
int id_pago
    int id_renta
    int id_cargo
    int complemento
}
  PAGOSCOMPLEMENTOS {
int id
    int id_pago
}
  CFDICOMPLEMENTOS {
int id_complementoPago
    int id_empresa
    int id_factura
}
  RENTASFV {
int id_renta_fotovolt
    int id_propiedad
    int id_local
    int id_cliente
}
  FV_LECTURAS {
int id_lectura
    int id_renta
    int id_cargo
}
  FV_CARGOS {
int id_cargo
    int id_renta_fotovolt
}
  FV_FACTURAS {
int id_factura
    int id_cargo
    int id_cliente
}
  FV_UUID {
int id_uuid
    int id_cargo
    int id_renta_fotovolt
}
  FV_PAGOS {
int id_pago
    int id_renta_fotovolt
    int cargo_id
    int id_complemento
}
  FV_CFDI_COMPLEMENTOS {
int id_complemento
    int id_propietario
    int id_factura
}
  FV_NOTAS {
int id_nota
    int id_propietario
}
```

### 4. Flujo de negocio extremo a extremo
```mermaid
flowchart LR
  A[Contrato RENTA] --> B[Genera CARGOS]
  B --> C[FACTURA + UUID]
  C --> D[PAGO]
  D --> E[COMPLEMENTO de pago]
  C --> F[NOTA (ajuste)]
  
  A2[Contrato FV] --> B2[LECTURAS FV]
  B2 --> C2[CARGOS FV]
  C2 --> D2[FACTURA FV + UUID]
  D2 --> E2[PAGO FV]
  E2 --> F2[COMPLEMENTO FV]
  D2 --> G2[NOTA CRÉDITO FV]
```

### 5. Checklist de estudio y calidad de datos
- **Integridad referencial**: verificar que todo `id_*` de tablas hijas exista en su maestro (rentas, clientes, propiedades, locales).  
- **Orfandad**: cargos sin renta, facturas sin cargo, pagos sin factura/cargo, UUIDs sin factura.  
- **Duplicados**: folio/UUID repetidos; pagos duplicados.  
- **Catálogos**: unificar `tipo_cliente`, `tipo_propietario`, `tipo_local`, estatus (vigente/cancelado).  
- **Fechas**: confirmar columnas de creación/actualización para incrementales.  
- **Reglas de negocio**: ¿un pago puede aplicar a múltiples cargos? Si sí, considerar **tabla puente**.

---

## Parte II. Diseño del Data Warehouse

### 6. Modelo dimensional (estrella)

#### 6.1 Hechos (Facts)
- **FactCargo** (grano: 1 fila por cargo de renta). Métricas: `importe`, `impuestos`, `estatus`.  
- **FactFactura** (grano: 1 por factura). Métricas: totales; **degenerate dimension** para `folio`/`serie` si aplica.  
- **FactPago** (grano: 1 por aplicación de pago o por pago si no hay desglose).  
- **FactRenta** (opcional para KPIs de ocupación/duración).  
- **FactFVLectura**, **FactFVCargo**, **FactFVFactura**, **FactFVPago** (módulo FV).  

#### 6.2 Dimensiones (Dims, con SK y SCD2 donde aplique)
- `DimCliente`, `DimPropietario`, `DimPropiedad`, `DimLocal`, `DimTipoLocal`.  
- `DimTiempo` (compartida por todos los hechos).  
- `DimCFDI/Documento` (serie, folio, tipo, UUID, estatus).  
- `DimEstatus`, `DimFormaPago`/`DimMetodoPago` si están en el origen.

#### 6.3 Diagrama estrella (alto nivel)
```mermaid
flowchart TB
  subgraph Hechos
    FC[FactCargo]
  FF[FactFactura]
  FP[FactPago]
  FR[FactRenta]
  FVL[FactFVLectura]
  FVC[FactFVCargo]
  FVF[FactFVFactura]
  FVP[FactFVPago]
  end
  DCLI[DimCliente]
  DPROPIE[DimPropietario]
  DPROP[DimPropiedad]
  DLOC[DimLocal]
  DTL[DimTipoLocal]
  DTIEMPO[DimTiempo]
  DCFDI[DimCFDI]
  DEST[DimEstatus]

  DCLI --- FC & FF & FP & FR & FVC & FVF & FVP
  DPROPIE --- FC & FF & FP & FR & FVC & FVF & FVP
  DPROP --- FC & FF & FP & FR & FVC & FVF & FVP
  DLOC --- FC & FF & FP & FR & FVC & FVF & FVP
  DTL --- FC & FR
  DTIEMPO --- FC & FF & FP & FR & FVL & FVC & FVF & FVP
  DCFDI --- FF & FP & FVF & FVP
  DEST --- FC & FF & FP & FVC & FVF & FVP
```

### 7. Mapeo Origen → DW
- **`rentascargo` → FactCargo`** (importe, IVA, estatus, `TiempoCargoKey`, SKs a Renta/Cliente/Propiedad/Local/TipoLocal).  
- **`rentasFacturacionFacturas` + `rentasFacturacionUUID` → `FactFactura`** (totales, `folio/serie`, `UUID`).  
- **`rentaspago` + `rentasPagosComplementos` + `cfdi_complementosPago` → `FactPago`** (importe, forma/método si aplica, complemento CFDI).  
- **FV**: `fotovoltaico_lecturas_pdbt` → `FactFVLectura`; `fotovoltaico_cargos` → `FactFVCargo`; `fotovoltaico_facturas` + `fotovolt_facturas_uuid` → `FactFVFactura`; `facturas_pagos_fotovolt` + `cfdi_complementos_pagos_fotovolt` → `FactFVPago`.

### 8. DDL base y patrones SCD

#### 8.1 DimTiempo (semilla de calendario)
```sql
CREATE TABLE dw.DimTiempo (
  TiempoKey INT PRIMARY KEY,     -- YYYYMMDD
  Fecha DATE NOT NULL,
  Anio SMALLINT NOT NULL,
  Mes TINYINT NOT NULL,
  Dia TINYINT NOT NULL,
  Trimestre TINYINT NOT NULL,
  NombreMes NVARCHAR(15) NOT NULL
);
```

#### 8.2 DimCliente (SCD Tipo 2 simplificado)
```sql
CREATE TABLE dw.DimCliente (
  ClienteKey INT IDENTITY PRIMARY KEY,
  IdClienteOrigen INT NOT NULL,
  TipoCliente NVARCHAR(10) NOT NULL, -- Fisica/Moral
  Nombre NVARCHAR(250) NULL,
  RFC NVARCHAR(20) NULL,
  VigenciaInicio DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
  VigenciaFin DATETIME2 NULL,
  EsActual BIT NOT NULL DEFAULT 1
);
```

#### 8.3 FactCargo (hecho)
```sql
CREATE TABLE dw.FactCargo (
  CargoKey BIGINT IDENTITY PRIMARY KEY,
  IdCargoOrigen INT NOT NULL,
  RentaKey INT NOT NULL,
  ClienteKey INT NOT NULL,
  PropiedadKey INT NOT NULL,
  LocalKey INT NOT NULL,
  TiempoCargoKey INT NOT NULL,
  Importe DECIMAL(18,2) NOT NULL,
  IVA DECIMAL(18,2) NULL,
  EstatusKey INT NULL
);
```

#### 8.4 MERGE para SCD2 (ejemplo)
```sql
MERGE dw.DimCliente AS tgt
USING (SELECT IdClienteOrigen, TipoCliente, Nombre, RFC FROM stg.clientes_delta) AS src
ON (tgt.IdClienteOrigen = src.IdClienteOrigen AND tgt.EsActual = 1)
WHEN MATCHED AND (
     ISNULL(tgt.TipoCliente,'') <> ISNULL(src.TipoCliente,'')
  OR ISNULL(tgt.Nombre,'')      <> ISNULL(src.Nombre,'')
  OR ISNULL(tgt.RFC,'')         <> ISNULL(src.RFC,'')
) THEN
  UPDATE SET tgt.EsActual = 0, tgt.VigenciaFin = SYSUTCDATETIME()
WHEN NOT MATCHED BY TARGET THEN
  INSERT (IdClienteOrigen, TipoCliente, Nombre, RFC, VigenciaInicio, EsActual)
  VALUES (src.IdClienteOrigen, src.TipoCliente, src.Nombre, src.RFC, SYSUTCDATETIME(), 1);
```

---

## Parte III. Proceso ETL/ELT

### 9. Staging, limpieza y normalización
1. **Staging (`stg.*`)**: clonar origen **1:1** y registrar `_ExtractedAt`.  
2. **Limpieza**: estandarizar catálogos `tipo_*`, corregir nulos, validar integridad.  
3. **Conformado**: construir `DimTiempo` y catálogos de `Estatus`, `TipoCliente`, `TipoLocal`, etc.  
4. **Llaves**: crear **claves sustitutas (SK)** en dimensiones y resolver **FKs** en hechos.

### 10. Cargas iniciales e incrementales
- **Inicial**: poblar `stg.*` completo y construir dimensiones/primeros hechos.  
- **Incremental por watermark**: guardar, por tabla, la última `id` o `updated_at` procesada.  
- **Idempotencia**: repetir pipeline sin duplicar (usar `MERGE`/`UPSERT` en staging y DW).

#### 10.1 Tabla de marcas (watermarks)
```sql
CREATE SCHEMA etl;
GO
CREATE TABLE etl.Watermarks (
  PipelineName NVARCHAR(100) NOT NULL,
  SourceTable NVARCHAR(128) NOT NULL,
  LastHighWatermark NVARCHAR(64) NOT NULL,
  UpdatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
  PRIMARY KEY (PipelineName, SourceTable)
);
```

---


### 11. Gobierno de datos y pruebas

**Objetivo:** asegurar que la información que ingresa al DW sea **calidad‑confiable**, **trazable** y **reproducible**.

#### 11.1 Gobierno de datos (mínimos viables)
- **Propiedad y responsables**: asigna *Data Owners* por dominio (Rentas, Facturación, Pagos, FV).
- **Diccionario y linaje**: documenta definiciones, reglas de negocio, y el linaje *origen → staging → dim/fact*.
- **Controles de acceso**: lectura/escritura segmentada por esquema (`stg`, `dw`, `bi`); credenciales de solo lectura para analistas.
- **Versionado**: versiona scripts SQL/Python (git) y **versiona datos críticos** (p.ej., snapshots mensuales).

#### 11.2 Pruebas de datos (antes de publicar)
- **Integridad**: claves foráneas simétricas entre `stg` y `dw` (no huérfanos).
- **Unicidad**: `UUID` de CFDI y `id_*` no duplicados.
- **Consistencia temporal**: fechas dentro de ventanas válidas (no en futuro salvo CFDI emitidos). 
- **Reconciliación**: sumas de cargos − notas ≈ facturas emitidas; facturas − pagos ≈ cuentas por cobrar.
- **Pruebas incrementales**: validar que *solo* filas nuevas/cambiadas entren por watermark.

#### 11.3 Monitoreo (operativo)
- **Tablero** de cargas: duración, filas procesadas, filas rechazadas, última ejecución OK/ERROR.
- **Alertas**: email/Teams/Slack cuando fallan cargas o cuando reglas de calidad superan umbrales.
- **Bitácora**: tabla `bi.LogETL` con `job`, `inicio`, `fin`, `estatus`, `filas`, `detalle_error`.

> Resultado: menor riesgo de *drift* de datos, auditorías más rápidas y confianza en los KPIs.

## Parte IV. Automatización con Python

### 12. Opciones de programación (cron, Task Scheduler, APScheduler)
- **Linux/macOS (cron)**: fiable en servidores; ejecuta scripts a horarios fijos.  
- **Windows (Task Scheduler)**: análogo a cron.  
- **APScheduler** (en Python): útil dentro de un servicio, pero para producción recomendamos **orquestar con cron/Task Scheduler** y dejar a Python sólo la lógica de ETL.

### 13. Pipeline Python ejemplo (incremental por watermark)
> Variables de entorno necesarias: `SRC_DB_URL`, `MSSQL_URL`, `ODBC_DRIVER`, etc.

```python
# etl/pipeline.py
import os, logging, sys
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("etl.log")]
)

SRC_DB_URL = os.getenv("SRC_DB_URL")         # p.ej., 'sqlite:///rentals.db' o 'mysql+pymysql://user:pwd@host/db'
MSSQL_URL  = os.getenv("MSSQL_URL")          # p.ej., 'mssql+pyodbc://user:pwd@server/db?driver=ODBC+Driver+17+for+SQL+Server'

eng_src = create_engine(SRC_DB_URL, pool_pre_ping=True)
eng_dw  = create_engine(MSSQL_URL, pool_pre_ping=True)

def get_watermark(pipeline, table):
    with eng_dw.begin() as conn:
        row = conn.execute(text("""
            SELECT LastHighWatermark FROM etl.Watermarks
            WHERE PipelineName=:p AND SourceTable=:t
        """), dict(p=pipeline, t=table)).fetchone()
        return row[0] if row else None

def set_watermark(pipeline, table, value):
    with eng_dw.begin() as conn:
        conn.execute(text("""
            MERGE etl.Watermarks AS tgt
            USING (SELECT :p AS PipelineName, :t AS SourceTable) AS src
            ON (tgt.PipelineName=src.PipelineName AND tgt.SourceTable=src.SourceTable)
            WHEN MATCHED THEN UPDATE SET LastHighWatermark=:v, UpdatedAt=SYSUTCDATETIME()
            WHEN NOT MATCHED THEN INSERT (PipelineName, SourceTable, LastHighWatermark)
                 VALUES (:p, :t, :v);
        """), dict(p=pipeline, t=table, v=str(value)))

def extract_incremental(table, id_col="id_cargo"):
    wm = get_watermark("rentas-etl", table) or "0"
    query = f"SELECT * FROM {table} WHERE {id_col} > :wm ORDER BY {id_col} ASC"
    logging.info(f"Extrayendo {table} con watermark > {wm}")
    df = pd.read_sql(text(query), eng_src, params={{"wm": wm}})
    return df

def upsert_staging(df, stg_table, key_cols):
    if df.empty:
        logging.info(f"Sin nuevos registros para {stg_table}")
        return 0, None
    with eng_dw.begin() as conn:
        tmp = f"##tmp_{stg_table}_{datetime.utcnow().strftime('%H%M%S')}"
        df.to_sql(tmp, conn, if_exists="replace", index=False)
        merge_cols = ", ".join(df.columns)
        on_clause = " AND ".join([f"t.{k}=s.{k}" for k in key_cols])
        set_clause = ", ".join([f"t.{c}=s.{c}" for c in df.columns if c not in key_cols])
        conn.execute(text(f"""
            MERGE stg.{stg_table} AS t
            USING {tmp} AS s
            ON ({on_clause})
            WHEN MATCHED THEN UPDATE SET {set_clause}
            WHEN NOT MATCHED THEN INSERT ({merge_cols}) VALUES ({', '.join([f's.{c}' for c in df.columns])});
        """))
        max_key = df[key_cols[0]].max()
        return len(df), max_key

def load_dim_fact():
    with eng_dw.begin() as conn:
        # Ejemplo simplificado: resolver SKs y poblar hechos desde staging
        conn.execute(text("EXEC dw.usp_Load_DimCliente"))
        conn.execute(text("EXEC dw.usp_Load_FactCargo"))

def main():
    # 1) rentascargo incremental (ajusta id_col si aplica)
    df_cargo = extract_incremental("rentascargo", id_col="id_cargo")
    rows, max_key = upsert_staging(df_cargo, "rentascargo", key_cols=["id_cargo"]) 
    if rows > 0:
        set_watermark("rentas-etl", "rentascargo", max_key)
    # 2) TODO: repetir para facturas, pagos, fv_lecturas, etc.
    load_dim_fact()
    logging.info("OK - ciclo completado")

if __name__ == "__main__":
    main()
```

### 14. Programar la extracción a las 06:00 y 15:00

#### 14.1 Linux/macOS (cron)
1. Edita el crontab del usuario del servicio:
```bash
crontab -e
```
2. Agrega:
```bash
# Ejecuta a las 06:00 y a las 15:00 todos los días
0 6 * * *  /usr/bin/env -S bash -lc 'cd /ruta/al/repo && /usr/bin/env -S bash -lc "export $(grep -v ^# .env | xargs); python3 etl/pipeline.py >> logs/cron.log 2>&1"'
0 15 * * * /usr/bin/env -S bash -lc 'cd /ruta/al/repo && /usr/bin/env -S bash -lc "export $(grep -v ^# .env | xargs); python3 etl/pipeline.py >> logs/cron.log 2>&1"'
```

#### 14.2 Windows (Task Scheduler)
```bat
:: Crear tarea que corre diario a las 06:00
schtasks /Create /SC DAILY /ST 06:00 /TN "ETL-Rentas-06" /TR "cmd /c cd C:\ruta\al\repo && setx -m $(type .env) && py etl\pipeline.py"
:: Crear tarea que corre diario a las 15:00
schtasks /Create /SC DAILY /ST 15:00 /TN "ETL-Rentas-15" /TR "cmd /c cd C:\ruta\al\repo && setx -m $(type .env) && py etl\pipeline.py"
```

---

## Apéndices

### A. Estructura de repositorio
```
/docs
  └── diccionario_datos.md
/sql
  ├── 01_ddl_dimensiones.sql
  ├── 02_ddl_hechos.sql
  ├── 03_dim_tiempo_seed.sql
  └── 10_cargas_incrementales.sql
/etl
  ├── pipeline.py
  └── usp/
      ├── usp_Load_DimCliente.sql
      └── usp_Load_FactCargo.sql
/logs
.env.example
README.md (este archivo)
```

### B. Scripts ejemplo (T-SQL y Python)
Incluye en `/sql` los DDLs mostrados y procedimientos `usp_*` para **resolver SKs**, ejecutar **MERGE** y poblar hechos. En `/etl/pipeline.py` ajusta **URL de origen/destino** y los nombres de **tablas** y **llaves** según el modelo real.

---

**Fin.**
