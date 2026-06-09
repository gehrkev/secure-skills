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

    ips = [ip.strip() for ip in x_forwarded_for.split(',')]

    for ip in ips:
        try:
            ip_obj = ipaddress.ip_address(ip)
            if not (ip_obj.is_private or ip_obj.is_loopback):
                raise ValueError(f"Non-local IP address detected: {ip}")
        except ValueError:
            raise ValueError(f"Invalid IP address: {ip}")

    return x_forwarded_for
