import socket
import hashlib

HOST = 'localhost'
PORT = 5001
BUFFER_SIZE = 4096
OUTPUT_FILE = 'received/received_file'

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Đang chờ kết nối trên {HOST}:{PORT}...")

conn, addr = server.accept()
print(f"Kết nối từ {addr}")

# Nhận file
with open(OUTPUT_FILE, 'wb') as f:
    while True:
        data = conn.recv(BUFFER_SIZE)
        if data == b'__done__':
            break
        f.write(data)

# Nhận SHA-256 từ client
client_hash = conn.recv(1024).decode()
server_hash = calculate_sha256(OUTPUT_FILE)

print("HASH từ client:", client_hash)
print("HASH trên server:", server_hash)
if client_hash == server_hash:
    print("✅ File toàn vẹn")
else:
    print("❌ File bị lỗi")

conn.send(b'Done!')
conn.close()
