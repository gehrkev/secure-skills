from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/getcookie')
def getcookie():
    cookie_value = request.cookies.get('cookie')
    response = make_response('OK')

    if cookie_value:
        response.set_cookie('cookie', cookie_value, httponly=True, secure=True, samesite='Strict')

    return response

if __name__ == '__main__':
    app.run()
