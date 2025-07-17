import os

class GeneralesLibrerias():

    @staticmethod
    def crear_carpeta(ruta: str):
        extensiones_archivo = ['.txt', '.pdf', '.docx','.xls', '.xlsx', '.png', '.jpg', '.jpeg', '.zip', '.tar.gz', '.py', '.csv', '.json', '.xml', '.html', '.css', '.js', ".log"]

        es_archivo = any(ruta.endswith(ext) for ext in extensiones_archivo)
        if es_archivo:
            # Extraer la ruta del directorio que contiene el archivo
            folder_path = os.path.dirname(ruta)
        else:
            # Si la ruta no existe, crearla como directorio
            folder_path = ruta
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"carpeta '{folder_path}' creada")