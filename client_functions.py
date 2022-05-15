import os
import socket
import sys


def send_requests():
    cache = dict()
    if len(sys.argv) == 2:
        f = open(sys.argv[1])
    else:
        f = open('requests.txt')
    for request in f:
        request_type, file_name, host_name, PORT, http_version = parse_request(request)
        if request_type == 'GET':
            request = generate_get_request(file_name, host_name, http_version)
        elif request_type == 'POST':
            request = generate_post_request(file_name, host_name, http_version)
        print(f'REQUEST:\n{request.decode()}\n')
        if request in cache.keys():
            print('CACHE HIT!\n')
            response = cache[request]
            if request_type == 'GET':
                handle_get_response(response, file_name, host_name, isCached=True)
            elif request_type == 'POST':
                handle_post_response(response)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host_name, PORT))
                s.sendall(request)
                response = s.recv(100000).decode('utf-8')
                cache[request] = response
                if request_type == 'GET':
                    handle_get_response(response, file_name, host_name)
                elif request_type == 'POST':
                    handle_post_response(response)
        print('-------------------------------------------\n\n')


def parse_request(request):
    http_version = 'HTTP/1.0'
    fields = request.split()
    request_type = fields[0]
    file_name = fields[1]
    host_name = fields[2]
    if len(fields) == 4:
        PORT = int(fields[3])
    else:
        PORT = 80
    return request_type, file_name, host_name, PORT, http_version


def generate_get_request(file_name, host_name, http_version):
    return bytes(f'GET {file_name} {http_version}\r\nHost:{host_name}\r\n\r\n', 'utf-8')


def generate_post_request(file_name, host_name, http_version):
    f = open(f'client{file_name}', 'rb')
    file_contents = f.read().decode('utf-8')
    return bytes(
        f'POST {file_name} {http_version}\r\nHost:{host_name}\r\n\r\n{file_contents}',
        'utf-8')


def create_host_directory(host_name):
    parent_dir = "D:/Networks/client"
    host_path = f'{parent_dir}/{host_name}'
    if not os.path.isdir(host_path):
        directory = host_name
        mode = 0o666
        path = os.path.join(parent_dir, directory)
        os.mkdir(path, mode)


def handle_get_response(response, file_name, host_name, isCached=False):
    response_status = response.split('\n')[0]
    print(F'RESPONSE STATUS:\n{response_status}\n')
    response_code = response_status.split()[1]
    if response_code == '200':
        body = response.split('\r\n\r\n')[1]
        print(f'BODY:\n{body}')
        if not isCached:
            create_host_directory(host_name)
            if file_name == '/':
                file_name = '/index.html'
            f = open(f'client/{host_name}/{file_name}', 'wb')
            f.write(bytes(body, 'utf-8'))
            print('FILE WRITTEN TO CLIENT SUCCESSFULLY\n')
    elif response_code == '404':
        print(f'{file_name} at {host_name} Not Found\n')


def handle_post_response(response):
    print(response)
