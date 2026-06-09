from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/getcookie')
def getcookie():
    # Retrieve the 'cookie' value from the request
    cookie_value = request.cookies.get('cookie')

    # Create a response
    response = make_response('Cookie processed')

    # Set the cookie in the response if it exists
    if cookie_value:
        response.set_cookie('cookie', cookie_value)

    return response

if __name__ == '__main__':
    app.run()
