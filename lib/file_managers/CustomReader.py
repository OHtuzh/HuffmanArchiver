BUFFER_SIZE = 8192


class CustomReader:
    def __init__(self, file_path: str):
        self.__file = open(file_path, 'rb')
        self.__buffer = [0] * BUFFER_SIZE
        self.__current_bit = BUFFER_SIZE * 8

    def read_bit(self) -> int:
        if self.__current_bit == BUFFER_SIZE * 8:
            tmp = self.__file.read(BUFFER_SIZE)
            for i in range(len(tmp)):
                self.__buffer[i] = tmp[i]
            self.__current_bit = 0
        data = (self.__buffer[self.__current_bit // 8] >> (8 - (self.__current_bit % 8) - 1)) & 1
        self.__current_bit += 1
        return data

    def read_byte(self) -> int:
        byte = 0
        for i in range(8):
            byte <<= 1
            byte += self.read_bit()
        return byte

    def read_int32(self) -> int:
        int32 = 0
        for i in range(4):
            int32 <<= 8
            int32 += self.read_byte()
        return int32

    def __del__(self):
        self.__file.close()
