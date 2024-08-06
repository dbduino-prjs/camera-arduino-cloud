import logging
from flask import Flask, request, send_from_directory, redirect, url_for
import os

PORT=8080

# Folder where the uploaded files are stored
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

# Logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print ('No file part', 400, request.files)
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        print ('No selected file', 400)
        return 'No selected file', 400
    app.logger.info(f"Uploading '{file.filename}'")
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    app.logger.info(f"File '{file.filename}' uploaded successfully")
    return 'File uploaded successfully', 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    app.logger.info("Downloading '{filename}'")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
