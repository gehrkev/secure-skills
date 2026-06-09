import ssl

def create_ssl_context():
    """Create an SSL context with standard library settings."""
    context = ssl.create_default_context()
    return context

if __name__ == '__main__':
    ctx = create_ssl_context()
    print(f"SSL context created: {ctx}")
    print(f"Check hostname: {ctx.check_hostname}")
    print(f"Verify mode: {ctx.verify_mode}")
