from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/download')
def download():
    filename = request.args.get('filename')
    if not filename:
        return 'No filename provided', 400
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
