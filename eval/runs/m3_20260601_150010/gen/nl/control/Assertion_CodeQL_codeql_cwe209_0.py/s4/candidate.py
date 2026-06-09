class SSHByteStreamReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self, n):
        """Read exactly n bytes from the stream.

        Raises EOFError if fewer than n bytes remain in the stream.
        """
        data = self.stream.read(n)
        if len(data) < n:
            raise EOFError(f"Expected {n} bytes, but only {len(data)} bytes available")
        return data
