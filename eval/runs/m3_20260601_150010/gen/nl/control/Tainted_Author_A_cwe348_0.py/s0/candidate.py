from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/check-x-forwarded-for')
def check_x_forwarded_for():
    # Get the x-forwarded-for header
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise Exception("X-Forwarded-For header not found")

    # The x-forwarded-for header can contain multiple IPs (comma separated)
    # Get the first one
    ip_address = x_forwarded_for.split(',')[0].strip()

    # Check if it's a local IP
    try:
        ip_obj = ipaddress.ip_address(ip_address)
        if not (ip_obj.is_private or ip_obj.is_loopback):
            raise Exception(f"IP address {ip_address} is not a local IP")
    except ValueError:
        raise Exception(f"Invalid IP address: {ip_address}")

    return x_forwarded_for

if __name__ == '__main__':
    app.run()
