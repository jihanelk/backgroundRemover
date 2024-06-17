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
    if 'files' not in request.files or 'ids' not in request.form:
        return 'No files or IDs part', 400
    files = request.files.getlist('files')
    ids = request.form.getlist('ids')
    if not files or not ids or len(files) != len(ids):
        return 'Files and IDs count mismatch', 400

    print("Files received:", [file.filename for file in files])
    print("IDs received:", ids)

    processed_images = []

    for file, id in zip(files, ids):
        data = file.read()
        img = remove_bg(data)
        processed_images.append((id, img))

    # Create a zip file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for id, img in processed_images:
            zf.writestr(f'{id}.png', img)
    memory_file.seek(0)

    return send_file(memory_file, mimetype='application/zip', as_attachment=True, attachment_filename='processed_images.zip')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
