import os
import socket
from socket import AF_INET, SOCK_STREAM, gethostbyname
host = "example.com"
path = "/index.html"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 80))


request = "GET "+path+" HTTP/1.1\r\nHost:"+host+"\r\nConnection: keep-alive\r\n\r\n"
s.sendall(request.encode())


data = s.recv(2000000)
header=data[0:data.find(b'\r\n\r\n')]
temp=header.decode()
temp=temp.split('Content-Length: ')[-1]
temp=temp.split('\r\n')[0]
content_length=int(temp)


haha = data


data=data[data.find(b'\r\n\r\n')+4:]
dest_folder="Download"
file_path = os.path.join(dest_folder, "Intro_Net_91407.txt")
 
count=len(data)
    
if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

with open(file_path, 'wb') as f:
    f.write(data)
    print(data)
    f.flush()
    os.fsync(f.fileno())
with open(file_path, 'ab') as f:
    while count<content_length:
        data = s.recv(2000000)
        count=count+len(data)
        f.write(data)
        print(data)
        f.flush()
        os.fsync(f.fileno())

s.close()

