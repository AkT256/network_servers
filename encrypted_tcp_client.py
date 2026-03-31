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
    """Подключается к защищённому TCP-серверу, выполняет обмен ключами, отправляет зашифрованное сообщение и выводит ответ."""
    message = input('Enter secure message: ')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_private_key = x25519.X25519PrivateKey.generate()
        client_public_key = client_private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        server_public_key = x25519.X25519PublicKey.from_public_bytes(recv_packet(client_socket))
        send_packet(client_socket, client_public_key)
        shared_key = client_private_key.exchange(server_public_key)
        key = derive_key(shared_key)
        send_packet(client_socket, encrypt_message(key, message))
        encrypted_response = recv_packet(client_socket)
        response = decrypt_message(key, encrypted_response)
        print(f'Secure server response: {response}')


if __name__ == '__main__':
    main()
