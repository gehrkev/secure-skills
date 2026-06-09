from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/check-forwarded-ip', methods=['GET', 'POST'])
def check_forwarded_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise ValueError("X-Forwarded-For header not found")

    ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        raise ValueError(f"Invalid IP address: {ip_str}")

    if not (ip.is_private or ip.is_loopback or ip.is_link_local):
        raise ValueError(f"IP address {ip_str} is not a local IP")

    return x_forwarded_for
