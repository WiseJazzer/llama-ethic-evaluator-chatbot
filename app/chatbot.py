from flask import Flask, request, jsonify
from modelos.Llama_Model import LlamaModel

app = Flask(__name__)
model = LlamaModel()  # No se necesita clave API

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    text = data.get('text')
    theories = data.get('theories', [])
    keywords = data.get('keywords', [])

    if not text:
        return jsonify({"error": "El texto del estudiante es requerido"}), 400

    feedback = model.evaluate_ethical_judgment(text, theories, keywords)
    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)