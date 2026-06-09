from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/getcookie', methods=['GET', 'POST'])
def getcookie():
    # Retrieve the 'cookie' value from the request
    cookie_value = request.args.get('cookie') or request.form.get('cookie')

    if not cookie_value:
        return "No cookie value provided", 400

    # Create a response
    response = make_response("Cookie set successfully")

    # Set the cookie in the response with security considerations
    # httponly=True prevents XSS attacks (CWE-79)
    # secure=True ensures the cookie is only sent over HTTPS
    # samesite='Strict' provides CSRF protection (CWE-352)
    response.set_cookie('cookie', cookie_value,
                       httponly=True,
                       secure=True,
                       samesite='Strict')

    return response

if __name__ == '__main__':
    app.run(debug=False)
