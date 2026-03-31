import socket

HOST = '127.0.0.1'
PORT = 5000
BUFFER_SIZE = 1024


def main():
    """Подключается к TCP-серверу, отправляет сообщение и выводит ответ сервера."""
    message = input('Enter message: ')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(BUFFER_SIZE)
        print(f'Server response: {data.decode("utf-8")}')


if __name__ == '__main__':
    main()
