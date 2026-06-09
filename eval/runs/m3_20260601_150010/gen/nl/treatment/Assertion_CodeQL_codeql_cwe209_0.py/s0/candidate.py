class SSHByteStreamReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self, num_bytes):
        """
        Read exactly num_bytes from the stream.

        Raises EOFError if fewer bytes than requested remain in the stream.
        """
        data = b''
        bytes_remaining = num_bytes

        while bytes_remaining > 0:
            chunk = self.stream.read(bytes_remaining)
            if not chunk:
                raise EOFError(f"Expected {num_bytes} bytes, but only got {len(data)} bytes")
            data += chunk
            bytes_remaining -= len(chunk)

        return data
