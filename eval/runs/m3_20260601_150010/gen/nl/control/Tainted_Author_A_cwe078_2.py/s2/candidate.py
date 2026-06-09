from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install():
    package_name = request.args.get('package') or request.form.get('package')

    if not package_name:
        return jsonify({'error': 'package parameter required'}), 400

    try:
        subprocess.run(['conda', 'install', '-y', package_name], check=True)
        return jsonify({'package': package_name})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
