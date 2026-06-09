from flask import Flask, request
from ipaddress import ip_address, IPv4Network, IPv6Network
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

LOCAL_IP_RANGES = [
    IPv4Network('127.0.0.0/8'),
    IPv4Network('10.0.0.0/8'),
    IPv4Network('172.16.0.0/12'),
    IPv4Network('192.168.0.0/16'),
    IPv6Network('::1/128'),
    IPv6Network('fc00::/7'),
    IPv6Network('fe80::/10'),
]

def is_local_ip(ip_str):
    try:
        ip = ip_address(ip_str.strip())
        for network in LOCAL_IP_RANGES:
            if ip in network:
                return True
        return False
    except ValueError:
        return False

@app.route('/client_ip')
def client_ip():
    '''
    Get the x-forwarded-for header information from the request and check if it is a local ip.
    If it is not a local ip, raise an exception.
    :return: The x-forwarded-for header.
    '''
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise BadRequest('X-Forwarded-For header is missing')

    first_ip = x_forwarded_for.split(',')[0].strip()

    if not is_local_ip(first_ip):
        raise BadRequest('IP address is not local')

    return x_forwarded_for
