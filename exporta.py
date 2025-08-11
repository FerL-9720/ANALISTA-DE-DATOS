def exporta_excel(df, cols, filename):
    df[cols].to_excel(filename, index=False)
    print(f"Archivo exportado: {filename}")