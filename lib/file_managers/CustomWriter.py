BUFFER_SIZE = 8192


class CustomWriter:
    def __init__(self, file_path: str):
        self.__file = open(file_path, 'wb')
        self.__buffer = [0] * BUFFER_SIZE
        self.__current_bit = 0

    def write_bit(self, bit: int):
        self.__buffer[self.__current_bit // 8] <<= 1
        self.__buffer[self.__current_bit // 8] += bit
        self.__current_bit += 1
        if self.__current_bit == BUFFER_SIZE * 8:
            #self.__file.write(''.join([chr(i) for i in self.__buffer]))
            self.__file.write(bytes(self.__buffer))
            self.__current_bit = 0
            for i in range(BUFFER_SIZE):
                self.__buffer[i] = 0

    def write_byte(self, byte: int):
        for i in range(8):
            self.write_bit((byte >> (8 - i - 1)) & 1)

    def write_int32(self, n: int):
        t = [n & 0xFF000000, n & 0x00FF0000, n & 0x0000FF00, n & 0x000000FF]
        for byte in [(n & 0xFF000000) >> 24, (n & 0x00FF0000) >> 16, (n & 0x0000FF00) >> 8, n & 0x000000FF]:
            self.write_byte(byte)
        x = 2

    def close(self):
        if self.__current_bit != 0:
            #self.__file.write(''.join([chr(i) for i in self.__buffer[:self.__current_bit // 8]]))
            self.__file.write(bytes(self.__buffer[:self.__current_bit // 8]))
            if self.__current_bit % 8 != 0:
                last_byte = self.__buffer[self.__current_bit // 8]
                for i in range(8 - (self.__current_bit % 8)):
                    last_byte <<= 1
                self.__file.write(bytes([last_byte]))
        self.__file.close()
