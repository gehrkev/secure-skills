from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def echo_content_type():
    content_type = request.headers.get('Content-Type', 'text/plain')
    return Response('', content_type=content_type)

if __name__ == '__main__':
    app.run()
