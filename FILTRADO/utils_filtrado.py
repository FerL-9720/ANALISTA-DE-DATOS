# utils_filtrado.py

import logging
import os
from datetime import datetime

logging.basicConfig(filename='filtrado.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_nuevos_clientes(ids):
    if ids:
        logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Nuevos clientes agregados ({len(ids)}): {sorted(list(ids))}")

def log_nuevas_propiedades(ids):
    if ids:
        logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Nuevas propiedades agregadas ({len(ids)}): {sorted(list(ids))}")

def eliminar_pruebas(df):
    cols_prueba = [col for col in df.columns if "prueba" in col.lower()]
    df = df.drop(columns=cols_prueba)
    df = df[~df.apply(lambda row: row.astype(str).str.lower().str.contains("prueba").any(), axis=1)]
    return df

def leer_ids_guardados(path):
    if not os.path.exists(path):
        return set()
    with open(path, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def guardar_ids(path, ids):
    with open(path, 'w', encoding='utf-8') as f:
        for id_ in ids:
            f.write(str(id_) + '\n')