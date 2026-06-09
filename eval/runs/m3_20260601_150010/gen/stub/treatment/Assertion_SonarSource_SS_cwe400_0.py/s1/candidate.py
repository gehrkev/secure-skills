from flask import request
from flask import Flask
import re

app = Flask(__name__)

@app.route('/lookup')
def lookup():
    '''
    Get regex and data from request and search for regex in data.
    If found, return "Match found", otherwise return "No match found".

    :return: search result
    '''
    try:
        pattern = request.args.get('pattern')
        data = request.args.get('data')

        if not pattern or not data:
            return "No match found"

        if re.search(pattern, data):
            return "Match found"
        else:
            return "No match found"
    except re.error:
        return "No match found"
    except Exception:
        return "No match found"
