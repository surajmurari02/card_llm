from flask import Flask, render_template, request, jsonify
import requests
import cv2
import numpy as np
import time

app = Flask(__name__)

# Server URL for processing
SERVER_URL = "http://4.240.46.255:1337/upload"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Get the image file from the request
    image_file = request.files.get('image')
    if image_file:
        # Convert the image to bytes
        image_bytes = image_file.read()
        
        # Prepare the files and text data for the POST request
        files = {'image': ('image.jpg', image_bytes, 'image/jpeg')}
        text = {"query": "I am providing business cards. Extract name, designation, company name, mobile number, email, and address in JSON format."}

        try:
            # Send the request to the external server
            response = requests.post(SERVER_URL, files=files, data=text, timeout=30)
            response_data = response.json()
        except requests.RequestException as e:
            return jsonify({"error": str(e)}), 500
        
        # Return JSON response to the front end
        return jsonify(response_data)
    
    return jsonify({"error": "No image provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
