import os
import io
import requests
from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
from PIL import Image
from rembg import remove

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/remove-bg', methods=['POST'])
def remove_bg_upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    image_file = request.files['image']
    try:
        input_image = Image.open(image_file.stream).convert("RGBA")
        output_image = remove(input_image)
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/remove-bg-url', methods=['POST'])
def remove_bg_url():
    data = request.get_json()
    image_url = data.get('image_url')
    if not image_url:
        return jsonify({'error': 'Missing image_url'}), 400

    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch image'}), 400
        input_image = Image.open(io.BytesIO(response.content)).convert("RGBA")
        output_image = remove(input_image)
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
