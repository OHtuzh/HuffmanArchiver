import os

import lib.HuffmanTree
from lib.file_managers.CustomWriter import CustomWriter
from math import log2
from os.path import basename


def count_entropy(frequency: dict, number_of_chars: int) -> int:
    return -sum(v / number_of_chars * log2(v / number_of_chars) for v in frequency.values())


def build_huffman_tree_and_table(file_path: str) -> (lib.HuffmanTree.Node, dict):
    frequency = dict()
    file = open(file_path, 'rb')
    counter = 0
    while (byte := file.read(1)):
        frequency[byte] = frequency.get(byte, 0) + 1
        counter += 1

    file.close()
    print(f'Entropy: {count_entropy(frequency, counter)}')
    tree, table = lib.HuffmanTree.build_huffman_tree_and_table(frequency)
    return tree, table, counter


def encode_node(writer: CustomWriter, node: lib.HuffmanTree.Node):
    if node.get_data() is not None:
        writer.write_bit(1)
        writer.write_byte(node.get_data())
    else:
        writer.write_bit(0)
        encode_node(writer, node.get_left())
        encode_node(writer, node.get_right())


def encode_file(file_path: str, archive_path: str):
    tree, table, number_of_chars = build_huffman_tree_and_table(file_path)
    writer = CustomWriter(archive_path)
    file_name = basename(file_path)
    writer.write_int32(len(file_name))
    for char in file_name:
        writer.write_byte(ord(char))
    writer.write_int32(number_of_chars)
    encode_node(writer, tree)

    input_data = open(file_path, 'rb')
    while (byte := input_data.read(1)):
        for bit in table.get(ord(byte)):
            writer.write_bit(int(bit))

    input_data.close()

    writer.close()
