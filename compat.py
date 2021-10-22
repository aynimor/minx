class Header(dict):
    def __init__(self, default=None):
        if default:
            self.update(default)

    @property
    def cookies(self):
        data = {}
        cookies = self.get("Cookie", None)
        if not cookies:
            return None
        data = {}
        for cookie in cookies.split("; "):
            k, v = cookie.split("=")
            data[k] = v
        return data
