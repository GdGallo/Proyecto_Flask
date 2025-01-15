from flask import Blueprint, request, jsonify
from .helpers import process_with_prompt

langchain_bp = Blueprint('langchain', __name__)

@langchain_bp.route('/langchain/process', methods=['POST'])
def process_text():
    # Validar que la solicitud contenga datos JSON
    data = request.get_json()
    if not data:
        return jsonify({'error': 'El cuerpo de la solicitud debe ser JSON.'}), 400

    # Validar que el campo "input" esté presente y no esté vacío
    user_input = data.get('input')
    if not user_input or not user_input.strip():
        return jsonify({'error': 'El campo "input" es obligatorio y no puede estar vacío.'}), 400

    # Crear el texto del prompt
    prompt_text = 'Actúa como un asistente experto en inteligencia artificial. Responde esta pregunta: {input}'
    
    try:
        response = process_with_prompt(prompt_text.format(input=user_input), user_input)
        return jsonify({'response': response}), 200
    except KeyError as e:
        return jsonify({'error': f'Llave faltante: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Valor inválido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500


