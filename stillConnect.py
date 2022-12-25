from contextlib import closing
import os
import socket
from stat import S_ISSOCK
import sys


link = "http://www.google.com"

def checkPortsSocket(ip,portlist):
    try:
        for port in portlist:
            sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect((ip,port))
            if result == 0:
                print ("Port {}: \t Open".format(port))
            else:
                print ("Port {}: \t Closed".format(port))
            sock.close()
    except socket.error as error:
        print (str(error))
        print ("Connection error")
        sys.exit() 

portlist=[80]

def check_tcp_socket(host, port, s_timeout=2):
    if(host.find("http://")>= 0):
        host = host[host.find("http://")+7:]
    if (host.find("https://")>= 0):
        host = host[host.find("http://")+8:]

    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(s_timeout)
        tcp_socket.connect((host, port))
        tcp_socket.close()
        return True
    except (socket.timeout, socket.error):
        return False 

#print(checkPortsSocket(link, portlist))

print(check_tcp_socket(link, 80))