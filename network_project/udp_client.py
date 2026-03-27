import socket

HOST = '127.0.0.1'
PORT = 5002
BUFFER_SIZE = 1024


def main():
    message = input('Enter message: ')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
        data, _ = client_socket.recvfrom(BUFFER_SIZE)
        print(f'Server response: {data.decode("utf-8")}')


if __name__ == '__main__':
    main()
