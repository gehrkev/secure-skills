import flask
import subprocess
import sys

app = flask.Flask(__name__)

@app.route('/install')
def install():
    package = flask.request.args.get('package')
    if package:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return package
    return ''

if __name__ == '__main__':
    app.run()
