import os
import requests

from flask import Flask, request

app = Flask(__name__)

# Define allowed URLs (or domains)
ALLOWED_URLS = [
    'https://example.com/data.json',
    'https://api.example.com/info',
]

@app.route('/curl')
def curl():
    '''
    Get the url from the request using 'url'.
    Download the file by taking the url parameter from the request.
    :return: url
    '''
    # Get the user-provided URL
    url = request.args.get('url', '')

    # Validate against allowed URLs
    if url not in ALLOWED_URLS:
        return "Invalid or unauthorized URL.", 400

    # Fetch content safely
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return "Failed to fetch content.", 500
