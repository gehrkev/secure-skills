from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def handle_request():
    content_type = request.headers.get('Content-Type')
    return Response('', content_type=content_type)

if __name__ == '__main__':
    app.run()
