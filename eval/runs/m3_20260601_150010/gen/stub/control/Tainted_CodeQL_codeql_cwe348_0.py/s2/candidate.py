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

    client_ip_addr = x_forwarded_for.split(',')[0].strip()

    ip = ipaddress.ip_address(client_ip_addr)
    if not (ip.is_private or ip.is_loopback):
        raise ValueError(f"IP {client_ip_addr} is not a local IP")

    return x_forwarded_for
