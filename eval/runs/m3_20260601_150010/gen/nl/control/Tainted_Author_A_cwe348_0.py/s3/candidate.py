from flask import Flask, request
import ipaddress

app = Flask(__name__)

def is_local_ip(ip):
    """Check if an IP address is local (private or loopback)"""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback
    except ValueError:
        return False

@app.route('/validate-forwarded-for')
def validate_forwarded_for():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise Exception("X-Forwarded-For header is missing")

    # Extract the first IP (original client IP)
    ip = x_forwarded_for.split(',')[0].strip()

    # Raise exception if IP is not local
    if not is_local_ip(ip):
        raise Exception(f"IP address {ip} is not a local IP")

    return x_forwarded_for
