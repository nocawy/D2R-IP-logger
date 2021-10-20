import psutil
from  ipaddress import ip_interface
import threading
import logging
from time import strftime, time
from datetime import datetime
from colorama import init, Fore, Back, Style

process_name = 'D2R.exe'
update_interval = 1     # refresh rate in seconds
logfile = 'D2R_ip_{}.log'.format(strftime('%Y-%m-%d'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(message)s', datefmt='%Y-%m-%d, %H:%M:%S',
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler()
    ]
)
init()

global_client = [
    '24.105.29.76',     # client
    '34.117.122.6',     # client
]
EU_client = [
    '37.244.28.80',     # EU client
    '37.244.28.180',    # EU client
    '37.244.54.10',     # EU client
]
NA_client = [
    '137.221.106.88',   # NA client
    '137.221.106.188',  # NA client
    '137.221.105.152',  # NA client
]
Asia_client = [
    '117.52.35.45',     # Asia client
    '117.52.35.179',    # Asia client
]
other = [
    '127.0.0.1',        # localhost
]

static_ips = global_client + EU_client + NA_client + Asia_client + other

last_ip = 0
region = '?'
last_time = 0
def printip():
    t = threading.Timer(update_interval, printip)
    t.daemon = True
    t.start()
    d2r_pid = 0
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            d2r_pid = proc.pid
    if d2r_pid:
        p = psutil.Process(d2r_pid)
    else:
        return
    # for c in p.connections('tcp'):
    #     print(c)
    global last_ip
    global region
    global last_time
    for c in p.connections('tcp'):
        if (c.raddr):
            ip = c.raddr.ip
            # print(ip)
            if(ip in EU_client):
                region = 'EU'
            if(ip in NA_client):
                region = 'NA'
            if(ip in Asia_client):
                region = 'Asia'
            if(ip not in static_ips and ip!=last_ip):
                logging.info('{}, {}'.format(region, ip))
                # logging.info(ip)
                last_ip = ip
                last_time = time()
    print(datetime.now().strftime('%Y-%m-%d, %H:%M:%S'), end="\r", flush=True)
    # if last_time>0 and time() - last_time >= 60:
    #     print(Fore.GREEN + datetime.now().strftime('%Y-%m-%d, %H:%M:%S'), end="\r", flush=True)
    # else:
    #     print(Style.RESET_ALL + datetime.now().strftime('%Y-%m-%d, %H:%M:%S'), end="\r", flush=True)

printip()
