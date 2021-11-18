import sys
import psutil
import logging
from time import strftime, time, sleep
from datetime import datetime
from colorama import init, Fore, Style
from sched import scheduler
from math import floor

update_interval = 0.1     # refresh rate in seconds
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

constant_ips = {
    '24.105.29.76',     # always open
    '34.117.122.6',     # always open
    '127.0.0.1',        # localhost
    '137.221.105.152',  # Americas lobby
    '37.244.54.10',     # Europe lobby
    '117.52.35.45',     # Asia lobby
}
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

previous_ips = set()
previous_time = time()
hunting_ip=''

print("D2R IP logger started. To exit press CTRL+C")
if len(sys.argv) >= 2:
    print('Hunting for ip: ' + Fore.LIGHTRED_EX + sys.argv[1] + Style.RESET_ALL)
    hunting_ip = sys.argv[1]

def find_procs_by_name(name):
    for p in psutil.process_iter(['name']):
        if p.info['name'] == name:
            return p
    return 0
p = find_procs_by_name('D2R.exe')

# def find_region(p):
#     for c in p.connections('tcp'):
#         if (c.raddr):
#             ip = c.raddr.ip
#             if(ip == '37.244.28.80'):
#                 return 'Europe', '80'
#             if(ip == '37.244.28.180'):
#                 return 'Europe', '180'
#             if(ip == '137.221.106.88'):
#                 return 'Americas', '88'
#             if(ip == '137.221.106.188'):
#                 return 'Americas', '188'
#             if(ip == '117.52.35.79'):
#                 return 'Asia', '79'
#             if(ip == '117.52.35.179'):
#                 return 'Asia', '179'
#     return '?','?'

def print_ip():
    s.enter(update_interval, 1, print_ip)   # run this function every update_interval
    global p
    if p==0 or p.is_running()==False:
        p = find_procs_by_name('D2R.exe')
    if p==0:
        print("game is not running", end="\r")
        return
    global previous_ips
    global previous_time
    region = '?'
    subregion = '?'
    open_ips = set()
    for c in p.connections('tcp'):
        if (c.raddr):
            ip = c.raddr.ip
            if(ip == '37.244.28.80'):
                region,subregion = 'Europe','80'
            elif(ip == '37.244.28.180'):
                region,subregion = 'Europe','180'
            elif(ip == '137.221.106.88'):
                region,subregion = 'Americas','88'
            elif(ip == '137.221.106.188'):
                region,subregion = 'Americas','188'
            elif(ip == '117.52.35.79'):
                region,subregion = 'Asia','79'
            elif(ip == '117.52.35.179'):
                region,subregion = 'Asia','179'
            elif(ip not in constant_ips):
                open_ips.add((ip, c.status))
    if len(open_ips) == 1:
        # found a new game ip, log it
        for current_game_ip, status in (open_ips-previous_ips):
            print(' '*44, end="\r", flush=True) #clear line
            if current_game_ip == hunting_ip:
                print(Fore.LIGHTRED_EX, end="\r", flush=True)
            logging.info('{},{}, {}, {}'.format(region, subregion, current_game_ip, status))
            if current_game_ip == hunting_ip:
                print(Style.RESET_ALL, end="\r", flush=True)
            previous_ips = open_ips.copy()
            previous_time = time()
    # display clock and seconds passed since last entry
    print(datetime.now().strftime(datetime_format)+", "+str(floor(time()-previous_time)), end="\r", flush=True)

s.enter(0, 1, print_ip)
try:
    s.run()
except KeyboardInterrupt:
    print() # newline on exit
    pass
