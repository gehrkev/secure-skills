import ssl

# Create an SSL context using standard library settings
context = ssl.create_default_context()

# The default context is configured with:
# - System CA certificates loaded
# - Hostname checking enabled
# - Certificate verification enabled
# - Minimum TLS version set to TLS 1.2
# - Strong cipher suites configured

# Optional: Configure additional security settings if needed
# context.check_hostname = True  # Already enabled by default
# context.verify_mode = ssl.CERT_REQUIRED  # Already set by default

print("SSL context created successfully with standard library settings")
print(f"Protocol: {context.protocol}")
print(f"Check hostname: {context.check_hostname}")
print(f"Verify mode: {context.verify_mode}")
