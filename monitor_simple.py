#-*- coding: utf-8 -*-
import config
import requests


def mail(nguoi_nhan, tieu_de, noi_dung):
	import smtplib
	TO = nguoi_nhan
	SUBJECT = tieu_de
	TEXT = noi_dung
	# Gmail Sign In
	# gmail_sender = 'liles125876@gmail.com'
	# gmail_passwd = 'khachuy2705'
	gmail_sender = config.username_sender
	gmail_passwd = config.password_sender

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	# server.starttls()
	server.login(gmail_sender, gmail_passwd)

	BODY = '\r\n'.join(['To: %s' % TO,
	                    'From: %s' % gmail_sender,
	                    'Subject: %s' % SUBJECT,
	                    '', TEXT]).encode('utf-8')
	try:
		server.sendmail(gmail_sender, TO.split(','), BODY)
		print('Email da duoc gui di')
	except Exception as values:
		print(values)
		print('Co loi trong qua trinh gui mail')
	server.quit()

def check_ping(target):
	import os
	if os.name == 'nt':
		rep = os.system("ping -n 1 " + target + '> nul')
		if rep == 0:
			mess = "Ping " + str(target) + " thanh cong"
			print(mess)
			return [1, mess]
		else:
			mess = "Mat ket noi toi " + target
			print(mess)
			return [0, mess]
	else:
		rep = os.system("ping -c 1 " + target)
		if rep == 0:
			mess = "Ping " + str(target) + " thanh cong"
			print(mess)
			return [1, mess]
		else:
			mess = "Mat ket noi toi " + target
			print(mess)
			return [0, mess]

def check_port(host, port):
	import socket
	host=str(host)
	port=int(port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(10) 
	result = sock.connect_ex((host,port))
	if result == 0:
		mess="Ket noi toi "+host+":"+str(port)+" thanh cong"
		print(mess)
		return [1, mess]
	else:
		mess="Ket noi toi "+host+":"+str(port)+" that bai"
		print(mess)
		return [0, mess]
		
def http_check(url, timeout=30):
	"""url phai co http hoac https ơ dau"""
	import requests
	#headers={'Host':'Gi cung duoc'}
	response=requests.get(url, timeout=timeout)
	if response.status_code == 200:
		mess="Ket noi toi "+url+" thanh cong"
		print(mess)
		return [1, mess]
	else:
		mess = "Ket noi toi " + url + " that bai"
		print(mess)
		return [0, mess]


def check_internet():
	"""tra ve True neu co internet, tra ve fail neu khong co internet"""
	chk=check_ping('8.8.8.8')
	if chk[0]==1:
		return True
	else:
		return False
		
def getnow(arg):
	import datetime
	"""nếu arg= int thì trả về số thôi, nếu arg = time thì trả về định dạng ngày tháng, nếu không thì return False"""
	if arg=='int':
		now=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		return int(now)
	elif arg == 'time':
		now = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S ")
		return str(now)
	else:
		return False
		
def check_port_list(lists):
	"""check list port sau do canh bao"""
	for tmp in lists:
		host_tmp=tmp.split(':')
		result=check_port(host=host_tmp[0],port=host_tmp[1])
		if result[0]==0:
			mail(config.list_email,'Canh bao check port that bai',result[1])
			noi_dung = str(getnow('int')) + "|-|" + getnow('time') + result[1]
			print(noi_dung)
			# a=rpush(noi_dung)
			# print(a)
			# telegram_send(result[1])
		else:
			continue

def check_ping_list(lists):
	"""Check list cac host can ping, sau do canh bao"""
	for tmp in lists:
		result=check_ping(tmp)
		if result[0]==0:
			mail(config.list_email,'Canh bao check ping that bai',result[1])
			# telegram_send(result[1])
			noi_dung = str(getnow('int')) + "|-|" + getnow('time') + result[1]
			print(noi_dung)
			# rpush(noi_dung)
		else:
			continue

def check_link_lists(lists):
	"""Check cac link được cấu hình trong config.py"""
	for tmp in lists:
		result=http_check(tmp)
		if result[0]==0:
			mail(config.list_email,'Canh bao check ping that bai',result[1])
			# telegram_send(result[1])
			noi_dung = str(getnow('int')) + "|-|" + getnow('time') + result[1]
			print(noi_dung)
			# rpush(noi_dung)
		else:
			continue
			
			
if __name__ == '__main__':
	import threading
	if check_internet():
		linkck = threading.Thread(target=check_link_lists, args=(config.list_url,))
		pingck = threading.Thread(target=check_ping_list, args=(config.list_check_ping,))
		portck = threading.Thread(target=check_port_list, args=(config.list_check_port,))
		linkck.start()
		pingck.start()
		portck.start()
		linkck.join()
		pingck.join()
		portck.join()