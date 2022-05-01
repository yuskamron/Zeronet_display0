from ping3 import ping
import re
import os
import requests
import glob
import fileinput

tracker_address = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
ipbox = list()

def ping_test(ip):
	result = ping(ip, unit='ms')
	if result == None:
		result = 0
		return result
	else:
		result = round(result, 2)
		return result
def tracker_list():
	f = open("tracker", "w")
	with open("trackers.json", "r") as tracker:
		while True:
			line = tracker.readline()
			if line == '':
				break;
			address = tracker_address.findall(line)
			for ip in address:
				f.write(f"{ip}\n")
		
def tor_node_list():
	req = requests.get("https://check.torproject.org/exit-addresses")
	req_lines = req.text.split("\n")
	
	with open("tor", "w") as node_file:
		for line in req_lines:
			if line.startswith("ExitAddress"):
				ip = line.split(" ")[1]
				node_file.write(f"{ip}\n")
		else:
			return True

def check_tor(ip):
	with open("tor", 'r') as tor_ip:
		if ip in tor_ip.read():
			return "True"
		else:
			return "False"
			
def check_tracker(ip):
	with open("tracker", 'r') as tracker_ip:
		if ip in tracker_ip.read():
			return "tracker"
		else:
			return "peer"

def user_data(ip):
	address = ip + "/"
	url = f"http://ipinfo.io/{address}json"
	response = requests.get(url)
	data =  response.json()
	return data

tracker_list()
tor_node_list()


directory = os.getcwd()
input_files = os.listdir(directory)
file_name = os.listdir(directory)
site = '16FBB4'
peer_check = 'Peer'
peer_check2 = 'peer'
ignore = ["127.0.0.1"]
ipbox = list()
site_address = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")


for filename in input_files:
	if "debug" not in filename:
		continue
	
	f = open(directory + '/' + filename)
	while True:
		line = f.readline()
		site_true = None
		site_true = site in line
		peer_true = None
		peer_true = peer_check in line
		peer_true2 = None
		peer_true2 = peer_check2 in line
		if line == '':
			break
		
		if site_true == True:
			if peer_true == True:
				address = site_address.findall(line)
				for ip in address:
					ipbox.append(ip)
					
		if site_true == True:
			if peer_true2 == True:
				address = site_address.findall(line)
				for ip in address:
					ipbox.append(ip)


ipbox = list(set(ipbox))
ipbox.sort()

g = open("peer", 'w')
for ip in ipbox:
    g.write(f"{ip}\n")

p = open("data", 'w')
for ip in ipbox:
	ping_result = ping_test(ip)
	tor = check_tor(ip)
	tracker = check_tracker(ip)
	data = user_data(ip)
	country = data['country']
	city = data['city']
	loc = data['loc']
	p.write(f"{ip} {tor} {tracker} {country} {city} {loc} {ping_result} \n")

	

p.close()
g.close()

exec(open("packet.py").read())
