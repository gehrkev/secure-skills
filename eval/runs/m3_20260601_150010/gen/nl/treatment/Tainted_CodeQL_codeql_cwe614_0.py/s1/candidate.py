from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/getcookie', methods=['GET', 'POST'])
def getcookie():
    # Retrieve the 'cookie' value from the request (query params or form data)
    cookie_value = request.args.get('cookie') or request.form.get('cookie')

    if not cookie_value:
        return 'No cookie value provided', 400

    # Create a response
    response = make_response('Cookie set successfully')

    # Set the cookie with security attributes to prevent XSS, CSRF, and replay attacks
    response.set_cookie(
        'cookie',
        cookie_value,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=3600
    )

    return response

if __name__ == '__main__':
    app.run()
