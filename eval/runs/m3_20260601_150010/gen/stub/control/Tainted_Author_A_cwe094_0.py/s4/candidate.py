from flask import Flask, request

app = Flask(__name__)

@app.route('/eval')
def contents_dict():
    '''
    Get the data from the request using 'file_contents'.
    Remove anything before the first '{' and after the last '}'.
    Return the content by evaluating it to a dictionary.
    '''
    # Get file_contents from request
    file_contents = request.args.get('file_contents') or request.form.get('file_contents')
    if not file_contents and request.is_json:
        data = request.get_json()
        if data:
            file_contents = data.get('file_contents')

    # Find the first '{' and last '}'
    start_idx = file_contents.find('{')
    end_idx = file_contents.rfind('}')

    # Extract substring from first '{' to last '}'
    extracted = file_contents[start_idx:end_idx+1]

    # Evaluate and return as dictionary
    result = eval(extracted)
    return result
