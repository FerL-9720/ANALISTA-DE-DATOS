# transformaciones.py

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