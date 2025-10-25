from flask import Blueprint, request, send_file, jsonify, after_this_request
from werkzeug.utils import secure_filename
import os
import uuid
from utils.pdf_converter import pdf_to_word

bp = Blueprint('pdf', __name__, url_prefix='/api/convert')

@bp.route('/pdf-to-word', methods=['POST'])
def pdf_to_word_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    files = request.files.getlist('file')  # Support multiple files

    if not files:
        return jsonify({"error": "No files provided"}), 400

    output_files = []

    for file in files:
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": f"Invalid file format for {file.filename}. PDF required."}), 400

        # Save upload
        upload_id = str(uuid.uuid4())
        pdf_path = os.path.join('uploads', f'{upload_id}.pdf')
        file.save(pdf_path)
        # Convert
        output_path = os.path.join('outputs', f'{upload_id}.docx')
        try:

            pdf_to_word(pdf_path, output_path)

            # Store output info
            output_files.append({
                "original_filename": secure_filename(file.filename),
                "output_path": output_path
            })

            # Delete files after download
            @after_this_request
            def remove_files(response):
                try:
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                    if os.path.exists(output_path):
                        os.remove(output_path)
                except Exception as e:
                    print(f"⚠️ Error deleting files: {e}")
                return response
        except Exception as e:
            # Cleanup in case of error
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            return jsonify({"error": f"Error converting {file.filename}: {str(e)}"}), 422

    # If only 1 file, send it directly
    if len(output_files) == 1:
        f = output_files[0]
        return send_file(
            f["output_path"],
            as_attachment=True,
            download_name=f"{f['original_filename'].rsplit('.', 1)[0]}.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    # If multiple files, return paths (or you could zip them)
    return jsonify({
        "message": f"{len(output_files)} files converted successfully",
        "files": [
            {
                "original_filename": f["original_filename"],
                "output_path": f["output_path"]
            } for f in output_files
        ]
    })
