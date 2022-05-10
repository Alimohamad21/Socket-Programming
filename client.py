import os
import socket

PORT = 80
f = open('requests.txt')
for request in f:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        fields = request.split()
        request_type = fields[0]
        file_name = fields[1]
        host_name = fields[2]

        if len(fields) == 4:
            PORT = 80
            version_no = fields[3]
        else:
            PORT = fields[3]
            version_no = fields[4]
        s.connect((host_name, PORT))
        if request_type == 'GET':
            request = f'GET {file_name} {version_no}\r\nHost:{host_name}\r\n\r\n'
            print(request)
            s.sendall(bytes(request, 'utf-8'))
            data = s.recv(100000).decode('utf-8')
            print(data)
            data = data.split('\n')
            response_code = data[0].split()[1]
            if response_code == '200' and host_name != 'localhost':
                data = data[14:]
                data = '\n'.join(data)
                print(data)
                f = open(f'client{file_name}', 'wb')
                f.write(bytes(data, 'utf-8'))
            elif response_code == '200' and host_name == 'localhost':
                data = data[1:]
                data = '\n'.join(data)
                print(data)
                f = open(f'client{file_name}', 'wb')
                f.write(bytes(data, 'utf-8'))
            elif response_code == '404':
                print(f'{file_name} at {host_name} Not Found')
        elif request_type == 'POST':
            f = open(f'client{file_name}', 'rb')
            file_size = os.path.getsize(f"client{file_name}")
            print(f'file_size:{file_size}')
            file_contents = f.read().decode('utf-8')
            request = f'POST {file_contents} {version_no}\r\nHost:{host_name}\r\nContent-Type:text/plain\r\nContent-Length:{file_size}\r\n\r\n'
            print(request)
            s.sendall(bytes(request, 'utf-8'))
            print('HENA')
            data = s.recv(100000)
            print('MSH HENA')
            print(data.decode('utf-8'))
