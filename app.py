from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {'error': 'No image uploaded'}, 400
    
    image_file = request.files['image']
    input_image = Image.open(image_file.stream)
    
    # Remove background
    output = remove(input_image)
    
    # Save output in memory
    img_io = io.BytesIO()
    output.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

@app.route('/')
def home():
    return "🟢 Background Remover API Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
