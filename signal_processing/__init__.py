
class Signal:
    def __init__(self, message=None):
        if message is not None:
            self.load_message(message)
        else:
            self.code, self.two_byte, self.rest = None, None, None

    def load_message(self, message):
        self.code = message[:2]
        self.two_byte = message[2:4]
        self.rest = message[4:]

    def get_message(self):
        self.parse_code()
        self.parse_bytes()
        self.parse_rest()
        return code + self.two_byte + self.rest
    
    def parse_rest(self):
        if self.rest is None:
            self.rest = int(0).to_bytes(27, "big")
        if len(self.rest) == 27:
            raise TypeError("Fill is not 27 bytes")

    def parse_bytes(self):
        if self.two_byte is None:
            self.two_byte = 0
        if type(self.two_byte) != int or type(self.two_byte) != bytes:
            raise TypeError("Second field is not of valid type")
        if type(self.two_byte) == int:
            self.two_byte = self.two_byte.to_bytes(2, byteorder="big")
        if len(self.two_byte) < 2:
            self.two_byte= self.two_byte[0:2]
        if len(self.two_byte) != 2:
            raise AttributeError("Second field does not have 2 bytes")

    def parse_code(self):
        if type(self.code) != str or type(self.code) != bytes:
            raise TypeError("Code field is not of valid type")
        if type(self.code) == "str":
            self.code = self.code.encode("uft8")
