import socket
import os
import hashlib

RECEIVED_FOLDER = 'received'
os.makedirs(RECEIVED_FOLDER, exist_ok=True)

server_socket = socket.socket()
server_socket.bind(('localhost', 9000))
server_socket.listen()

print("Server nhận file đang chạy...")

while True:
    conn, addr = server_socket.accept()
    header = conn.recv(1024).decode()
    filename, expected_hash = header.split('|')
    conn.send(b'OK')

    filepath = os.path.join(RECEIVED_FOLDER, filename)
    with open(filepath, 'wb') as f:
        while True:
            data = conn.recv(4096)
            if data == b'DONE':
                break
            f.write(data)

    # Tính SHA-256 và kiểm tra
    actual_hash = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
    if actual_hash == expected_hash:
        print(f"[✓] File {filename} hợp lệ (SHA-256 trùng khớp).")
    else:
        print(f"[!] CẢNH BÁO: File {filename} bị thay đổi!")

    conn.close()
