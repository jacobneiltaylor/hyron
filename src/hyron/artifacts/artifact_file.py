from io import BytesIO


class ArtifactFile:
    def __init__(self, name, encoding):
        self.name = name
        self.encoding = encoding
        self.buf = BytesIO()
        self._open = True

    def _write(self, callback):
        if self._open:
            self.buf.write(callback())
        else:
            raise RuntimeError(f"File '{self.name}' is already closed")

    def write_bytes(self, data: bytes):
        self._write(lambda: data)

    def write_text(self, data: str):
        self._write(lambda: data.encode(self.encoding))

    def close(self):
        self._open = False

    def get_contents(self):
        self.close()
        return self.buf.getvalue()
