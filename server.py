import socket
from crypto import decrypt_message

HOST = 'localhost'
PORT = 9999
KEY = "123abc"  # Key cố định cho demo

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[🟢] Đang lắng nghe tại {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[📥] Kết nối từ {addr}")
            data = conn.recv(1024)
            if data:
                encrypted = data.decode()
                print(f"[🔒 Tin nhắn mã hóa]: {encrypted}")
                try:
                    decrypted = decrypt_message(encrypted, KEY)
                    print(f"[🔐 Tin nhắn đã giải mã]: {decrypted}")
                except Exception as e:
                    print(f"[❌] Giải mã thất bại. Dữ liệu: {encrypted}")
                    print(f"Lỗi: {e}")