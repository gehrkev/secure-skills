from flask import Flask, request
from ipaddress import ip_address, ip_network

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

    client_ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ip_address(client_ip_str)
    except ValueError:
        raise ValueError("Invalid IP address in X-Forwarded-For header")

    local_networks = [
        ip_network('127.0.0.0/8'),
        ip_network('10.0.0.0/8'),
        ip_network('172.16.0.0/12'),
        ip_network('192.168.0.0/16'),
        ip_network('::1/128'),
        ip_network('fc00::/7'),
    ]

    is_local = any(ip in network for network in local_networks)

    if not is_local:
        raise ValueError(f"IP {client_ip_str} is not a local IP")

    return x_forwarded_for
