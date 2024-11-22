from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Configura tu API Key de OpenAI
openai.api_key = ''

# Ruta principal para renderizar el HTML
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para interactuar con ChatGPT y adaptar el texto
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Recibimos el texto, tipo de adaptación y público desde el request
        data = request.json
        texto = data.get('texto')
        tipo_adaptacion = data.get('adaptacion')
        publico = data.get('publico')

        # Contexto para el mensaje a la API de OpenAI
        user_message = f"""El usuario te envía el siguiente texto:
        "{texto}"

        Elige un estilo de texto basado en: {tipo_adaptacion}.
        Adapta el texto para el público objetivo: {publico}.
        """

        # Llamada a la API de OpenAI utilizando el endpoint de completions
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Cambia a "gpt-4" si tienes acceso
            messages=[{"role": "user", "content": user_message}],
            max_tokens=300,
            temperature=0.7,
        )

        # Extraemos y enviamos la respuesta generada por la IA
        chatgpt_response = response['choices'][0]['message']['content'].strip()

        return jsonify({'response': chatgpt_response})

    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
