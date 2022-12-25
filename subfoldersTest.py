import re
import socket
import os
import threading
CHUNKSIZE = 1_000_000

def download_By_ContentLength(link):
    # host = "web.stanford.edu"
    # path = "/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt"
    # orilink ="http://web.stanford.edu/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt"
    # erase "http://"
    host, name, path = splitLink(link)
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

    data=data[data.find(b'\r\n\r\n')+4:]
    dest_folder, file_name = createFolder(host, name , path)

    
    count=len(data)
        
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

    print("saving to: "+file_name)


    with open(file_name, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    with open(file_name, 'ab') as f:
        while count<content_length:
            data = s.recv(2000000)
            count=count+len(data)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

    s.close()

def typeofFile(link):
    bool = False

    toF=[".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".apsx", ".pptx", ".pptm", ".ppsx", ".ppsm", ".html", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".net"]

    for i in toF:
        if i in link:
            bool = True

    return bool
    
def splitLink(link):
    if(link.find("http://")!=-1):
        link=link[len("http://"):]
    if(link.find("https://")!=-1):
        link=link[len("https://"):]

    link = link.rstrip('/')

    host=''
    name=''
    path=''

    if(link.find('/', link.find('//') + 2) == -1):
        if link.find('http://')== -1 and link.find('https://')== -1:
            host=link[:]
        else:
            host=link[link.find('//') + 2: link.find('/', link.find('//') + 2)]
    else:
        if(link.find('http://')== -1) and (link.find('https://')== -1):
            host=link[: link.find('/', link.find('//') + 2)]
        else:
            host=link[link.find('//') + 2: link.find('/', link.find('//') + 2)]
        name=link[link.rfind('/') + 1:]
        path=link[link.find('/', link.find('//') + 2):]

    if(path==""):
        path=path+"/"
    return host, name, path

def createFolder(host, name, path):
    dest_folder= host +"_download"

    rename= host
    if(name ==''):
        rename = host + "_index.html"
    else:
        rename = host + "_" + name
    
    file_path = os.path.join(dest_folder, rename)
    return dest_folder, file_path 

def download_By_ChunkEncoding(link):
    # host = "google.com"
    # path = ""
    # orilink ="http://www.google.com" -> name = ""
    # orilink ="http://www.google.com/" -> name = "index.html"
    # orilink ="http://web.stanford.edu/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt" -> name =Intro_Net_91407.ppt
    #chunk_size = 4096
    
    host, name, path = splitLink(link)
    dest_folder, file_name = createFolder(host, name, path)

    
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

    # socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))
    

    request = "GET " + path + " HTTP/1.1\r\nHost:" + \
        host + "\r\nConnection: keep-alive\r\n\r\n"
    s.sendall(request.encode())

    # header download
    header = ""
    while not header.endswith('\r\n\r\n'):
        header += s.recv(1).decode()
    header = header[0:header.find('\r\n\r\n')]
    # print(header)
    # print('-------------------------------------------------------------------------------------------------')

    BUFFER_SIZE = 1024 * 2
    with open(file_name, 'wb') as f:
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

def download_Folder(link):
    host, name, path = splitLink(link)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))

    input = link

    request = "GET " + path + "/ HTTP/1.1\r\nHost:" + \
        host + "\r\nConnection: keep-alive\r\n\r\n"
    s.sendall(request.encode())

    data = s.recv(1000)
    header=data[0:data.find(b'\r\n\r\n')]
    temp=header.decode()


    if(temp.find("Content-Length")!=-1):
        temp = temp[temp.find("Content-Length: ") + len("Content-Length: "): temp.find("\r\n", temp.find("Content-Length"))]

        content_length=int(temp)

        data=data[data.find(b'\r\n\r\n')+4:]
        count=len(data)

        while count <=content_length:
            my_dict = re.findall('(?<=<a href=")[^"]*', str(data))
        
            for x in my_dict:
            
                if typeofFile(x):
                    download_By_ContentLength(link + x)
            
            data = s.recv(1024*20)
            if(count==content_length):
                break
            count=count+len(data)
            
            
            
        print('Saving completed')
        s.close()
    else:
        host, name, path = splitLink(link)
        file_name = ''
        dest_folder= ''
        dest_folder, file_name = createFolder(host, name, path)
        header = ""
        while not header.endswith('\r\n\r\n'):
            header += s.recv(1).decode()
        header = header[0:header.find('\r\n\r\n')]
        # print(header)
        # print('-------------------------------------------------------------------------------------------------')

        BUFFER_SIZE = 1024 * 2
        with open(file_name, 'wb') as f:
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
                            #print(data)
                            my_dict = re.findall('(?<=<a href=")[^"]*', str(data))
                            for x in my_dict:
                            
                                if typeofFile(x):
                                    download_By_ContentLength(link + x)

                            n -= len(data)
                            if n + 2 == 0:
                                break
                        print('Saving...')
                except:
                    pass
                if chunk_size <= 0:
                    break
        print('Saving completed')

def check_File_or_Folder(link):
    if typeofFile(link)==False and link[len(link)-1]=="/":
        return True #Folder
    return False #File

def download_File(link):
    host, name, path = splitLink(link)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))

    input = link

    request = "GET " + path + "/ HTTP/1.1\r\nHost:" + \
        host + "\r\nConnection: keep-alive\r\n\r\n"
    s.sendall(request.encode())

    data = s.recv(1000)
    header=data[0:data.find(b'\r\n\r\n')]
    temp=header.decode()


    if(temp.find("Content-Length")!=-1):
        download_By_ContentLength(link)
    else:
        download_By_ChunkEncoding(link)



def main():
    link = input()
    arr= link.split(" ")
    threads = list()
    for index in range(len(arr)):
        print("Main    : create and start thread %d.", index)
        if(check_File_or_Folder(arr[index])==True):
            x = threading.Thread(target=download_Folder, args=(arr[index],))
        else:
            x = threading.Thread(target=download_File, args=(arr[index],))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        print("Main    : before joining thread %d.", index)
        thread.join()
        print("Main    : thread %d done", index)

if __name__ == '__main__':
    main()