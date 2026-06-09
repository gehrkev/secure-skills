from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install():
    package_name = request.args.get('package') or request.form.get('package')

    if not package_name:
        return {'error': 'package parameter is required'}, 400

    subprocess.run(['conda', 'install', '-y', package_name], check=True)

    return {'package': package_name}

if __name__ == '__main__':
    app.run()
