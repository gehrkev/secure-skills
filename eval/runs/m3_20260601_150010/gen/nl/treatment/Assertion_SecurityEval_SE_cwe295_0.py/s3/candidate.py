import ssl

context = ssl.create_default_context()
print(f"SSL context created: {context}")
print(f"Protocol: {context.protocol}")
print(f"Verify mode: {context.verify_mode}")
print(f"Check hostname: {context.check_hostname}")
