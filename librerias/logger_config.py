import logging
from datetime import datetime
import os

def get_logger(name: str = __name__):
    # Directorio base (la carpeta donde está este archivo)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta a la carpeta 'logs' un nivel arriba
    log_dir = os.path.abspath(os.path.join(base_dir, '..', 'logs'))
    os.makedirs(log_dir, exist_ok=True)

    # Nombre único para cada ejecución
    log_filename = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
    log_file = os.path.join(log_dir, log_filename)

    logger = logging.getLogger(name)

    # Evitar duplicación de handlers
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Handler para archivo
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # (Opcional) También imprimir en consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.info(f"📄 Logger inicializado. Archivo: {log_file}")

    return logger