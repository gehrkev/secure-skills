from flask import Flask, request

app = Flask(__name__)


def is_local_ip(ip):
    """Check if an IP address is local/private."""
    ip = ip.strip()

    # IPv4 loopback
    if ip.startswith('127.'):
        return True

    # IPv6 loopback
    if ip == '::1':
        return True

    # Private ranges
    if ip.startswith('10.'):
        return True
    if ip.startswith('192.168.'):
        return True
    if ip.startswith('172.'):
        parts = ip.split('.')
        if len(parts) >= 2:
            try:
                second_octet = int(parts[1])
                if 16 <= second_octet <= 31:
                    return True
            except ValueError:
                pass

    if ip.lower() == 'localhost':
        return True

    return False


@app.route('/client_ip')
def client_ip():
    """Get the client IP from x-forwarded-for header and verify it's local."""
    x_forwarded_for = request.headers.get('x-forwarded-for')

    if not x_forwarded_for:
        raise ValueError("x-forwarded-for header not found")

    client_ip_addr = x_forwarded_for.split(',')[0].strip()

    if not is_local_ip(client_ip_addr):
        raise ValueError(f"IP address {client_ip_addr} is not local")

    return x_forwarded_for


if __name__ == '__main__':
    app.run()
