from flask import Flask, request
import ipaddress

app = Flask(__name__)


@app.route('/check-forwarded-ip', methods=['GET'])
def check_forwarded_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise ValueError("X-Forwarded-For header not provided")

    client_ip = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(client_ip)
    except ValueError:
        raise ValueError(f"Invalid IP address in X-Forwarded-For: {client_ip}")

    if not ip.is_private:
        raise ValueError(f"IP address {client_ip} is not a local IP")

    return x_forwarded_for


if __name__ == '__main__':
    app.run(debug=False)
