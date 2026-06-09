from flask import Flask, request
from ipaddress import ip_address

app = Flask(__name__)

@app.route('/check-forwarded-ip', methods=['GET'])
def check_forwarded_ip():
    # Extract the x-forwarded-for header
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise ValueError("X-Forwarded-For header is missing")

    # Get the first IP in the list (original client IP)
    client_ip = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ip_address(client_ip)
    except ValueError:
        raise ValueError(f"Invalid IP address: {client_ip}")

    # Check if IP is local (private or loopback)
    if not (ip.is_private or ip.is_loopback):
        raise ValueError(f"IP address {client_ip} is not a local IP")

    return x_forwarded_for
