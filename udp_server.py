import socket

HOST = '127.0.0.1'
PORT = 5002
BUFFER_SIZE = 1024


def main():
    """Запускает UDP-сервер, принимает дейтаграммы и отправляет клиентам эхо-ответы."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f'UDP server started on {HOST}:{PORT}')
        while True:
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            message = data.decode('utf-8')
            print(f'Received from {addr[0]}:{addr[1]} -> {message}')
            response = f'ECHO: {message}'.encode('utf-8')
            server_socket.sendto(response, addr)


if __name__ == '__main__':
    main()
