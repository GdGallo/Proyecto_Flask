from flask import Blueprint, request, jsonify
from .helpers import process_with_prompt, save_to_memory, retrieve_memory
from . import langchain_bp

@langchain_bp.route("/langchain/process", methods=["POST"])
def process_text():
    # Validar que la solicitud contenga datos JSON
    data = request.get_json()
    if not data:
        return jsonify({"error": "El cuerpo de la solicitud debe ser JSON."}), 400

    # Validar que el campo "input" esté presente y no esté vacío
    user_input = data.get("input")
    if not user_input or not user_input.strip():
        return jsonify({"error": 'El campo "input" es obligatorio y no puede estar vacío.'}), 400

    # Crear el texto del prompt
    prompt_text = "Actúa como un asistente experto en inteligencia artificial. Responde esta pregunta: {input}"

    try:
        # Procesar el prompt con el texto del usuario
        response = process_with_prompt(prompt_text.format(input=user_input), user_input)
        return jsonify({"response": response}), 200
    except KeyError as e:
        return jsonify({"error": f"Llave faltante: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Valor inválido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500

@langchain_bp.route("/langchain/chat", methods=["POST"])
def chat_with_memory():
    # Validar que la solicitud contenga datos JSON
    data = request.get_json()
    if not data or "input" not in data or "session_id" not in data:
        return jsonify({"error": 'El cuerpo de la solicitud debe contener los campos "input" y "session_id".'}), 400

    # Validar la presencia de "input" y "session_id"
    session_id = data.get("session_id")
    user_input = data.get("input")
    past_conversation = retrieve_memory(session_id)
    
    context = "\n".join(
        f"Usuario:{conv['user_input']}\nBot:{conv['bot_response']}" for conv in past_conversation
    )

    # Crear el prompt con el contexto
    prompt_text = f"{context}\nUsuario: {user_input}\nBot:"
    bot_response = process_with_prompt(prompt_text, user_input)

    # Guardar la nueva interacción en la memoria
    save_to_memory(session_id, user_input, bot_response)
    return jsonify({"response": bot_response}), 200
