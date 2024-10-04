from flask import Flask, request, jsonify, send_from_directory
from actions import bp as actionsbp
from filters import bp as filtersbp
from andriod import bp as androidbp
from helpers import allowed_extension, get_secure_filename_filepath, upload_to_s3
import boto3, botocore


UPLOAD_FOLDER = 'uploads/'
DOWNLOAD_FOLDER = 'downloads/'
ALLOWED_EXTENSION = ['png', 'jpg', 'jpeg']

app = Flask(__name__)

app.secret_key = 'SECRET_KEY_API'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['ALLOWED_EXTENSION'] = ALLOWED_EXTENSION

app.register_blueprint(actionsbp)
app.register_blueprint(filtersbp)
app.register_blueprint(androidbp)


app.config['S3_BUCKET'] = 'image-api'
app.config['S3_KEY'] = ''
app.config['S3_SECRET'] = ''
app.config['S3_LOCATION'] = ''


@app.route('/images', methods=['GET', 'POST'])
def images():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file was selected.'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file was selected.'}), 400

        if not allowed_extension(file.filename):
            return jsonify({'error': 'The extension is not supported.'}), 400

        # filename, filepath = get_secure_filename_filepath(file.filename)
        # file.save(filepath)
        output = upload_to_s3(file, app.config['S3_BUCKET'])
        return jsonify({
            'message': 'File successfully uploaded.',
            # 'filename': filename,
            'filename': output
        }), 201

    images = []
    s3_resource = boto3.resource('s3', aws_access_key_id=app.config['S3_KEY'],
                                 aws_secret_access_key=app.config['S3_SECRET'])
    s3_bucket = s3_resource.Bucket(app.config['S3_BUCKET'])
    for obj in s3_bucket.objects.filter(Prefix='uploads/'):
        if obj.key == 'uploads/':
            continue
        images.append(obj.key)
    return jsonify({"data": images})


# @app.route('/uploads/<name>')
@app.route('/downloads/<name>')
def download_file(name):
    # return send_from_directory(app.config['UPLOAD_FOLDER'], name)
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], name)
