from flask import current_app
from werkzeug.utils import secure_filename
import os


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSION']


def get_secure_filename_filepath(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    return filename, filepath