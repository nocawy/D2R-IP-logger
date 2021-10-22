import psutil
import logging
from time import strftime, time, sleep
from datetime import datetime
from colorama import init, Fore, Style
from sched import scheduler

update_interval = 1     # refresh rate in seconds; setting lower than 1 might be pointless because the process of checking connections takes close to 1s
logfile = 'D2R_ip_{}.log'.format(strftime('%Y-%m-%d'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(message)s', datefmt='%Y-%m-%d, %H:%M:%S',
    handlers=[
        logging.FileHandler(logfile),   # remove this line to stop logging to a file
        logging.StreamHandler()
    ]
)

global_client = [
    '24.105.29.76',     # client
    '34.117.122.6',     # client
    '127.0.0.1',        # localhost
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

init()  # colorama initialisation
s = scheduler(time, sleep)

previous_ip = 0
current_game_ip = 0
previous_time = 0
def print_ip():
    s.enter(update_interval, 1, print_ip)   # run this function every update_interval
    d2r_pid = 0
    # find D2R process
    for proc in psutil.process_iter():
        if proc.name() == 'D2R.exe':
            d2r_pid = proc.pid
            break
    if d2r_pid:
        p = psutil.Process(d2r_pid)
    else:   
        # if game is not running
        return
    global previous_ip
    global current_game_ip
    global previous_time
    region = '?'
    for c in p.connections('tcp'):
        if (c.raddr):
            ip = c.raddr.ip
            if(ip in EU_client):
                region = 'EU'
            elif(ip in NA_client):
                region = 'NA'
            elif(ip in Asia_client):
                region = 'Asia'
            elif(ip not in global_client):
                current_game_ip = ip
    if(current_game_ip!=previous_ip):
        # found a new game ip, log it
        print(' '*44, end="\r", flush=True) #clear line
        logging.info('{}, {}'.format(region, current_game_ip))
        previous_ip = current_game_ip
        previous_time = time()
    # display clock, coloured green if more then 1 minute passed since last game creation:
    msg = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    info = ' (press CTRL+C to exit)'
    if previous_time>0 and time()-previous_time>=60:
        print(Fore.GREEN + msg + Style.RESET_ALL + info, end="\r", flush=True)
    else:
        print(msg + info, end="\r", flush=True)

s.enter(0, 1, print_ip)
try:
    s.run()
except KeyboardInterrupt:
    print() # newline on exit
    pass
