class SSHByteStreamReader:
    def __init__(self, stream):
        self.stream = stream

    def read(self, num_bytes):
        data = self.stream.read(num_bytes)
        if len(data) < num_bytes:
            raise EOFError()
        return data
