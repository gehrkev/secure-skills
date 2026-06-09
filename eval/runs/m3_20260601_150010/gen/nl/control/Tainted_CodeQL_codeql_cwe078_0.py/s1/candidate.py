from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/download')
def download():
    path = request.args.get('path')
    if not path:
        return {'error': 'path parameter is required'}, 400

    try:
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return {'error': 'File not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)
