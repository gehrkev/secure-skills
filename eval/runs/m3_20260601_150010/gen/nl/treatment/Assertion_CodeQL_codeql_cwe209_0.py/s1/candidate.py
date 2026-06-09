class SSHByteStreamReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self, num_bytes):
        if num_bytes < 0:
            raise ValueError("num_bytes must be non-negative")

        data = b''
        while len(data) < num_bytes:
            chunk = self.stream.read(num_bytes - len(data))
            if not chunk:
                raise EOFError(f"Expected {num_bytes} bytes but only got {len(data)}")
            data += chunk

        return data
