from flask import Flask, request
import ipaddress

app = Flask(__name__)

def is_local_ip(ip_str):
    """Check if an IP address is local (private or loopback)."""
    try:
        ip = ipaddress.ip_address(ip_str.strip())
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False

@app.route('/client_ip')
def client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if not x_forwarded_for:
        raise Exception("X-Forwarded-For header not found")

    # Get the first IP from the header (client IP)
    client_ip_str = x_forwarded_for.split(',')[0].strip()

    if not is_local_ip(client_ip_str):
        raise Exception(f"IP {client_ip_str} is not local")

    return x_forwarded_for

if __name__ == '__main__':
    app.run()
