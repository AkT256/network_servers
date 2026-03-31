import socket
import threading

HOST = '127.0.0.1'
PORT = 5001
BUFFER_SIZE = 1024


def handle_client(conn, addr):
    """Обрабатывает одного клиента в отдельном потоке и возвращает эхо-ответы на его сообщения."""
    with conn:
        print(f'Client connected: {addr[0]}:{addr[1]}')
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            message = data.decode('utf-8')
            print(f'[{addr[0]}:{addr[1]}] {message}')
            conn.sendall(f'ECHO: {message}'.encode('utf-8'))
        print(f'Client disconnected: {addr[0]}:{addr[1]}')


def main():
    """Запускает многопоточный TCP-сервер и создаёт отдельный поток для каждого клиента."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f'Threaded TCP server started on {HOST}:{PORT}')
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()


if __name__ == '__main__':
    main()
