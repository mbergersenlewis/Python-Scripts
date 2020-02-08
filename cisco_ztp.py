from netmiko import ConnectHandler
import time

device = ConnectHandler(device_type='cisco_ios', ip='10.180.235.101', username='staging', password='stagingGF')
current_version = device.send_command_expect('show version | include System image file')
#print( ssh_client + ": DOWNLOAD OF NEW IMAGE HAS STARTING... THIS PROCESS TAKES ABOUT 10 MINUTES" + device.send_command_expect("archive download-sw /overwrite ftp://10.34.6.8/packages/ie2000-universalk9-tar.152-4.EA5.tar", delay_factor=10))


if current_version == 'System image file is "sdflash:/ie2000-universalk9-mz.152-4.EA8/ie2000-universalk9-mz.152-4.EA8.bin"' or current_version == 'System image file is "flash:/ie2000-universalk9-mz.152-4.EA8/ie2000-universalk9-mz.152-4.EA8.bin"':
	print(ssh_client + ' has successfully loaded ie2000-universalk9-mz.152-4.EA8... DISCONNECTING FROM SWITCH')
	device.disconnect()
elif current_version != 'System image file is "sdflash:/ie2000-universalk9-mz.152-4.EA8/ie2000-universalk9-mz.152-4.EA8.bin"' or current_version != 'System image file is "flash:/ie2000-universalk9-mz.152-4.EA8/ie2000-universalk9-mz.152-4.EA8.bin"':
	device.send_command('write memory', delay_factor=10)
	print(ssh_client + ": DOWNLOAD OF NEW IMAGE HAS STARTING... THIS PROCESS TAKES ABOUT 12 MINUTES" + device.send_command_expect("archive download-sw /overwrite /reload ftp://10.34.6.8/packages/ie2000-universalk9-tar.152-4.EA8.tar", delay_factor=10))
    time.sleep(10)
	print(ssh_client + " --> RELOADING SWITCH SO NEW IMAGE CAN BE USED")
	#device.send_command('write memory', delay_factor=10)
	#device.send_command('reload', expect_string='confirm')
	#device.send_command('\n')
else:
	print("THIS SHOULD NEVER MATCH, SOMETHING WENT WRONG.")
