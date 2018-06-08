import socket
import fcntl
import struct
from twisted.internet.protocol import Protocol

import time

from Support.Commandos import *

class NetworkClient(Protocol):
    def __init__(self, port: int, addr: str = '',interface = 'eth0'):
        self.ip = self.get_ip_address(interface)
        print(self.ip)
        self.port = port

        if addr is not '' and len(addr.split('.')) == 4:
            _,ipTemplate,ipParts = self.getIPParts(addr)
            ip = self.checkServer(ipParts[3],ipTemplate)
            if ip != '':
                print(f"Found server at {ip}")
                self.server_addres = addr
            else:
                self.server_addres = self.getServer()
        else:
            self.server_addres= self.getServer()

    def getServer(self) -> tuple:
        ipList,ipTemplate,_ = self.getIPParts(self.ip)

        while True:
            for i in ipList:
                ip = self.checkServer(i,ipTemplate)
                if ip != '':
                    print(f"Found server at {ip}")
                    return ip
            print("Cannot find a valid server!")
            time.sleep(10)

    def checkServer(self,i,ipTemplate):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, 0))
        print("Checking address {0}".format(ipTemplate.format(i)))
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((ipTemplate.format(i), self.port))
        if result is 0:
            sock.close()
            return ipTemplate.format(i)
        sock.close()
        return ''

    def getIPParts(self,ip):
        ipList = range(0, 256)
        ipParts = ip.split(".")
        ipTemplate = ipParts[0] + '.' + ipParts[1] + '.' + ipParts[2] + '.{0}'

        return ipList,ipTemplate,ipParts

    def sendMessage(self,msg : str):
        self.transport.write(msg.encode())

    def dataReceived(self,data):
        print(data)
        for process in self.registeredProcesses:
            process.put_message(data)

    def registerProces(self, process):
        try:
            self.registeredProcesses.append(process)
        except AttributeError:
            self.registeredProcesses = [process]

    def get_ip_address(self,ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack(b'256s', str.encode(ifname[:15]))
        )[20:24])

    def connectionMade(self):
        print("Client connected!")
        for process in self.registeredProcesses:
            process.put_message(str.encode(cmd_client_connected[0]))


