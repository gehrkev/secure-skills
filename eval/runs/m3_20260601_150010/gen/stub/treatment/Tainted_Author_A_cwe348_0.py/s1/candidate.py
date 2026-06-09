from flask import Flask
from flask import request
import ipaddress

app = Flask(__name__)

def is_local_ip(ip_str):
    '''
    Check if an IP address is a local/private IP.
    '''
    try:
        ip = ipaddress.ip_address(ip_str.strip())
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False

@app.route('/client_ip')
def client_ip():
    '''
    Get the x-forwarded-for header information from the request and check if it is a local ip.
    If it is not a local ip, raise an exception.
    :return: The x-forwarded-for header.
    '''
    forwarded_for = request.headers.get('X-Forwarded-For')

    if not forwarded_for:
        raise ValueError('X-Forwarded-For header is missing')

    # X-Forwarded-For can contain multiple IPs (client, proxy1, proxy2, ...)
    # The first IP is typically the client IP
    ips = [ip.strip() for ip in forwarded_for.split(',')]
    client_ip_str = ips[0] if ips else None

    if not client_ip_str:
        raise ValueError('X-Forwarded-For header is empty')

    # Check if the client IP is a local IP
    if not is_local_ip(client_ip_str):
        raise ValueError(f'IP address {client_ip_str} is not a local IP')

    return forwarded_for
