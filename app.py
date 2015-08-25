#!/usr/bin/env python

import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
from werkzeug import secure_filename
from flask import jsonify


# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

# If the file you are trying to upload is too big, you'll get this message
@app.errorhandler(413)
def request_entity_too_large(error):
    message = 'The file is too large, my friend.<br>'
    maxFileSizeKB = app.config['MAX_CONTENT_LENGTH']/(1024)
    message += "The biggest I can handle is " + str(maxFileSizeKB) + "KB"
    message += "<a href='" + url_for("index") + "'>Try again</a>"
    return message, 413

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# The root where we ask user to enter a file
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if not allowed_file(file.filename):
        message = "Sorry. Only files that end with one of these "
        message += "extensions is permitted: " 
        message += str(app.config['ALLOWED_EXTENSIONS'])
        message += "<a href='" + url_for("index") + "'>Try again</a>"
        return message
    elif not file:
        message = "Sorry. There was an error with that file.<br>"
        message += "<a href='" + url_for("index") + "'>Try again</a>"
        return message        
    else:
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',filename=filename))


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888,debug=False)
