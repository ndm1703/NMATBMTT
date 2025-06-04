import socket
import os

RECEIVED_FOLDER = 'received'
os.makedirs(RECEIVED_FOLDER, exist_ok=True)

server_socket = socket.socket()
server_socket.bind(('localhost', 9000))
server_socket.listen(1)
print("Server nhận file đang chạy tại localhost:9000...")

while True:
    conn, addr = server_socket.accept()
    print(f"Kết nối từ {addr}")
    data = conn.recv(1024).decode()
    print(f"Nhận dữ liệu: {data!r}")
    if '|' not in data:
        print("Dữ liệu nhận được không hợp lệ!")
        conn.close()
        continue
    filename, hash_value = data.split('|', 1)
    conn.send(b'ACK')

    filepath = os.path.join(RECEIVED_FOLDER, filename)
    with open(filepath, 'wb') as f:
        while True:
            chunk = conn.recv(4096)
            if chunk == b"DONE":
                break
            f.write(chunk)
    print(f"Đã nhận file {filename} với SHA-256: {hash_value}")
    conn.close()