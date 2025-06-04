from flask import Flask, request, send_file, render_template
import socket
import hashlib

app = Flask(__name__)

def send_file_over_socket(filepath):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5001))

    # Gửi file
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            client.send(chunk)
    client.send(b'__done__')

    # Gửi SHA-256
    sha256 = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
    client.send(sha256.encode())

    # Đợi phản hồi
    client.recv(1024)
    client.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    path = f"uploads/{uploaded_file.filename}"
    uploaded_file.save(path)

    send_file_over_socket(path)
    return f"✅ Đã gửi file: {uploaded_file.filename}. <a href='/download'>Tải file nhận được</a>"

@app.route('/download')
def download():
    return send_file("received/received_file", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
