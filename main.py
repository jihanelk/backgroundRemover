from flask import Flask, request, send_file
from flask_cors import CORS
import io
import zipfile
from PIL import Image
import rembg

app = Flask(__name__)
CORS(app)

def remove_bg(data):
    input_image = Image.open(io.BytesIO(data))
    output_image = rembg.remove(input_image)
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format='PNG')
    return output_buffer.getvalue()

@app.route('/remove-bg', methods=['POST'])
def remove_bg_endpoint(): 
    if 'files' not in request.files:
        return 'No files part', 400
    files = request.files.getlist('files')
    if not files:
        return 'No selected files', 400

    processed_images = []

    for file in files:
        data = file.read()
        img = remove_bg(data)
        processed_images.append(img)

    # Create a zip file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for i, img in enumerate(processed_images):
            zf.writestr(f'image_{i}.png', img)
    memory_file.seek(0)

    return send_file(memory_file, mimetype='application/zip', as_attachment=True, attachment_filename='processed_images.zip')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
