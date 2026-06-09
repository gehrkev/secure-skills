from flask import Flask, request

app = Flask(__name__)

@app.route('/check_url')
def check_url():
    target_url = request.args.get('target_url', '')

    if target_url.endswith('.com/'):
        return 'True'
    else:
        return 'False'

if __name__ == '__main__':
    app.run()
