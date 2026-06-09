from flask import Flask, request
import ipaddress

app = Flask(__name__)


@app.route('/check-forwarded-ip')
def check_forwarded_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise Exception("X-Forwarded-For header not found")

    ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        raise Exception(f"Invalid IP address in X-Forwarded-For: {ip_str}")

    if not (ip_obj.is_private or ip_obj.is_loopback):
        raise Exception(f"IP address {ip_str} is not a local IP")

    return x_forwarded_for
