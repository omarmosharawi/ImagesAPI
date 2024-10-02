from flask import Blueprint, request, current_app, redirect, url_for
from helpers import get_secure_filename_filepath
import os
from PIL import Image
from zipfile import ZipFile
from datetime import datetime
import shutil
from os.path import basename

bp = Blueprint('android', __name__, url_prefix='/android')

ICON_SIZE = [29, 40, 57, 58, 60, 80, 87, 114, 120, 180, 1024]


@bp.route('/', methods=["POST"])
def create_images():
    filename = request.json['filename']
    filepath, filename = get_secure_filename_filepath(filename)

    tempfolder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp')
    os.makedirs(tempfolder)

    for size in ICON_SIZE:
        outfile = os.path.join(tempfolder, f'{size}.png')
        image = Image.open(filepath)
        out = image.resize((size, size))
        out.save(outfile, 'PNG')

    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).rsplit('.')[0]
    zipfilename = f'{timestamp}.zip'
    zipfilepath = os.path.join(current_app.config['UPLOAD_FOLDER'], zipfilename)

    with ZipFile(zipfilepath, 'w') as zipObj:
        for foldername, subfolders, filenames, in os.walk(tempfolder):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                zipObj.write(filepath, basename(filepath))
        shutil.rmtree(tempfolder)
        redirect(url_for('download_file', name=zipfilename))