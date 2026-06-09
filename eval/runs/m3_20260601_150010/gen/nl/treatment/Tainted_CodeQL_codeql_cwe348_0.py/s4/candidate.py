from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/client_ip', methods=['GET'])
def client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise Exception("X-Forwarded-For header not found")

    client_ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(client_ip_str)
    except ValueError:
        raise Exception(f"Invalid IP address: {client_ip_str}")

    if not (ip.is_loopback or ip.is_private):
        raise Exception(f"IP address {client_ip_str} is not local")

    return x_forwarded_for

if __name__ == '__main__':
    app.run()
