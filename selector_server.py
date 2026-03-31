import selectors
import socket
import types

HOST = '127.0.0.1'
PORT = 5003
BUFFER_SIZE = 1024
selector = selectors.DefaultSelector()


def accept_connection(server_socket):
    """Принимает новое подключение и регистрирует клиентский сокет в селекторе."""
    conn, addr = server_socket.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    selector.register(conn, selectors.EVENT_READ, data=data)
    print(f'Client connected: {addr[0]}:{addr[1]}')


def service_connection(key, mask):
    """Обрабатывает события чтения и записи для клиентского соединения через селектор."""
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(BUFFER_SIZE)
        if recv_data:
            message = recv_data.decode('utf-8')
            print(f'[{data.addr[0]}:{data.addr[1]}] {message}')
            data.outb += f'ECHO: {message}'.encode('utf-8')
            selector.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
        else:
            print(f'Client disconnected: {data.addr[0]}:{data.addr[1]}')
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
        if not data.outb:
            selector.modify(sock, selectors.EVENT_READ, data=data)


def main():
    """Запускает TCP-сервер на selectors и обслуживает несколько подключений без потоков."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        server_socket.setblocking(False)
        selector.register(server_socket, selectors.EVENT_READ, data=None)
        print(f'Selector server started on {HOST}:{PORT}')
        try:
            while True:
                events = selector.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        accept_connection(key.fileobj)
                    else:
                        service_connection(key, mask)
        except KeyboardInterrupt:
            print('Server stopped')
        finally:
            selector.close()


if __name__ == '__main__':
    main()
