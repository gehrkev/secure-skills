from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/client_ip', methods=['GET', 'POST'])
def client_ip():
    x_forwarded_for = request.headers.get('x-forwarded-for')

    if not x_forwarded_for:
        raise Exception("x-forwarded-for header not found")

    # Get the first IP in the list (client IP)
    client_ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(client_ip_str)
    except ValueError:
        raise Exception(f"Invalid IP address: {client_ip_str}")

    # Check if IP is local (private or loopback)
    if not (ip.is_private or ip.is_loopback):
        raise Exception(f"IP address is not local: {client_ip_str}")

    return x_forwarded_for

if __name__ == '__main__':
    app.run(debug=True)
