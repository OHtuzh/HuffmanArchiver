from lib.Decoder import decode_archive
from lib.Encoder import encode_file

if __name__ == '__main__':
    while True:
        operation = input('Operations: encode decode exit\n')
        if operation == "encode":
            file_path = input('Enter filepath: ')
            archive_name = input('Archive name: ')
            encode_file(file_path, archive_name + '.huff')
        elif operation == "decode":
            archive_path = input('Enter archive path: ')
            decode_archive(archive_path)
        elif operation == "exit":
            break
        else:
            print('Unknown operation!')
