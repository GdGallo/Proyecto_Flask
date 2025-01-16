from langchain_openai.llms import OpenAI
from langchain.prompts import PromptTemplate
from .config import OPENAI_API_KEY  
from models import ConversationMemory, db


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
        db.session.commit()          # Ejecutar commit para guardar los cambios en la base de datos
        # Limitar la memoria a 10 conversaciones
        conversation_count = ConversationMemory.query.filter_by(session_id=session_id).count() 
        if conversation_count > 10:summarize_conversation(session_id)
        #OPCIONAL: eliminar post antiguos
        #delete_old_conversation(session_id)
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
    

def summarize_conversation(session_id):
    # Recuperar la conversación desde la memoria
    conversation = retrieve_memory(session_id)
    if not conversation:
        return None
    
    # Crear el contexto uniendo entradas y respuestas
    context = "\n".join(
        f"Usuario: {conv['user_input']}\nBot: {conv['bot_response']}"
        for conv in conversation
    )
    
    # Crear el prompt para el resumen
    summary_prompt = (
        "Aquí hay una conversación entre el usuario y un bot. Resume de manera breve y clara:\n\n"
        f"{context}\n\nResumen:"
    )
    
    # Obtener el modelo de lenguaje (llm)
    llm = get_llm()
    summary = llm(summary_prompt)

    # Guardar el resumen en la base de datos
    memory_entry = ConversationMemory(
        session_id=session_id,
        user_input="[RESUMEN]",
        bot_response=summary
    )
    db.session.add(memory_entry)
    db.session.commit()

    return summary


    # Eliminar interacciones antiguas
def delete_old_conversations(session_id):
    conversation = ConversationMemory.query.filter_by(session_id=session_id).all()
    if len(conversation) > 10:
        for conv in conversation[:-1]:
            #Manten solo el resumen mas reciente
            db.session.delete(conv)
            db.session.commit()