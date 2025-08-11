from config import ESTADOS_VALIDOS, MUNICIPIO_A_ESTADO, ESTADO_VARIANTE_A_ESTADO
from limpieza import limpiar_texto

def estado_o_municipio(valor):
    val = limpiar_texto(valor)
    if val in ESTADO_VARIANTE_A_ESTADO:
        return ESTADO_VARIANTE_A_ESTADO[val]
    elif val in ESTADOS_VALIDOS:
        return val
    elif val in MUNICIPIO_A_ESTADO:
        print(f"Municipio detectado en columna estado: '{valor}' -> Se cambia por estado '{MUNICIPIO_A_ESTADO[val]}'")
        return MUNICIPIO_A_ESTADO[val]
    else:
        print(f"Valor NO identificado como estado ni municipio: '{valor}'")
        return f"no identificado ({valor})" if valor else "no identificado"

def detecta_variantes_nuevas(df, col):
    variantes = []
    for idx, val in df[col].dropna().items():
        val_limpio = limpiar_texto(val)
        if (val_limpio not in ESTADOS_VALIDOS and
            val_limpio not in MUNICIPIO_A_ESTADO and
            val_limpio not in ESTADO_VARIANTE_A_ESTADO and
            val_limpio != ""):
            variantes.append((idx, val))
    return variantes

def filtra_y_corrige_estados(df, col, id_col):
    df[col + '_original'] = df[col]
    df[col] = df.apply(lambda row: estado_o_municipio(row[col]), axis=1)
    variantes = detecta_variantes_nuevas(df, col)
    if variantes:
        print(f"\n--- Registros NO identificados en columna '{col}' ---")
        for idx, val in variantes:
            print(f"ID: {df.at[idx, id_col] if id_col in df.columns else idx} | Valor original: '{val}' | Normalizado: '{df.at[idx, col]}'")
        print("--- Fin de registros no identificados ---\n")
    else:
        print(f"No se detectaron variantes nuevas de estados o municipios en '{col}'.")
    return df