from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/client_ip')
def client_ip_endpoint():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise Exception("X-Forwarded-For header not found")

    # X-Forwarded-For can contain multiple IPs, get the first one
    client_ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(client_ip_str)
    except ValueError:
        raise Exception(f"Invalid IP address: {client_ip_str}")

    if not (ip.is_private or ip.is_loopback):
        raise Exception(f"IP address {client_ip_str} is not local")

    return x_forwarded_for

if __name__ == '__main__':
    app.run(debug=True)
