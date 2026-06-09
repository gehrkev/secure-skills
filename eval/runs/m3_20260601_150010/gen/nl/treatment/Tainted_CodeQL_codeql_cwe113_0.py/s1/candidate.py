from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/echo-content-type', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def echo_content_type():
    content_type = request.headers.get('Content-Type', 'text/plain')

    return Response('Content-Type echoed', content_type=content_type)

if __name__ == '__main__':
    app.run()
