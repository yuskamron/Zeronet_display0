from http.client import IM_USED
import os,re

from django.shortcuts import render

from . import crawler_library

# Create your views here.
def main(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    res_data = {}
    
    return render(request, 'main.html',res_data)

def crawler(request):
    res_data = {}
    path_base = os.getcwd()+"/board/crawler_data/"
    
    # 크롤링하는 과정(main)
    crawler_library.tracker_list()
    crawler_library.tor_node_list()
    directory = os.getcwd()+"/board/crawler_data/"
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
        f = open(directory + filename)
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
                        
    a_ipbox = list(set(ipbox))
    a_ipbox.sort()
    
    g = open(path_base+"peer", 'w')
    for ip in a_ipbox:
        g.write(f"host {ip} or ")
    
    im_d = []
    boards = []

    

    p = open(path_base+"data", 'w')
    for ip in a_ipbox:
        im_d = []
        tor = crawler_library.check_tor(ip)
        tracker = crawler_library.check_tracker(ip)
        data = crawler_library.user_data(ip)
        country = data['country']
        city = data['city']
        loc = data['loc']

        im_d.append(ip)
        im_d.append(tor)
        im_d.append(tracker)
        im_d.append(country)
        im_d.append(city)
        im_d.append(loc)
        boards.append(im_d)
        p.write(f"{ip} {tor} {tracker} {country} {city} {loc} \n")
    
    
        

    p.close()
    g.close()
    del im_d
    
    return render(request,'crawler.html',{'boards':boards})

def traffic(request) :

    path_base = os.getcwd()+"/board/crawler_data/"
    traffic = [] # this list is for storing data from traffic.crash
    traffic_list = [] # this list is for binding all information derived from traffic list

    f = open(path_base+"traffic.crash", 'r')

    while True:
        if line == '':
                break
        line = f.readline()
        local_time_date = line.split(" ")[1]
        local_time = line.split(" ")[2]
        proto_T = line.split(" ")[3]
        layer_v = line.split(" ")[4]
        src_ip = line.split(" ")[5]
        dst_ip = line.split(" ")[6]
        pkt_size = line.split(" ")[7]

        traffic.append(local_time_date)
        traffic.append(local_time)
        traffic.append(proto_T)
        traffic.append(layer_v)
        traffic.append(src_ip)
        traffic.append(dst_ip)
        traffic.append(pkt_size)

        traffic_list.append(traffic)
        
    return render(request, 'traffic.html', {traffic: 'traffics'})
