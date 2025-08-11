# Diccionarios y listas
ESTADOS_VALIDOS = {
    "aguascalientes", "baja california", "baja california sur", "campeche", "chiapas", "chihuahua",
    "ciudad de mexico", "coahuila", "colima", "durango", "guanajuato", "guerrero", "hidalgo",
    "jalisco", "mexico", "michoacan", "morelos", "nayarit", "nuevo leon", "oaxaca", "puebla",
    "queretaro", "quintana roo", "san luis potosi", "sinaloa", "sonora", "tabasco", "tamaulipas",
    "tlaxcala", "veracruz", "yucatan", "zacatecas",
    "estados unidos", "brasil", "california", "texas", "atlanta"
}

MUNICIPIO_A_ESTADO = {
    "morelia": "michoacan",
    "culiacan": "sinaloa",
    "guadalajara": "jalisco",
    "monterrey": "nuevo leon",
    "durango": "durango",
    "celaya": "guanajuato",
    "patzcuaro": "michoacan",
    "uruapan": "michoacan",
    "zapopan": "jalisco",
    "san pedro garza garcia": "nuevo leon",
    "benito juarez": "ciudad de mexico",
    "miguel hidalgo": "ciudad de mexico",
    "cuauhtemoc": "ciudad de mexico",
    "azcapotzalco": "ciudad de mexico",
    "tlalpan": "ciudad de mexico",
    "alvaro obregon": "ciudad de mexico",
    "iztapalapa": "ciudad de mexico",
    "tlalnepantla": "mexico",
    "atlacomulco": "mexico",
    "ecatepec": "mexico",
    "naucalpan": "mexico",
    "tijuana": "baja california",
    "matamoros": "tamaulipas",
    "villa de reyes": "san luis potosi",
    "acapulco": "guerrero",
    "hermosillo": "sonora",
    "san luis potosi": "san luis potosi",
    "toluca": "mexico",
    "ensenda": "baja california",
    "progreso": "yucatan",
    "juriquilla": "queretaro",
}

ESTADO_VARIANTE_A_ESTADO = {
    "df": "ciudad de mexico",
    "d.f.": "ciudad de mexico",
    "distrito federal": "ciudad de mexico",
    "cdmx": "ciudad de mexico",
    "mexico df": "mexico",
    "mexico, d.f.": "ciudad de mexico",
    "edo de mexico": "mexico",
    "edo. de mexico": "mexico",
    "estado de mexico": "mexico",
    "michoacan de ocampo": "michoacan",
    "michoacan": "michoacan",
    "michocacan": "michoacan",
    "michacan": "michoacan",
    "michoacÃn de ocampo": "michoacan",
    "michoacÃ¡n de ocampo": "michoacan",
    "michoacÃ¡n": "michoacan",
    "mexico": "mexico",
    "lazaro cardenas": "michoacan",
    "tepotzotlan": "mexico",
    "monterrey": "nuevo leon",
    "ciidad de mexico": "ciudad de mexico",
    "maxico distrito federal": "ciudad de mexico",
    "m": "",
    "mi": "",
    "prueba": "",
    "estado de prueba": "",
    "estado_prueba": "",
    "rger": "",
    "0": "",
    "nan": "",
    "mÃ©xico distrito federal": "ciudad de mexico",
    "estado de  mexico": "mexico",
    "coronado california": "",
}

CLIENTES_TO_SHOW = [
    'id', 'rfc','tipo','razonsocial','calle','ext','interior','colonia', 'municipio','estado','cp',
    'contactonombre','contactoapaterno','contactoamaterno','contactotelefono', 'contactocelular','created'
]
PROPIEDADES_TO_SHOW = [
    'propietarioid', 'tipopropietario','nombre','alias','nopredial','calle','ext','interior','colonia',
    'municipio','estado','cp','tipopredio','m2terreno','m2construccion','enventa', 'enfideicomiso',
    'otroEstado','googlemaps','created'
]
