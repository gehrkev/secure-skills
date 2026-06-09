from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/getcookie")
def getcookie():
    '''
    Get the cookie from the request using 'cookie' and set it as a cookie in the response.
    :return: The response with the cookie.
    '''
    cookie_value = request.args.get('cookie')
    response = make_response('Cookie set')
    if cookie_value:
        response.set_cookie('cookie', cookie_value, httponly=True, secure=True, samesite='Strict')
    return response
