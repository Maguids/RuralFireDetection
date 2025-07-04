import os
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras.models import Model, load_model
from PIL import Image
import tensorflow as tf
from model_loader import build_model_1, build_AHMHCNN_mCBAM

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

# Modelos base sem pesos (arquiteturas)
base_model_1 = build_model_1()
base_model_2 = build_AHMHCNN_mCBAM()
loaded_models = {}

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['image']
    phase = request.form.get('phase')
    model_name = request.form.get('modelName')

    if not model_name or not phase:
        return jsonify({'error': 'phase e modelName são obrigatórios'}), 400

    key = f'{phase}_{model_name}'
    model_path = f'Models/{phase}/{model_name}/model.h5'

    if not os.path.exists(model_path):
        return jsonify({'error': f'Model file not found at {model_path}'}), 404

    if key in loaded_models:
        model = loaded_models[key]
    else:
        lower_name = model_name.lower()
        if 'model_2' in lower_name:
            model = tf.keras.models.clone_model(base_model_2)
            model.load_weights(model_path)
        elif 'model_1' in lower_name:
            model = tf.keras.models.clone_model(base_model_1)
            model.load_weights(model_path)
        else:
            return jsonify({'error': f'Model "{model_name}" não suportado'}), 400
        loaded_models[key] = model

    input_size = 256 if 'model_2' in model_name.lower() else 224
    img = Image.open(file.stream).convert('RGB')
    img = img.resize((input_size, input_size))
    img_array = np.asarray(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0]
    predicted_class = int(np.argmax(prediction))
    confidence = float(np.max(prediction))
    has_fire = predicted_class == 1

    return jsonify({
        'hasFire': has_fire,
        'confidence': f"{confidence:.2f}"
    })

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/ImageSamples/<path:filename>')
def serve_sample_image(filename):
    return send_from_directory('ImageSamples', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
