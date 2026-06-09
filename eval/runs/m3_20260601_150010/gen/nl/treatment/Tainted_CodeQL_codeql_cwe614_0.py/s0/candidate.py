from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/getcookie')
def getcookie():
    cookie_value = request.args.get('cookie') or request.form.get('cookie')

    if cookie_value:
        response = make_response('Cookie set')
        response.set_cookie('cookie', cookie_value, httponly=True, secure=True, samesite='Strict')
        return response
    else:
        return 'No cookie value provided', 400

if __name__ == '__main__':
    app.run()
