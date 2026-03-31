import os
import socket
import struct
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HOST = '127.0.0.1'
PORT = 5004
BUFFER_SIZE = 4096


def recv_exact(conn, size):
    """Считывает из сокета строго указанное количество байтов или сообщает о разрыве соединения."""
    data = b''
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            raise ConnectionError('Connection closed')
        data += chunk
    return data


def send_packet(conn, data):
    """Отправляет пакет данных с префиксом длины для корректного чтения на другой стороне."""
    conn.sendall(struct.pack('!I', len(data)) + data)


def recv_packet(conn):
    """Принимает пакет данных, сначала считывая его длину, а затем само содержимое."""
    length = struct.unpack('!I', recv_exact(conn, 4))[0]
    return recv_exact(conn, length)


def derive_key(shared_key):
    """Преобразует общий секрет в симметричный ключ с помощью HKDF."""
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'network-project').derive(shared_key)


def encrypt_message(key, message):
    """Шифрует текстовое сообщение алгоритмом AES-GCM и возвращает nonce вместе с шифротекстом."""
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, message.encode('utf-8'), None)
    return nonce + encrypted


def decrypt_message(key, data):
    """Расшифровывает полученные данные алгоритмом AES-GCM и возвращает исходную строку."""
    aesgcm = AESGCM(key)
    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')


def main():
    """Запускает защищённый TCP-сервер, выполняет обмен ключами и обрабатывает одно зашифрованное сообщение клиента."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f'Encrypted TCP server started on {HOST}:{PORT}')
        conn, addr = server_socket.accept()
        with conn:
            print(f'Client connected: {addr[0]}:{addr[1]}')
            server_private_key = x25519.X25519PrivateKey.generate()
            server_public_key = server_private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
            send_packet(conn, server_public_key)
            client_public_key = x25519.X25519PublicKey.from_public_bytes(recv_packet(conn))
            shared_key = server_private_key.exchange(client_public_key)
            key = derive_key(shared_key)
            encrypted_request = recv_packet(conn)
            message = decrypt_message(key, encrypted_request)
            print(f'Decrypted message: {message}')
            response = f'ECHO: {message}'
            send_packet(conn, encrypt_message(key, response))
        print('Server stopped')


if __name__ == '__main__':
    main()
