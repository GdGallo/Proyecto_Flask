from dotenv import load_dotenv
import os

load_dotenv()  # Cargar las variables del archivo .env
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError('La clave API no está asignada.')
