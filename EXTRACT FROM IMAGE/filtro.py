import pytesseract
from PIL import Image
import re
import pandas as pd

# Si usas Windows, especifica la ruta de tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import os
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def ocr_image(image_path):
    # Abre la imagen y extrae el texto
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='spa')  # 'spa' para español
    return text

def extract_info(text):
    # Busca nombre, domicilio, celular usando expresiones regulares simples
    nombre = re.search(r'Nombre[:\- ]+([A-Za-záéíóúÁÉÍÓÚ ]+)', text)
    domicilio = re.search(r'Domicilio[:\- ]+([A-Za-z0-9áéíóúÁÉÍÓÚ ,.-]+)', text)
    celular = re.search(r'(?:Celular|Tel[ée]fono)[:\- ]+(\d{10,})', text)

    return {
        'nombre': nombre.group(1) if nombre else None,
        'domicilio': domicilio.group(1) if domicilio else None,
        'celular': celular.group(1) if celular else None
    }

if __name__ == "__main__":
    # Cambia 'factura.jpg' por el nombre de tu imagen
    texto = ocr_image('factura.jpeg')
    print("Texto extraído:")
    print(texto)

    datos = extract_info(texto)
    print("\nDatos encontrados:")
    print(datos)

    # Guardar los datos extraídos en columnas separadas en Excel
    df = pd.DataFrame({
        'Nombre': [datos['nombre']],
        'Domicilio': [datos['domicilio']],
        'Celular': [datos['celular']]
    })
    # Guardar el texto completo en otra hoja del Excel
    with pd.ExcelWriter('resultado.xlsx') as writer:
        df.to_excel(writer, sheet_name='Datos extraídos', index=False)
        pd.DataFrame({'Texto extraído': [texto]}).to_excel(writer, sheet_name='Texto completo', index=False)
    print('\nDatos guardados en resultado.xlsx (cada dato en su columna, texto completo en otra hoja)')