from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/get-forwarded-for', methods=['GET'])
def get_forwarded_for():
    forwarded_for = request.headers.get('X-Forwarded-For')

    if not forwarded_for:
        raise ValueError("X-Forwarded-For header not found")

    # x-forwarded-for can contain multiple IPs; extract the first one
    client_ip = forwarded_for.split(',')[0].strip()

    try:
        ip_obj = ipaddress.ip_address(client_ip)
    except ValueError:
        raise ValueError(f"Invalid IP address: {client_ip}")

    # Check if it's a local/private IP
    if not ip_obj.is_private:
        raise ValueError(f"IP address {client_ip} is not a local IP")

    return forwarded_for

if __name__ == '__main__':
    app.run()
