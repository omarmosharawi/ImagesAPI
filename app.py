from flask import Flask, request, jsonify
from actions import bp as actionsbp
# from filters import bp as filtersbp
# from andriod import bp as androidbp
from helpers import allowed_extension, get_secure_filename_filepath


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSION = ['png', 'jpg', 'jpeg']

app = Flask(__name__)

app.secret_key = 'SECRET_KEY_API'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSION'] = ALLOWED_EXTENSION

app.register_blueprint(actionsbp)


@app.route('/images', methods=["POST"])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file was selected.'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file was selected.'}), 400

        if not allowed_extension(file.filename):
            return jsonify({'error': 'The extension is not supported.'}), 400

        filename, filepath = get_secure_filename_filepath(file.filename)
        return jsonify({
            'message': 'File successfully uploaded.',
            'filename': filename,
        }), 201


# app.register_blueprint(filtersbp)
#
# app.register_blueprint(androidbp)
