from flask import Flask, request
import ipaddress

app = Flask(__name__)

def is_local_ip(ip_str):
    """Check if an IP address is a local/private IP"""
    try:
        ip = ipaddress.ip_address(ip_str.strip())
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False

@app.route('/get-forwarded-ip')
def get_forwarded_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise Exception("X-Forwarded-For header not found")

    # Get the first IP in case there are multiple
    ip = x_forwarded_for.split(',')[0].strip()

    if not is_local_ip(ip):
        raise Exception(f"IP address {ip} is not a local IP")

    return x_forwarded_for

if __name__ == '__main__':
    app.run()
