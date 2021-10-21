import psutil
import logging
from time import strftime, time, sleep
from datetime import datetime
from colorama import init, Fore, Style
import sched

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
    '117.52.35.79',     # Asia client
    '117.52.35.179',    # Asia client
]
other = [
    '127.0.0.1',        # localhost
]
static_ips = global_client + EU_client + NA_client + Asia_client + other

init()
s = sched.scheduler(time, sleep)

last_ip = 0
the_ip = 0
last_time = 0
def print_ip():
    s.enter(update_interval, 1, print_ip)
    d2r_pid = 0
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            d2r_pid = proc.pid
            break
    if d2r_pid:
        p = psutil.Process(d2r_pid)
    else:   
        # game is not running
        return
    global last_ip
    global the_ip
    global last_time
    region = '?'
    for c in p.connections('tcp'):
        if (c.raddr):
            ip = c.raddr.ip
            if(ip in EU_client):
                region = 'EU'
            if(ip in NA_client):
                region = 'NA'
            if(ip in Asia_client):
                region = 'Asia'
            if(ip not in static_ips):
                the_ip = ip
    if(the_ip!=last_ip):
        logging.info('{}, {}'.format(region, the_ip))
        last_ip = the_ip
        last_time = time()
    msg = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    if last_time>0 and time()-last_time>=60:
        print(Fore.GREEN + msg + Style.RESET_ALL, end="\r", flush=True)
    else:
        print(msg, end="\r", flush=True)

s.enter(0, 1, print_ip)
s.run()
