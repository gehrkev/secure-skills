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

    client_ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(client_ip_str)
    except ValueError:
        raise ValueError(f"Invalid IP address: {client_ip_str}")

    if not ip.is_private:
        raise Exception(f"IP address {client_ip_str} is not a local IP")

    return x_forwarded_for
