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
    xfwd = request.headers.get('X-Forwarded-For')
    if not xfwd:
        raise ValueError('X-Forwarded-For header is missing')

    # Get the first IP (client IP)
    client_ip_str = xfwd.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(client_ip_str)
    except ValueError:
        raise ValueError(f'Invalid IP address: {client_ip_str}')

    # Check if it's a local/private IP
    if not ip.is_private:
        raise Exception(f'IP address is not local: {client_ip_str}')

    return xfwd
