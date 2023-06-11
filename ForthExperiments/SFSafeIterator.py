class SafeIterator:
    def __init__(self, content):
        if isinstance(content, list):
            content = iter(content)
        self.content = content

    def next(self):
        try:
            return next(self.content)
        except:
            return None
