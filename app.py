"""Flask application for thesis document formatting."""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from src.formatter import DocumentFormatter
from src.exceptions import FormattingError, InvalidFileFormatError, FileCorruptedError
import os
import tempfile
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'docx'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Display upload page."""
    return render_template('index.html')


@app.route('/format', methods=['POST'])
def format_document():
    """Handle document formatting request."""

    # Check file presence
    if 'file' not in request.files:
        return jsonify({'error': '请选择文件'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': '请选择文件'}), 400

    # Validate file extension
    if not allowed_file(file.filename):
        return jsonify({'error': '仅支持.docx格式'}), 400

    upload_path = None
    formatted_path = None

    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Check file size (secondary check)
        if os.path.getsize(upload_path) > 50 * 1024 * 1024:
            os.remove(upload_path)
            return jsonify({'error': '文件过大，最多50MB'}), 400

        # Format document
        formatter = DocumentFormatter()
        formatted_path = formatter.format_document(upload_path, keep_original=False)

        # Read formatted file into memory
        with open(formatted_path, 'rb') as f:
            file_data = BytesIO(f.read())

        # Cleanup temp files
        if os.path.exists(upload_path):
            os.remove(upload_path)
        if os.path.exists(formatted_path):
            os.remove(formatted_path)

        # Return formatted file
        file_data.seek(0)
        return send_file(
            file_data,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f"{filename.rsplit('.', 1)[0]}_formatted.docx"
        )

    except InvalidFileFormatError as e:
        return jsonify({'error': str(e)}), 400
    except FileCorruptedError as e:
        return jsonify({'error': '文件无效或损坏，请重新上传'}), 400
    except FormattingError as e:
        return jsonify({'error': f'处理失败：{str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'未知错误：{str(e)}'}), 500
    finally:
        # Ensure cleanup
        if upload_path and os.path.exists(upload_path):
            try:
                os.remove(upload_path)
            except:
                pass
        if formatted_path and os.path.exists(formatted_path):
            try:
                os.remove(formatted_path)
            except:
                pass


@app.route('/result')
def result():
    """Display result page."""
    return render_template('result.html')


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': '文件过大，最多50MB'}), 413


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True', host='0.0.0.0', port=port)
