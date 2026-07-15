class MockHttpResponse:
    def __init__(self, status_code=200, json=None, text="", content=b""):
        self.status_code = status_code
        self._json = json
        self._text = text
        self._content = content

    def json(self):
        return self._json


class MockSideEffects:
    pass
