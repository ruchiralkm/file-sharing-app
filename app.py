from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string, jsonify
import os
import sys
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Folder to store uploaded files
UPLOAD_FOLDER = '/tmp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML code embedded as a template string with enhanced stylish UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FileBeam</title>
    <style>
        :root {
            --primary-color: #4a90e2;
            --secondary-color: #f5a623;
            --background-color: #f0f4f8;
            --text-color: #333;
            --card-background: #ffffff;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: url('https://wallpaperaccess.com/full/1750461.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .container {
            max-width: 800px;
            width: 90%;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(2px);
        }
        h1 {
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .upload-section, .reset-section {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .btn-primary {
            background-color: var(--primary-color);
            color: white;
        }
        .btn-primary:hover {
            background-color: #3a7bc8;
            transform: translateY(-2px);
        }
        .btn-danger {
            background-color: var(--secondary-color);
            color: white;
        }
        .btn-danger:hover {
            background-color: #e59400;
            transform: translateY(-2px);
        }
        .btn-download {
            background-color: var(--primary-color);
            color: white;
            padding: 8px 16px;
            font-size: 14px;
        }
        .btn-download:hover {
            background-color: #3a7bc8;
        }
        .file-input {
            display: none;
        }
        .file-label {
            display: inline-block;
            padding: 12px 24px;
            background-color: var(--primary-color);
            color: white;
            border-radius: 50px;
            cursor: pointer;
            font-weight: bold;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .file-label:hover {
            background-color: #3a7bc8;
            transform: translateY(-2px);
        }
        .file-list {
            list-style-type: none;
            padding: 0;
        }
        .file-item {
            background-color: var(--card-background);
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 10px;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }
        .file-item:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .file-info {
            display: flex;
            align-items: center;
        }
        .file-name {
            margin-right: 15px;
        }
        .file-size {
            color: #666;
            font-size: 0.9em;
        }
        .file-link {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: bold;
        }
        .file-link:hover {
            text-decoration: underline;
        }
        .progress-container {
            width: 100%;
            background-color: #f3f3f3;
            border-radius: 20px;
            margin-top: 20px;
            overflow: hidden;
            display: none;
        }
        .progress-bar {
            width: 0;
            height: 30px;
            background-color: var(--primary-color);
            text-align: center;
            line-height: 30px;
            color: white;
            transition: width 0.5s ease;
        }
        #upload-status {
            text-align: center;
            margin-top: 10px;
            font-weight: bold;
            color: var(--primary-color);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>FileBeam</h1>
        <center>
          <h5>©Designed by Ruchira Kaluarachchi</h5>
          <p>Scan this QR code with other device</p>
          <img src="https://raw.githubusercontent.com/ruchiralkm/Small-Testing/refs/heads/main/Assets/frame.png" alt="qr-code" style="width: 150px; height: 150px;">
        </center>
        <div class="upload-section">
            <form id="upload-form" action="/upload" method="post" enctype="multipart/form-data">
                <label for="file-upload" class="file-label">Choose File</label>
                <input id="file-upload" class="file-input" type="file" name="file">
            </form>
        </div>
        <div class="progress-container" id="progress-container">
            <div class="progress-bar" id="progress-bar"></div>
        </div>
        <div id="upload-status"></div>
        <div class="reset-section">
            <form action="/reset" method="post">
                <input type="submit" class="btn btn-danger" value="Reset (Remove All Files)">
            </form>
        </div>
        <center><span style="color:red;">This application made testing purposes for only</span></center>
        <h2>Uploaded Files</h2>
        <ul class="file-list">
            {% for file in files %}
                <li class="file-item">
                    <div class="file-info">
                        <span class="file-name">{{ file }}</span>
                        <span class="file-size">{{ file_sizes.get(file, 'Unknown size') }}</span>
                    </div>
                    <a href="{{ url_for('download_file', filename=file) }}" class="btn btn-download">Download</a>
                </li>
            {% else %}
                <li>No files uploaded yet.</li>
            {% endfor %}
        </ul>
    </div>
    <script>
        document.getElementById('file-upload').onchange = function() {
            if (this.files.length > 0) {
                uploadFile(this.files[0]);
            }
        };

        function uploadFile(file) {
            var xhr = new XMLHttpRequest();
            var formData = new FormData();
            formData.append('file', file);

            xhr.open('POST', '/upload', true);

            xhr.upload.onprogress = function(e) {
                if (e.lengthComputable) {
                    var percentComplete = (e.loaded / e.total) * 100;
                    document.getElementById('progress-bar').style.width = percentComplete + '%';
                    document.getElementById('progress-bar').textContent = Math.round(percentComplete) + '%';
                }
            };

            xhr.onloadstart = function(e) {
                document.getElementById('progress-container').style.display = 'block';
                document.getElementById('upload-status').textContent = 'Uploading...';
            };

            xhr.onloadend = function(e) {
                document.getElementById('upload-status').textContent = 'Upload Complete!';
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            };

            xhr.send(formData);
        }
    </script>
</body>
</html>
"""

# Error handler for all exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error('An error occurred: %s', str(e), exc_info=True)
    return render_template_string("""
        <h1>An Error Occurred</h1>
        <p>Sorry, an unexpected error has occurred. Please try again later.</p>
        <p>Error: {{ error }}</p>
    """, error=str(e)), 500

# Home route: Show upload form and list of uploaded files
@app.route('/')
def home():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        file_sizes = {}
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            size = os.path.getsize(file_path)
            file_sizes[file] = f"{size / 1024:.2f} KB"
        return render_template_string(HTML_TEMPLATE, files=files, file_sizes=file_sizes)
    except Exception as e:
        app.logger.error('Error in home route: %s', str(e), exc_info=True)
        return handle_exception(e)

# Upload files from phone/PC
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            raise ValueError('No file part')
        
        file = request.files['file']
        if file.filename == '':
            raise ValueError('No selected file')
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return jsonify({'success': True, 'message': 'File uploaded successfully'})
    except Exception as e:
        app.logger.error('Error in upload_file route: %s', str(e), exc_info=True)
        return jsonify({'success': False, 'message': str(e)})

# Download files to mobile/PC
@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        app.logger.error('Error in download_file route: %s', str(e), exc_info=True)
        return handle_exception(e)

# Reset (remove all files)
@app.route('/reset', methods=['POST'])
def reset_files():
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        return redirect(url_for('home'))
    except Exception as e:
        app.logger.error('Error in reset_files route: %s', str(e), exc_info=True)
        return handle_exception(e)

if __name__ == '__main__':
    app.run(debug=True)
