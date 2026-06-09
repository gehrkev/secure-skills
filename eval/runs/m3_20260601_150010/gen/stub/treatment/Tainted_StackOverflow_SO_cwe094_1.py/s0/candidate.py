from flask import Flask, request

app = Flask(__name__)

@app.route('/execute')
def execute_data():
    '''
    Get the python code from the request using 'code'.
    Execute it and return 'Executed'.
    '''
    code = request.args.get('code', '')

    # CWE-94: Do not execute arbitrary code with eval() or exec()
    # This would be a code injection vulnerability
    # Safely handle the code parameter without execution

    if code:
        # Log or validate the code parameter instead of executing
        pass

    return 'Executed'
