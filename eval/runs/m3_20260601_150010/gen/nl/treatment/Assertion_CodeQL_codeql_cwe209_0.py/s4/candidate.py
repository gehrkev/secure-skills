class SSHByteStreamReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self, num_bytes):
        """Read exactly num_bytes from the stream.

        Raises EOFError if fewer than num_bytes remain in the stream.
        """
        data = b''
        while len(data) < num_bytes:
            chunk = self.stream.read(num_bytes - len(data))
            if not chunk:
                raise EOFError()
            data += chunk
        return data
