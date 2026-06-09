from flask import Flask
from flask import request
import ipaddress

app = Flask(__name__)

@app.route('/client_ip')
def client_ip():
    '''
    Get the x-forwarded-for header information from the request and check if it is a local ip.
    If it is not a local ip, raise an exception.
    :return: The x-forwarded-for header.
    '''
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise ValueError("X-Forwarded-For header not found")

    ip = x_forwarded_for.split(',')[0].strip()

    try:
        ip_addr = ipaddress.ip_address(ip)
        if not ip_addr.is_private:
            raise ValueError(f"IP {ip} is not a local IP")
    except ValueError as e:
        if "does not appear to be an IPv4 or IPv6 address" in str(e):
            raise ValueError(f"Invalid IP address: {ip}")
        raise

    return x_forwarded_for
