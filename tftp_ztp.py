
from fbtftp.base_handler import BaseHandler
from fbtftp.base_server import BaseServer
from netmiko import ConnectHandler
import time
import datetime
import sys
import os

## Matthew Bergersen Lewis   
## June 18th 2018            
## v1                        


#### TFTP SETTINGS ########
LISTEN_ON = '0.0.0.0'
SERVER_PORT = 69
TFTP_ROOT = '/opt/ztp/tftproot'
RETRIES = 3
TIMEOUT = 5
#### TFTP SETTINGS ########

"    ############     ##########     ##########     ##             ##########\n     ##########       ########      #########      ##              ########\n         ##                         ##             ##\n         ##                         ##             ##\n         ##          ##########     ##########     ##             ##########\n         ##           ########      ##########     ##             ##########\n         ##                                 ##     ##             ##      ##\n         ##                                 ##     ##             ##      ##\n         ##          ##########      #########     ##########     ##      ##\n         ##           ########      ##########     #########      ##      ##\n\n########################################################################################\n# This computer system is the property of Tesla Motors and may be accessed only        #\n# by authorized users. Tesla Motors, reserves the right to monitor any activity or     #\n# communication on this system and retrieve any information stored within this system. # \n# By accessing and using this system, you are consenting to such monitoring and        #\n# information retrieval for law enforcement and other purposes.                        #\n# Unauthorized use of this system is strictly prohibited and may be subject to         #\n# disciplinary actions including criminal prosecution.                                 #\n########################################################################################\n";

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
        print('    ############     ##########     ##########     ##             ##########\n     ##########       ########      #########      ##              ########\n         ##                         ##             ##\n         ##                         ##             ##\n         ##          ##########     ##########     ##             ##########\n         ##           ########      ##########     ##             ##########\n         ##                                 ##     ##             ##      ##\n         ##                                 ##     ##             ##      ##\n         ##          ##########      #########     ##########     ##      ##\n         ##           ########      ##########     #########      ##      ##\n\n########################################################################################\n# This computer system is the property of Tesla Motors and may be accessed only        #\n# by authorized users. Tesla Motors, reserves the right to monitor any activity or     #\n# communication on this system and retrieve any information stored within this system. # \n# By accessing and using this system, you are consenting to such monitoring and        #\n# information retrieval for law enforcement and other purposes.                        #\n# Unauthorized use of this system is strictly prohibited and may be subject to         #\n# disciplinary actions including criminal prosecution.                                 #\n########################################################################################\n')
        print('')
        print('TFTP PROCESS IS RUNNING, DO NOT EXIT SCRIPT.')
        print('#' * 60)
        print('Peer: {} UDP/{}'.format(stats.peer[0], stats.peer[1]))
        print('File: {}'.format(stats.file_path))
        print('Sent Packets: {}'.format(stats.packets_sent))
        print('#' * 60)
        #### ^^ DISPLAY TFTP ACTIVITY ^^ #########

        print('Please wait, once base templete is loaded more dialog will be provided.')
        ssh_client = stats.peer[0]
        device = ConnectHandler(device_type='cisco_ios', ip=10.180.235.101', username='staging', password='stagingGF')
        client_version = device.send_command_expect("show version | begin Switch")
        print('*' * 60)
        print('Current Version of IOS on: ' + ssh_client + ':\n' + client_version )
        output = device.read_until_prompt()
        print('Sending command archive download-sw /overwrite tftp://192.168.1.10/ie2000-universalk9-tar.152-4.EA5.tar to the staging switch')
        print(output)
    except (EOFError, SSHException):
        print(ssh_client + ': The template is still being downloaded, please wait')

def main():
    server = TftpServer(LISTEN_ON, SERVER_PORT, RETRIES, TIMEOUT)
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()
check_version = device.send_command_expect('show version | include System image file is "sdflash:/ie2000-universalk9-mz.152-4.EA5/ie2000-universalk9-mz.152-4.EA5.bin"')

if __name__ == '__main__':
    main()
