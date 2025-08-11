import pandas as pd
from config import CLIENTES_TO_SHOW, PROPIEDADES_TO_SHOW
from estados import filtra_y_corrige_estados
from exporta import exporta_excel
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

def notificar_ventana(titulo, mensaje):
    pass  # Eliminada la ventana emergente

def eliminar_pruebas(df):
    # Elimina columnas cuyo nombre contiene "prueba"
    cols_prueba = [col for col in df.columns if "prueba" in col.lower()]
    df = df.drop(columns=cols_prueba)
    # Elimina filas donde cualquier valor contiene "prueba" (case-insensitive)
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

def transformar_propiedades(df):
    if 'enventa' in df.columns:
        df['enventa'] = df['enventa'].map({0: 'NO ESTÁ EN VENTA', 1: 'EN VENTA'}).fillna('DESCONOCIDO')
    if 'enfideicomiso' in df.columns:
        df['enfideicomiso'] = df['enfideicomiso'].map({0: 'NO ESTÁ EN FIDEICOMISO', 1: 'EN FIDEICOMISO'}).fillna('DESCONOCIDO')
    OTRO_ESTADO_MAP = {
        0: 'En venta',
        1: 'Fideicomiso',
        2: 'Vendido',
        3: 'En desarrollo',
        4: 'Detenido',
        5: 'En renta',
        6: 'Propio',
        7: 'Fideicomiso Liquidado'
    }
    if 'otroEstado' in df.columns:
        df['otroEstado'] = df['otroEstado'].map(OTRO_ESTADO_MAP).fillna('DESCONOCIDO')
    return df

def transformar_clientes(df):
    TIPO_MAP = {1: 'Física', 2: 'Moral'}
    if 'tipo' in df.columns:
        df['tipo'] = df['tipo'].map(TIPO_MAP).fillna('DESCONOCIDO')
    return df

def main():
    print("Cargando datos de clientes y propiedades...")
    clientes = pd.read_csv(r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\clientes.csv', on_bad_lines='skip', encoding='latin1')
    propiedades = pd.read_csv(r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\propiedades.csv', on_bad_lines='skip', encoding='latin1')
    clientes.columns = clientes.columns.str.replace('`', '')

    # Leer IDs previos
    path_clientes_ids = 'clientes_ids.txt'
    path_propiedades_ids = 'propiedades_ids.txt'
    ids_clientes_previos = leer_ids_guardados(path_clientes_ids)
    ids_propiedades_previos = leer_ids_guardados(path_propiedades_ids)

    # Detectar nuevos clientes y propiedades
    ids_clientes_actuales = set(str(row['id']) for idx, row in clientes.iterrows() if 'id' in row)
    ids_propiedades_actuales = set(str(row['propietarioid']) for idx, row in propiedades.iterrows() if 'propietarioid' in row)

    nuevos_clientes = ids_clientes_actuales - ids_clientes_previos
    nuevos_propiedades = ids_propiedades_actuales - ids_propiedades_previos

    # Loguear solo si hay nuevos clientes
    log_nuevos_clientes(nuevos_clientes)

    # Loguear solo si hay nuevas propiedades
    log_nuevas_propiedades(nuevos_propiedades)

    # Elimina columnas y filas de prueba
    clientes = eliminar_pruebas(clientes)
    propiedades = eliminar_pruebas(propiedades)

    clientes = filtra_y_corrige_estados(clientes, 'estado', 'id')
    propiedades = filtra_y_corrige_estados(propiedades, 'estado', 'propietarioid')
    propiedades = propiedades[propiedades['propietarioid'].isin([1, 2, 3, 5])]

    if 'created' in clientes.columns:
        clientes['created'] = pd.to_datetime(clientes['created'], errors='coerce').dt.strftime('%Y-%m-%d')
    if 'created' in propiedades.columns:
        propiedades['created'] = pd.to_datetime(propiedades['created'], errors='coerce').dt.strftime('%Y-%m-%d')

    clientes = transformar_clientes(clientes)
    propiedades = transformar_propiedades(propiedades)

    # Ya no se loguean detalles individuales, solo el resumen arriba

    # Actualizar archivos de IDs
    guardar_ids(path_clientes_ids, ids_clientes_actuales)
    guardar_ids(path_propiedades_ids, ids_propiedades_actuales)

    exporta_excel(clientes, CLIENTES_TO_SHOW, r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\clientes_filtrados.xlsx')
    exporta_excel(propiedades, PROPIEDADES_TO_SHOW, r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\propiedades_filtradas.xlsx')

if __name__ == "__main__":
    main()