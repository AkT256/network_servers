import socket

HOST = '127.0.0.1'
PORT = 5000
BUFFER_SIZE = 1024


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f'TCP server started on {HOST}:{PORT}')
        conn, addr = server_socket.accept()
        with conn:
            print(f'Client connected: {addr[0]}:{addr[1]}')
            data = conn.recv(BUFFER_SIZE)
            if data:
                message = data.decode('utf-8')
                print(f'Received: {message}')
                response = f'ECHO: {message}'.encode('utf-8')
                conn.sendall(response)
        print('Server stopped')


if __name__ == '__main__':
    main()
