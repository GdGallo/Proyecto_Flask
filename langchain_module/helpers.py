from langchain_openai.llms import OpenAI
from langchain.prompts import PromptTemplate
from .config import OPENAI_API_KEY  # Cambiar a importación relativa si necesario
from models import ConversationMemory, db  # Cambiar a importación relativa si está dentro de un paquete


# Crear una instancia de LLM con la clave de la API
def get_llm():
    if not OPENAI_API_KEY:
        raise ValueError("La clave OPENAI_API_KEY no está definida. Verifica tu archivo de configuración.")
    return OpenAI(api_key=OPENAI_API_KEY, temperature=0.6)

def process_with_prompt(prompt_text, user_input):
    try:
        # Obtén la instancia de LLM
        llm = get_llm()

        # Crea y formatea el prompt
        prompt = PromptTemplate(template=prompt_text, input_variables=["input"])
        formatted_prompt = prompt.format(input=user_input)

        # Genera la respuesta usando LLM
        return llm(formatted_prompt)
    except Exception as e:
        raise RuntimeError(f"Error al procesar el prompt: {e}")

def save_to_memory(session_id, user_input, bot_response):
    try:
        # Crea una nueva entrada de conversación en la memoria
        memory_entry = ConversationMemory(
            session_id=session_id,
            user_input=user_input,
            bot_response=bot_response,
        )
        db.session.add(memory_entry)
        db.session.commit()  # Ejecutar commit para guardar los cambios en la base de datos
    except Exception as e:
        db.session.rollback()  # Revertir la transacción en caso de error
        raise RuntimeError(f"Error al guardar en la memoria: {e}")

def retrieve_memory(session_id):
    try:
        # Recupera todas las entradas de la memoria para una sesión específica
        memory_entries = ConversationMemory.query.filter_by(session_id=session_id).all()
        return [
            {
                "user_input": entry.user_input,
                "bot_response": entry.bot_response
            }
            for entry in memory_entries
        ]
    except Exception as e:
        raise RuntimeError(f"Error al recuperar la memoria: {e}")
