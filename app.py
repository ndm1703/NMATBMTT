from flask import Flask, render_template, request, jsonify
from crypto import encrypt_message
import socket

app = Flask(__name__)

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/send', methods=['POST'])
def send():
    msg = request.form['message']
    key = request.form['key']
    encrypted = encrypt_message(msg, key)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 9999))
            s.sendall(encrypted.encode())
        return jsonify({'status': 'success', 'encrypted': encrypted})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

