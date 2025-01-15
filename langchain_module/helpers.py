from langchain_openai.llms import OpenAI
from langchain.prompts import PromptTemplate
from .config import OPENAI_API_KEY

# Crear una instancia de LLM con la clave de la API
def get_llm():
    # Asegúrate de devolver la instancia correctamente
    return OpenAI(api_key=OPENAI_API_KEY, temperature=0.6)

def process_with_prompt(prompt_text, user_input):
    # Obtén la instancia de LLM
    llm = get_llm()

    # Crea y formatea el prompt
    prompt = PromptTemplate(template=prompt_text, input_variables=['input'])
    formatted_prompt = prompt.format(input=user_input)

    # Genera la respuesta usando LLM
    return llm(formatted_prompt)
