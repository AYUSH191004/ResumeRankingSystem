from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
        
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Process resume and return results
    return jsonify({'success': True, 'filename': filename})
