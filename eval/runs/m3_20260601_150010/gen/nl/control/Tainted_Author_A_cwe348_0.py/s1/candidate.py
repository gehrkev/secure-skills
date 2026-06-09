from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/check-xff', methods=['GET'])
def check_xff():
    # Get the x-forwarded-for header
    xff = request.headers.get('X-Forwarded-For')

    if not xff:
        raise Exception("X-Forwarded-For header not present")

    # Extract the first IP (x-forwarded-for can contain multiple IPs)
    ip_str = xff.split(',')[0].strip()

    # Check if it's a valid IP address
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        raise Exception(f"Invalid IP address: {ip_str}")

    # Raise an exception if the IP is not local/private
    if not ip.is_private:
        raise Exception(f"IP {ip_str} is not a local IP")

    return xff

if __name__ == '__main__':
    app.run()
