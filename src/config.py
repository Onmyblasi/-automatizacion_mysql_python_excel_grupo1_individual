import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables desde el archivo .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Configuración de Base de Datos
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# --- NUEVAS VARIABLES QUE PIDE MAIN.PY ---

# Nombre del archivo Excel final (asegúrate de que la carpeta 'dashboard' exista)
EXCEL_FILE = "dashboard/dashboard_sakila.xlsx"

# ¿Quieres que se abra el Excel automáticamente al terminar? (True/False)
# Lo lee del .env, si no existe usa 'True' por defecto
AUTO_OPEN_EXCEL = os.getenv("AUTO_OPEN_EXCEL", "True").lower() == "true"

# Carpeta donde se guardarán los CSV generados
OUTPUT_FOLDER = "output"