from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/check-forwarded', methods=['GET', 'POST'])
def check_forwarded():
    # Extract the x-forwarded-for header
    forwarded_for = request.headers.get('X-Forwarded-For')

    if not forwarded_for:
        raise ValueError("X-Forwarded-For header is missing")

    # Get the first IP address (in case of multiple)
    ip_str = forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        raise ValueError(f"Invalid IP address: {ip_str}")

    # Check if it's a local IP (private or loopback)
    if not (ip.is_private or ip.is_loopback):
        raise ValueError(f"IP address {ip_str} is not a local IP")

    return forwarded_for

if __name__ == '__main__':
    app.run()
