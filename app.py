<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultra Stylish File Sharing</title>
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
            backdrop-filter: blur(10px);
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
        <h1>Ultra Stylish File Sharing</h1>
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
