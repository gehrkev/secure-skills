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
    xff = request.headers.get('X-Forwarded-For')

    if not xff:
        raise ValueError("X-Forwarded-For header not found")

    client_ip_str = xff.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(client_ip_str)
        if not (ip.is_private or ip.is_loopback):
            raise ValueError(f"IP {client_ip_str} is not a local IP")
    except ipaddress.AddressValueError:
        raise ValueError(f"Invalid IP address: {client_ip_str}")

    return xff
