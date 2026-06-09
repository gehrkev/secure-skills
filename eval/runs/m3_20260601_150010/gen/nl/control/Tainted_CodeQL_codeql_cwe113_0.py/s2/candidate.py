from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def extract_content_type():
    content_type = request.headers.get('Content-Type')
    response = make_response('OK')

    if content_type:
        response.headers['Content-Type'] = content_type

    return response

if __name__ == '__main__':
    app.run()
