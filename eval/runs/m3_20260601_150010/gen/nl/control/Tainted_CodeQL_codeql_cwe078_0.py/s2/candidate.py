from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    path = request.args.get('path')
    if not path:
        return {'error': 'Path parameter required'}, 400

    try:
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return {'error': 'File not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
