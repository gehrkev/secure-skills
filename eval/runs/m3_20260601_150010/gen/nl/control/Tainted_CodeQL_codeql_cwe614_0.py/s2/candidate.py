from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/getcookie')
def getcookie():
    cookie_value = request.args.get('cookie')
    response = make_response('Cookie set')
    if cookie_value:
        response.set_cookie('cookie', cookie_value)
    return response

if __name__ == '__main__':
    app.run()
