import pandas as pd
from config import CLIENTES_TO_SHOW, PROPIEDADES_TO_SHOW
from estados import filtra_y_corrige_estados
from exporta import exporta_excel
from utils_filtrado import (
    log_nuevos_clientes, log_nuevas_propiedades,
    eliminar_pruebas, leer_ids_guardados, guardar_ids
)
from transformaciones import transformar_propiedades, transformar_clientes

def main():
    print("Cargando datos de clientes y propiedades...")
    clientes = pd.read_csv(r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\clientes.csv', on_bad_lines='skip', encoding='utf-8')
    propiedades = pd.read_csv(r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\propiedades.csv', on_bad_lines='skip', encoding='utf-8')
    clientes.columns = clientes.columns.str.replace('`', '')

    path_clientes_ids = 'clientes_ids.txt'
    path_propiedades_ids = 'propiedades_ids.txt'
    ids_clientes_previos = leer_ids_guardados(path_clientes_ids)
    ids_propiedades_previos = leer_ids_guardados(path_propiedades_ids)

    ids_clientes_actuales = set(str(row['id']) for idx, row in clientes.iterrows() if 'id' in row)
    ids_propiedades_actuales = set(str(row['propietarioid']) for idx, row in propiedades.iterrows() if 'propietarioid' in row)

    nuevos_clientes = ids_clientes_actuales - ids_clientes_previos
    nuevos_propiedades = ids_propiedades_actuales - ids_propiedades_previos

    log_nuevos_clientes(nuevos_clientes)
    log_nuevas_propiedades(nuevos_propiedades)

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

    guardar_ids(path_clientes_ids, ids_clientes_actuales)
    guardar_ids(path_propiedades_ids, ids_propiedades_actuales)

    exporta_excel(clientes, CLIENTES_TO_SHOW, r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\clientes_filtrados.xlsx')
    exporta_excel(propiedades, PROPIEDADES_TO_SHOW, r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\propiedades_filtradas.xlsx')

if __name__ == "__main__":
    main()