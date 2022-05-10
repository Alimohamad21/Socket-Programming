import socket

HOST = 'localhost'
PORT = 80
WAITING_TIME = 10
version_no = ''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                decoded_data = data.decode('utf-8')
                fields = decoded_data.split('\n')[0].split()
                request_type = fields[0]
                file = fields[1]
                version_no = fields[2]
                if request_type == 'GET':
                    try:
                        f = open(f'server{file}', 'rb')
                        file_contents = f.read().decode("utf-8")
                        response = f'{version_no} 200 0K\r\n\r\n{file_contents}'
                        conn.sendall(bytes(response, 'utf-8'))
                        print('File transmitted to client successfully')
                    except IOError:
                        print('File not accessible')
                        conn.sendall(bytes(f'{version_no} 404 Not Found\r\n', 'utf-8'))
                elif request_type == 'POST':
                    conn.sendall(bytes(f'{version_no} 200 OK\r\n', 'utf-8'))
                    f = open(f'server{file}', 'wb')
                    f.write(bytes(file, 'utf-8'))
                    print('File written to server')
