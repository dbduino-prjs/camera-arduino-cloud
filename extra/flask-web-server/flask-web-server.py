import logging
from flask import Flask, request, send_from_directory, redirect, url_for
import os
from threading import Thread

# Set your own HTTP and HTTPS listening ports
PORT_HTTP  = 8080
PORT_HTTPS = 8443

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

def run_http():
    app.run(host='0.0.0.0', port=PORT_HTTP, debug=False)

def run_https():
    context = ('cert.pem', 'key.pem')  # Replace with your actual certificate and key files
    app.run(host='0.0.0.0', port=PORT_HTTPS, debug=False, ssl_context=context)

if __name__ == '__main__':
    app.debug = True  # Enable debugging mode manually

    http_thread  = Thread(target=run_http)
    https_thread = Thread(target=run_https)
    
    http_thread.start()
    https_thread.start()
    
    http_thread.join()
    https_thread.join()
