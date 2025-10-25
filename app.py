from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
# CORS(app, origins=["http://localhost:5173", "https://yourdomain.com"])
CORS(app)
# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Import routes
from routes import pdf_routes, doc_routes, image_routes
app.register_blueprint(pdf_routes.bp)
app.register_blueprint(doc_routes.bp)
# app.register_blueprint(image_routes.bp)

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# Cleanup old files (call periodically)
def cleanup_old_files():
    cutoff = datetime.now() - timedelta(hours=1)
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        for file in os.listdir(folder):
            filepath = os.path.join(folder, file)
            if os.path.getmtime(filepath) < cutoff.timestamp():
                os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)