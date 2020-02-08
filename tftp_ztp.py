from fbtftp.base_handler import BaseHandler
from fbtftp.base_server import BaseServer
from netmiko import ConnectHandler
import netmiko
from netmiko.ssh_exception import NetMikoTimeoutException
import time
import datetime
import sys
import os

## Matthew Bergersen Lewis   
## mbergersenlewis@tesla.com 
## June 18th 2018            
## v1                        


#### TFTP SETTINGS ########
LISTEN_ON = '0.0.0.0'
SERVER_PORT = 69
TFTP_ROOT = '/opt/ztp/tftproot'
RETRIES = 3
TIMEOUT = 5
#### TFTP SETTINGS ########

class TftpData:

    def __init__(self, filename):
        path = os.path.join(TFTP_ROOT, filename)
        self._size = os.stat(path).st_size
        self._reader = open(path, 'rb')

    def read(self, data):
        return self._reader.read(data)

    def size(self):
        return self._size

    def close(self):
        self._reader.close()


class StaticHandler(BaseHandler):

    def get_response_data(self):
        return TftpData(self._path)


class TftpServer(BaseServer):

    def get_handler(self, server_addr, peer, path, options):
        return StaticHandler(
            server_addr, peer, path, options, session_stats)


def session_stats(stats):
    try:
        #### DISPLAY TFTP ACTIVITY #########
#        print('    ############     ##########     ##########     ##             ##########\n     ##########       ########      #########      ##              ########\n         ##                         ##             ##\n         ##                         ##             ##\n         ##          ##########     ##########     ##             ##########\n         ##           ########      ##########     ##             ##########\n         ##                                 ##     ##             ##      ##\n         ##                                 ##     ##             ##      ##\n         ##          ##########      #########     ##########     ##      ##\n         ##           ########      ##########     #########      ##      ##\n\n########################################################################################\n# This computer system is the property of Tesla Motors and may be accessed only        #\n# by authorized users. Tesla Motors, reserves the right to monitor any activity or     #\n# communication on this system and retrieve any information stored within this system. # \n# By accessing and using this system, you are consenting to such monitoring and        #\n# information retrieval for law enforcement and other purposes.                        #\n# Unauthorized use of this system is strictly prohibited and may be subject to         #\n# disciplinary actions including criminal prosecution.                                 #\n########################################################################################\n')
        print('')
        print('TFTP PROCESS IS RUNNING, DO NOT EXIT SCRIPT.')
        print('#' * 60)
        print('# Active TFTP Peer: {} UDP/{}'.format(stats.peer[0], stats.peer[1]))
#        print('File: {}'.format(stats.file_path))
#        print('Sent Packets: {}'.format(stats.packets_sent))
        print('#' * 60)
        #### ^^ DISPLAY TFTP ACTIVITY ^^ #########
        ssh_client = stats.peer[0]
        device = ConnectHandler(device_type='cisco_ios', ip=ssh_client, username='staging', password='stagingGF')
        # grabbing switch version
        client_version = device.send_command_expect("show version | include System image file")
        version = client_version.split("/")
        version_index = version[1]
        # grabbing serial number of switch
        serial_number = device.send_command_expect('show version | include Motherboard serial').split(": ")
        if version_index != "ie2000-universal9-mz.152-4.EA8":
            print('#' * 10 + 'SUCCESSFULLY PROVISIONED: 'ssh_client +' : '+ serial_number[1] + '#' * 10)
            print(ssh_client + ' has successfully loaded ie2000-universal9-mz.152-4.EA8.bin... DISCONNECT THE SWITCH')
            device.disconnect()
        elif version_index == 'ie2000-universal9-mz.152-4.EA8':
            print("inside elif statement " + version[1])
            device.send_command('write memory', delay_factor=10)
            print(ssh_client +':' + serial_number[1] + "--> DOWNLOADING OF NEW IMAGE HAS STARTED... THIS PROCESS TAKES ABOUT 12 MINUTES" + device.send_command_expect("archive download-sw /overwrite /reload tftp://192.168.1.10/ie2000-universal9-tar.152-4.EA8.tar", delay_factor=10))
            time.sleep(10)
            print(ssh_client +':' + serial_number[1] + " --> RELOADING SWITCH SO NEW IMAGE CAN BE USED") 
        else:
            print("THIS SHOULD NEVER MATCH, SOMETHING WENT WRONG")
    except (NetMikoTimeoutException):
        print(ssh_client +':' + '--> The base template is still being downloaded, ssh key is being generated etc, please wait')
    except (FileNotFoundError):
        print(ssh_client +':' +'--> Switch is trying to open default files, please wait')

def main():
    server = TftpServer(LISTEN_ON, SERVER_PORT, RETRIES, TIMEOUT)
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    main()
