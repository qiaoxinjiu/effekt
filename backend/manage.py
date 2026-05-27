# encoding: UTF-8
from flask_cors import CORS
from flask import make_response, jsonify, request, redirect, send_from_directory, safe_join
from app import create_app
import os

app = create_app()
CORS(app, resources=r'/*')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'attachment', 'bug_picture')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    try:
        safe_path = safe_join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(safe_path):
            return f"File not found: {filename}", 404
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)


def cors_response(res):
    response = make_response(jsonify(res))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response
