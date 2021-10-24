# D2R-IP-logger

A simple python script to display the IP of your game in Diablo II Resurrected and log it to a CSV file including a timestamp and region (EU/NA/Asia).

Useful for hunting Diablo Clone, or data collection.

![](https://i.imgur.com/3hjxBHn.png)

## How to install
If you don't have Python installed yet, install it from https://www.python.org/downloads/

Download the [D2R_ip.py](https://github.com/nocawy/D2R-IP-logger/blob/master/D2R_ip.py?raw=true) file.

## How to use

Run `D2R_ip.py`

On Windows you can either:
- double-click `D2R_ip.py` in File Explorer 
- or open Command Prompt (press Windows Key + r, type `cmd`, press enter), navigate to the directory where you downloaded the file (i.e. type `cd C:\Users\YourUsername\Downloads\`) then type `py D2R_ip.py` or `python D2R_ip.py`.

To stop the program press CTRL+C or simply close the console window.

## Info

In the last line a clock is displayed, which will turn green after 1 minute since the last game creation (which is, as of now, the cooldown before the servers allow you to create a new game).

The logfiles appear in the same folder, with filenames `D2R_ip_*.log` where * is today's date.  
If you don't want any logfiles created then modify the code, the instructions are in comments.

## How it works

The script in essence works the same way as `netstat`, [TCPView](https://docs.microsoft.com/en-us/sysinternals/downloads/tcpview) or `Resource Monitor` (a built-in Windows tool).  
It asks your operating system what TCP connections are open by which processes using a standard Python library `psutil`. It doesn't require admin rights, doesn't inject or modify anything, doesn't break TOS.

## Other software

If you don't care about creating logs, you may try:
* [TCPView](https://docs.microsoft.com/en-us/sysinternals/downloads/tcpview) -  for more detailed overview of your system's TCP connections
* [D2R-IPTool](https://github.com/VideoGameRoulette/D2RTools) - for an in-game D2R overlay display of your IP, aimed to help in DClone hunting
