from flask import Flask, render_template, request, jsonify
import requests
import json
import cv2
import numpy as np
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

app = Flask(__name__)

# Server URL for processing the image
SERVER_URL = "http://4.213.51.175:11434"

# Google Sheets ID and range
SHEET_ID = "1k4AsP6TvcTFypiwl32f6Utr9URbMX0GctJ8GgQYBR20"
RANGE_NAME = "Sheet1!A:A"  # Appends data starting from the next available row in Column A

# Google Sheets Authentication
def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        'image-processing-app-440900-d05a27643e6f.json', scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build('sheets', 'v4', credentials=credentials)

# Function to append data to Google Sheets
def append_to_google_sheet(response_data):
    try:
        # Clean the response data to remove unwanted escape characters and extra period at the end
        cleaned_data = response_data.strip('"').replace('\\"', '"')

        # Use regex to remove any trailing characters that are not part of the JSON
        cleaned_data = re.sub(r'[^{}[\],":0-9a-zA-Z\s-]', '', cleaned_data)  # Remove unwanted characters
        
        # Optionally, remove the trailing period and check for any extra quotes or stray characters
        cleaned_data = cleaned_data.rstrip('.').strip()  # Remove the trailing period and extra whitespace

        # Ensure that there is no stray double quote at the end
        if cleaned_data.endswith('"'):
            cleaned_data = cleaned_data[:-1]  # Remove the trailing quote if present

        # Log cleaned data to inspect
        print("Cleaned data:")
        print(cleaned_data)

        # Convert the cleaned JSON string to a Python dictionary
        data = json.loads(cleaned_data)  # Parse the response as JSON

        service = authenticate_google_sheets()
        sheet = service.spreadsheets()

        # Prepare data in the format required by Google Sheets
        values = [[
            data.get("name", ""),
            data.get("designation", ""),
            data.get("companyname", ""),
            data.get("mobilenumber", ""),
            data.get("email", ""),
            data.get("address", "")
        ]]

        body = {
            'values': values
        }

        # Append data to the Google Sheet
        result = sheet.values().append(
            spreadsheetId=SHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

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
        text = {
            "query": "I am providing business cards. Extract name, designation, company name, mobile number, email, and address in JSON format. Please return raw, clean JSON with no escape characters. Do not halocinate"
        }

        try:
            # Send the request to the external server
            response = requests.post(SERVER_URL, files=files, data=text, timeout=30)
            response_data = response.text  # Get the response as raw text

            # Log the raw response content for inspection
            print("Raw response content:")
            print(response_data)
            
            # Append the received data to Google Sheets after cleaning
            append_to_google_sheet(response_data)
            
        except requests.RequestException as e:
            return jsonify({"error": str(e)}), 500
        
        # Return JSON response to the front end
        return jsonify(response_data)
    
    return jsonify({"error": "No image provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)

