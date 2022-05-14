import socket


def handle_requests():
    HOST = 'localhost'
    PORT = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(100000)
                    if not data:
                        break
                    print(f'CLIENT REQUEST:\n{data.decode()}')
                    request_type, file_name, http_version, body = parse_client_request(data)
                    if request_type == 'GET':
                        handle_get_request(conn, file_name, http_version)
                    elif request_type == 'POST':
                        handle_post_request(conn, file_name, http_version, body)


def parse_client_request(client_request):
    client_request = client_request.decode('utf-8')
    fields = client_request.split('\n')[0].split()
    request_type = fields[0]
    file_name = fields[1]
    http_version = fields[2]
    body = ''
    if request_type == 'POST':
        body = client_request.split('\r\n\r\n')[1]
    return request_type, file_name, http_version, body


def handle_get_request(conn, file_name, http_version):
    try:
        f = open(f'server{file_name}', 'rb')
        file_contents = f.read().decode("utf-8")
        response = f'{http_version} 200 0K\r\n\r\n{file_contents}'
        conn.sendall(bytes(response, 'utf-8'))
        print('File transmitted to client successfully')
    except IOError:
        print('File not accessible')
        conn.sendall(bytes(f'{http_version} 404 Not Found\r\n', 'utf-8'))


def handle_post_request(conn, file_name, http_version, body):
    print(f'POSTED DATA:\n{body}\n')
    conn.sendall(bytes(f'{http_version} 200 OK\r\n', 'utf-8'))
    f = open(f'server{file_name}', 'wb')
    f.write(bytes(body, 'utf-8'))
    print('File written to server')
