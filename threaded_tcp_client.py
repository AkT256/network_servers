import socket

HOST = '127.0.0.1'
PORT = 5001
BUFFER_SIZE = 1024


def main():
    """Подключается к многопоточному TCP-серверу, отправляет сообщения и выводит ответы."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f'Connected to threaded TCP server {HOST}:{PORT}')
        while True:
            message = input('Enter message (or exit): ')
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(BUFFER_SIZE)
            print(f'Server response: {data.decode("utf-8")}')


if __name__ == '__main__':
    main()
