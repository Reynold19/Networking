import os
import requests
import socket

def download_By_ContentLength(link):
    # host = "web.stanford.edu"
    # path = "/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt"
    # orilink ="http://web.stanford.edu/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt"
    # erase "http://"
    link=link[7:]
    host = link[:link.find('/')]
    name = link[link.rfind('/')+1:]
    path = link[link.find('/'):]
    
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
    dest_folder= host +"_download"

    rename= host
    if(name ==''):
        rename = host + "_index.html"
    else:
        rename = host + "_" + name
    
    file_path = os.path.join(dest_folder, rename)
    
    count=len(data)
        
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

    print("saving to: "+file_path)


    with open(file_path, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    with open(file_path, 'ab') as f:
        while count<content_length:
            data = s.recv(2000000)
            count=count+len(data)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

    s.close()

##################################################################


def download_By_ChunkEncoding_Requests(link):
    # host = "google.com"
    # path = ""
    # orilink ="http://www.google.com" -> name = ""
    # orilink ="http://www.google.com/" -> name = "index.html"
    # orilink ="http://web.stanford.edu/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt" -> name =Intro_Net_91407.ppt
    chunk_size = 4096
    host=''
    name=''
    path=''

    link = link.rstrip('/')

    if(link.find('/', link.find('//') + 2) == -1):
        host=link[link.find('//') + 2:]
    else:
        host=link[link.find('//') + 2: link.find('/', link.find('//') + 2)]
        name=link[link.rfind('/') + 1:]
        path=link[link.find('/', link.find('//') + 2):]

    # filename = "goole.com.html"
    # document_url = "http://www.google.com"
    rename=''
    if(name==''):
        rename = host + '_index.html'
    else:
        if(name.find('.') == -1):
            rename = host + '_' + name + '.html'
        else:
            rename = host + '_' + name
    
    filename = rename
    document_url = link

    dest_folder = host + '_download'
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

    filename = os.path.join(dest_folder, filename)

    with requests.get(document_url, stream=True) as r:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())

##################################################################



def download_By_ChunkEncoding(link):
    # host = "google.com"
    # path = ""
    # orilink ="http://www.google.com" -> name = ""
    # orilink ="http://www.google.com/" -> name = "index.html"
    # orilink ="http://web.stanford.edu/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt" -> name =Intro_Net_91407.ppt
    #chunk_size = 4096
    host=''
    name=''
    path=''

    link = link.rstrip('/')

    if(link.find('/', link.find('//') + 2) == -1):
        host=link[link.find('//') + 2:]
    else:
        host=link[link.find('//') + 2: link.find('/', link.find('//') + 2)]
        name=link[link.rfind('/') + 1:]
        path=link[link.find('/', link.find('//') + 2):]

    rename=''
    if(name==''):
        rename = host + '_index.html'
    else:
        if(name.find('.') == -1):
            rename = host + '_' + name + '.html'
        else:
            rename = host + '_' + name
    
    filename = rename
    document_url = link

    dest_folder = host + '_download'
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

    filename = os.path.join(dest_folder, filename)

    # socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))
    if(path == ''):
        path = '/'

    request = "GET " + path + " HTTP/1.1\r\nHost:" + \
        host + "\r\nConnection: keep-alive\r\n\r\n"
    s.sendall(request.encode())

    # header download
    header = ""
    while not header.endswith('\r\n\r\n'):
        header += s.recv(1).decode()
    header = header[0:header.find('\r\n\r\n')]
    print(header)
    print('-------------------------------------------------------------------------------------------------')

    BUFFER_SIZE = 1024 * 2
    with open(filename, 'wb') as f:
        while True:
            try:
                # Get chunk size
                chunkSize_line = ""
                while not chunkSize_line.endswith('\n'):
                    chunkSize_line += s.recv(1).decode()
                chunkSize_line = chunkSize_line[0:chunkSize_line.find('\r\n')]
                chunk_size = int(chunkSize_line, 16)
                print('Chunk_size = ', chunk_size)

                # download and save chunked data
                if chunk_size > 0:

                    n = chunk_size
                    while True:
                        if n >= BUFFER_SIZE:
                            data = s.recv(BUFFER_SIZE)
                        else:
                            data = s.recv(n+2)
                       
                        f.write(data)
                        f.flush()

                        n -= len(data)
                        if n + 2 == 0:
                            break
                    
            except:
                pass
            if chunk_size <= 0:
                break
    
    s.close()




def main():
    link = input()
    #download_By_ContentLength(link)
    #download_By_ChunkEncoding_Requests(link)
    download_By_ChunkEncoding(link)

if __name__ == '__main__':
    main()
