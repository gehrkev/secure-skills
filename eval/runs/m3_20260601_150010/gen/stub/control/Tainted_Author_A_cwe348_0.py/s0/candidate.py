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
        raise Exception("X-Forwarded-For header not found")

    # Extract the client IP (first IP in the chain)
    ip_str = x_forwarded_for.split(',')[0].strip()

    # Check if it's a local/private IP
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        if not ip_obj.is_private:
            raise Exception("IP is not local")
    except ValueError:
        raise Exception(f"Invalid IP address: {ip_str}")

    return x_forwarded_for
