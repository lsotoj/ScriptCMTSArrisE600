import netmiko
import paramiko
import getpass
import logging
import socket
import csv
import os


exceptions = (paramiko.ssh_exception.SSHException,netmiko.ssh_exception.NetMikoTimeoutException, netmiko.ssh_exception.NetMikoAuthenticationException, socket.timeout, socket.error, ValueError, EOFError)
global directorio

directorio = os.getcwd()

devices = open('devices.txt','r')
devices = devices.read()
devices = devices.strip().splitlines()

logs = open('Errors.txt', 'w')

username = ''
password = ''

b = directorio + '/sh_cm/' + 'sh_cm' + '.csv'
f=open(b,'w')

for device in devices:
	try:
		connection = netmiko.ConnectHandler(ip=device, device_type='linux', username=username, password=password)
		print ('SSH To: ' + device)
	except exceptions as exception_type:
		print('Unable to Connect to: ' + device)
		logs.write(device + '\n')
		continue

	
	name = connection.find_prompt()

	connection.send_command('configure no pagination', expect_string = '[#\?$]')		
	output= connection.send_command('show cable modem', expect_string = '[#\?$]')
	output=output.split('\n')

	for x in output:
		a=str(x)
		if 'Total' in a:
			break
		a=a.replace("     ",",")        
		a=a.replace("    ",",")
		a=a.replace("   ",",")
		a=a.replace("  ",",")
		a=a.replace(" ",",")
		a=a.replace(",,",",")
		a=a.replace(",,",",")
		f.write(name + ',' + a + '\r\n')
		continue

f.close()
print('LISTADO TERMIANDO')