class ByteBuilder:
    def __init__(self, size=0):
        self._bytes = bytearray(size)
        self._index = 0

    @property
    def content(self):
        return self._bytes

    @property
    def index(self):
        return self._index

    def seek(self, offset, mode='c'):
        if mode == 's':
            self._index = offset
        elif mode == 'c':
            self._index += offset
        elif mode == 'e':
            self._index = len(self._bytes) + offset

    # end of seek

    def feed(self, data: bytes, mode='APPEND'):
        size = len(data)
        start = self._index
        end = start + size
        buffer_size = len(self._bytes)
        if buffer_size < end:
            self._bytes += b'\00' * (end - buffer_size)
        if mode == 'SET':
            self._bytes[start:end] = data
        elif mode == 'APPEND':
            self._bytes[start:end] = data
            self._index = end
        elif mode == 'AND':
            new_data = data
            old_data = self._bytes[start:end]
            for i in range(size):
                new_data[i] = new_data[i] & old_data[i]
            self._bytes[start:end] = new_data
        elif mode == 'OR':
            new_data = data
            old_data = self._bytes[start:end]
            for i in range(size):
                new_data[i] = new_data[i] | old_data[i]
            self._bytes[start:end] = new_data
        elif mode == 'XOR':
            new_data = data
            old_data = self._bytes[start:end]
            for i in range(size):
                new_data[i] = new_data[i] ^ old_data[i]
            self._bytes[start:end] = new_data
        else:
            raise Exception(f"Unknown feed mode: '{mode}'! Expected modes: SET, APPEND, AND, OR, XOR")
    # end of feed
# end of class
