from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def echo_content_type():
    content_type = request.headers.get('Content-Type')
    response = Response("OK", content_type=content_type)
    return response

if __name__ == '__main__':
    app.run()
