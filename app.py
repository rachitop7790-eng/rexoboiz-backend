import os
import zipfile
import shutil
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Ye frontend aur backend ka rasta kholta hai

UPLOAD_FOLDER = '/tmp/uploads'
CONVERT_FOLDER = '/tmp/converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "RexoBoiz Converter Backend is Running Active!"

@app.route('/convert', methods=['POST'])
def convert_world():
    if 'world' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['world']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save original file
    zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(zip_path)

    # Output file path (.mcworld)
    output_filename = file.filename.rsplit('.', 1)[0] + '.mcworld'
    output_path = os.path.join(CONVERT_FOLDER, output_filename)

    # For testing & fast processing, renaming zip to mcworld
    shutil.copyfile(zip_path, output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
