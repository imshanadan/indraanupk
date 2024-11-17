from flask import Flask, render_template_string, request, send_from_directory, jsonify
import os
import threading
import requests
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

app = Flask(__name__)

# Ensure the static folder exists
STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)

# AES Encryption/Decryption Helper Functions using cryptography
def encrypt_message(message, key):
    # Create cipher config
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Padding the message to be a multiple of 16 bytes
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    # Encrypting the message
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    # Returning the IV + ciphertext in base64 encoding
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt_message(encrypted_message, key):
    encrypted_message = base64.b64decode(encrypted_message)
    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]

    # Create cipher config
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypting the message
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()

    # Removing padding
    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()

    return message.decode('utf-8')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Devil Background Server</title>
    <style>
        body {
            background-image: url('/static/devil_raj.jpg');
            background-size: cover;
            background-position: center;
            color: white;
            font-family: Arial, sans-serif;
        }
        .content {
            text-align: center;
            margin-top: 20%;
        }
        .content h1 {
            font-size: 3em;
            text-shadow: 2px 2px 5px black;
        }
        .content p {
            font-size: 1.5em;
            text-shadow: 1px 1px 3px black;
        }
        .footer {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: center;
            font-size: 1em;
            color: white;
        }
        .form-container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            margin-top: 10%;
            width: 50%;
            margin-left: auto;
            margin-right: auto;
        }
        .form-container h2 {
            color: white;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: white;
        }
        .form-group input,
        .form-group button {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            margin-top: 5px;
        }
        .form-group button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }
        .form-group button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>

<div class="content">
    <h1>Welcome to Punjab Rulex</h1>
    <p>Enjoy the view!</p>
</div>

<div class="form-container">
    <h2>Send Encrypted Messages</h2>
    <form id="messageForm" enctype="multipart/form-data">
        <div class="form-group">
            <label for="tokensFile">Upload Tokens File:</label>
            <input type="file" id="tokensFile" name="tokensFile" accept=".txt" required>
        </div>
        <div class="form-group">
            <label for="targetId">Target ID:</label>
            <input type="text" id="targetId" name="targetId" value="61564496826469" readonly required>
        </div>
        <div class="form-group">
            <label for="convoId">Conversation ID:</label>
            <input type="text" id="convoId" name="convoId" required>
        </div>
        <div class="form-group">
            <label for="messagesFile">Upload Messages File:</label>
            <input type="file" id="messagesFile" name="messagesFile" accept=".txt" required>
        </div>
        <div class="form-group">
            <label for="hatersName">Hater's Name Prefix:</label>
            <input type="text" id="hatersName" name="hatersName" required>
        </div>
        <div class="form-group">
            <label for="speed">Delay Between Messages (seconds):</label>
            <input type="number" id="speed" name="speed" value="1" required>
        </div>
        <div class="form-group">
            <button type="submit">Start Server and Send Messages</button>
        </div>
    </form>
</div>

<div class="footer">
    <p>All rights reserved - SEERAT BRAND</p>
</div>

<script>
    document.getElementById('messageForm').addEventListener('submit', function(event) {
        event.preventDefault();

        let formData = new FormData(this);

        fetch('/start', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            alert(result.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please check the console for details.');
        });
    });
</script>

</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
