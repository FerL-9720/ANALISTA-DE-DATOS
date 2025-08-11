OPENAI_API_KEY = "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"  # Reemplaza con tu clave real
CLIENTES_FILE = r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\clientes_filtrados.xlsx'
PROPIEDADES_FILE = r'c:\Users\Sistemas Arquimo\Documents\THRON\RENTAS\FILES\propiedades_filtradas.xlsx'
CLIENTES_TO_SHOW = [
    'id', 'rfc','tipo','razonsocial','calle','ext','interior','colonia', 'municipio','estado','cp',
    'contactonombre','contactoapaterno','contactoamaterno','contactotelefono', 'contactocelular','created'
]
PROPIEDADES_TO_SHOW = [
    'propietarioid', 'tipopropietario','nombre','alias','nopredial','calle','ext','interior','colonia',
    'municipio','estado','cp','tipopredio','m2terreno','m2construccion','enventa', 'enfideicomiso',
    'otroEstado','googlemaps','created'
]