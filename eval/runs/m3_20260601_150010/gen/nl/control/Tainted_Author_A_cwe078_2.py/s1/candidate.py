from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install_package():
    package_name = request.args.get('package') or request.form.get('package')

    if not package_name:
        return {'error': 'No package name provided'}, 400

    try:
        subprocess.run(['conda', 'install', '-y', package_name], check=True)
        return {'package': package_name}
    except subprocess.CalledProcessError as e:
        return {'error': f'Failed to install {package_name}: {str(e)}'}, 500

if __name__ == '__main__':
    app.run()
