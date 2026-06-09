from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/execute_bash', methods=['GET', 'POST'])
def execute_bash():
    command = request.args.get('command') or request.form.get('command')
    if not command:
        return "No command provided", 400

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run()
