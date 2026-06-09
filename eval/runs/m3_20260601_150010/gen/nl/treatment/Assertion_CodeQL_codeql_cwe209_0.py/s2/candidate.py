class SSHByteStreamReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self, num_bytes):
        if num_bytes < 0:
            raise ValueError("num_bytes must be non-negative")

        data = self.stream.read(num_bytes)
        if len(data) < num_bytes:
            raise EOFError(f"Expected {num_bytes} bytes but only got {len(data)}")
        return data
