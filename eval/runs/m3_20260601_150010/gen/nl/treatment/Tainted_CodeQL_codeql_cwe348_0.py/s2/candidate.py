from flask import Flask, request
import ipaddress

app = Flask(__name__)

@app.route('/client_ip')
def client_ip():
    x_forwarded_for = request.headers.get('x-forwarded-for')

    if not x_forwarded_for:
        raise ValueError("x-forwarded-for header not found")

    client_ip_str = x_forwarded_for.split(',')[0].strip()

    try:
        ip = ipaddress.ip_address(client_ip_str)

        if not (ip.is_loopback or ip.is_private or ip.is_link_local):
            raise ValueError(f"IP address {client_ip_str} is not local")

        return x_forwarded_for
    except ipaddress.AddressValueError as e:
        raise ValueError(f"Invalid IP address: {str(e)}")

if __name__ == '__main__':
    app.run()
