from lib.file_managers.CustomReader import CustomReader
from lib.HuffmanTree import Node


def read_node(reader: CustomReader) -> Node:
    if reader.read_bit() == 1:
        return Node(data=reader.read_byte())
    else:
        left = read_node(reader)
        right = read_node(reader)
        return Node(left=left, right=right)


def decode_archive(archive_path: str):
    reader = CustomReader(archive_path)

    file_name_size = reader.read_int32()
    file_name = ''.join([chr(reader.read_byte()) for i in range(file_name_size)])
    number_of_chars = reader.read_int32()
    tree = read_node(reader)

    output = open(file_name, 'wb')

    current = tree
    wrote = 0
    while True:
        bit = reader.read_bit()
        if bit == 0:
            current = current.get_left()
        else:
            current = current.get_right()
        if current.get_data() is not None:
            output.write(bytes([current.get_data()]))
            current = tree
            wrote += 1
            if wrote == number_of_chars:
                break
