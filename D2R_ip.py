import sys
import psutil
import logging
from time import strftime, time, sleep
from datetime import datetime
from colorama import init, Fore, Style
from sched import scheduler
from math import floor

update_interval = 1     # refresh rate in seconds; setting lower than 1 might be pointless because the process of checking connections takes close to 1s
logfile = 'D2R_ip_{}.log'.format(strftime('%Y-%m-%d'))
datetime_format = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(message)s', datefmt=datetime_format,
    handlers=[
        logging.FileHandler(logfile),   # remove this line to stop logging to a file
        logging.StreamHandler()
    ]
)

constant_ips = [
    '24.105.29.76',     # always open
    '34.117.122.6',     # always open
    '127.0.0.1',        # localhost
    '137.221.105.152',  # Americas lobby
    '37.244.54.10',     # Europe lobby
    '117.52.35.45',     # Asia lobby
]
# regions = [
#     '137.221.106.88',   # Americas
#     '137.221.106.188',  # Americas
#     '37.244.28.80',     # Europe
#     '37.244.28.180',    # Europe
#     '117.52.35.79',     # Asia
#     '117.52.35.179',    # Asia
# ]

init()  # colorama initialisation
s = scheduler(time, sleep)

previous_ip = 0
current_game_ip = 0
previous_time = time()
hunting_ip=''

print("D2R IP Logger started. To exit press CTRL+C")
if len(sys.argv) >= 2:
    print('Hunting for ip: ' + Fore.LIGHTRED_EX + sys.argv[1] + Style.RESET_ALL)
    hunting_ip = sys.argv[1]

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
    subregion = '?'
    for c in p.connections('tcp'):
        if (c.raddr):
            ip = c.raddr.ip
            if(ip == '37.244.28.80'):
                region = 'Europe'
                subregion = '80'
            elif(ip == '37.244.28.180'):
                region = 'Europe'
                subregion = '180'
            elif(ip == '137.221.106.88'):
                region = 'Americas'
                subregion = '88'
            elif(ip == '137.221.106.188'):
                region = 'Americas'
                subregion = '188'
            elif(ip == '117.52.35.79'):
                region = 'Asia'
                subregion = '79'
            elif(ip == '117.52.35.179'):
                region = 'Asia'
                subregion = '179'
            elif(ip not in constant_ips):
                current_game_ip = ip
    if(current_game_ip!=previous_ip):
        # found a new game ip, log it
        print(' '*44, end="\r", flush=True) #clear line
        if current_game_ip == hunting_ip:
            print(Fore.LIGHTRED_EX, end="\r", flush=True)
        logging.info('{},{}, {}'.format(region, subregion, current_game_ip))
        if current_game_ip == hunting_ip:
            print(Style.RESET_ALL, end="\r", flush=True)
        previous_ip = current_game_ip
        previous_time = time()
    # display clock and seconds passed since last entry
    print(datetime.now().strftime(datetime_format)+", "+str(floor(time()-previous_time)), end="\r", flush=True)

s.enter(0, 1, print_ip)
try:
    s.run()
except KeyboardInterrupt:
    print() # newline on exit
    pass
