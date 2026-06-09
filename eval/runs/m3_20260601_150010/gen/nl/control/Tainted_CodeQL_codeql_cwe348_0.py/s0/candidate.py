from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/client_ip')
def client_ip():
    # Get the x-forwarded-for header
    x_forwarded_for = request.headers.get('x-forwarded-for')

    if not x_forwarded_for:
        raise Exception("x-forwarded-for header not found")

    # Extract the first IP from the header (in case there are multiple)
    ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        raise Exception(f"Invalid IP address: {ip_str}")

    # Check if the IP is local (private or loopback)
    if not (ip.is_private or ip.is_loopback):
        raise Exception(f"IP address is not local: {ip_str}")

    return x_forwarded_for

if __name__ == '__main__':
    app.run()
