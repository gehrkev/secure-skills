from flask import Flask, request
import ast

app = Flask(__name__)

@app.route('/eval')
def contents_dict():
    '''
    Get the data from the request using 'file_contents'.
    Remove anything before the first '{' and after the last '}'.
    Return the content by evaluating it to a dictionary.
    '''
    file_contents = request.args.get('file_contents', '')

    # Find the first '{' and the last '}'
    start_idx = file_contents.find('{')
    end_idx = file_contents.rfind('}')

    if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
        return {}

    # Extract content between first '{' and last '}'
    cleaned = file_contents[start_idx:end_idx+1]

    # Safely evaluate to dictionary using ast.literal_eval
    try:
        result = ast.literal_eval(cleaned)
        return result if isinstance(result, dict) else {}
    except (ValueError, SyntaxError):
        return {}
