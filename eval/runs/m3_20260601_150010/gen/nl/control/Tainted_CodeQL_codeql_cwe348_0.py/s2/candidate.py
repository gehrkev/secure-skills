from flask import Flask, request
import ipaddress

app = Flask(__name__)

def is_local_ip(ip):
    """Check if an IP address is local/private."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_loopback or ip_obj.is_private
    except ValueError:
        return False

@app.route('/client_ip')
def client_ip():
    forwarded_for = request.headers.get('X-Forwarded-For')

    if not forwarded_for:
        raise Exception("X-Forwarded-For header not found")

    ip = forwarded_for.split(',')[0].strip()

    if not is_local_ip(ip):
        raise Exception(f"IP address {ip} is not local")

    return forwarded_for

if __name__ == '__main__':
    app.run()
