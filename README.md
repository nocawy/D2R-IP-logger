# D2R-IP-logger

A python script to display the IP of your online game in `Diablo II: Resurrected` and log it to a CSV file including a timestamp and region (Americas/Europe/Asia).

Useful for hunting Diablo Clone or data collection.

![](https://i.imgur.com/2cjC4R6.png)

## How to install

A compiled version for Windows can be downloaded form the [Release Page](https://github.com/nocawy/D2R-IP-logger/releases). The latest version is here:
[D2R_ip.exe](https://github.com/nocawy/D2R-IP-logger/releases/latest/download/D2R_ip.exe).  

You can also run the [D2R_ip.py](https://github.com/nocawy/D2R-IP-logger/blob/master/D2R_ip.py?raw=true) script manually by following the steps below:
* Install Python (If you don't have it)
  * https://www.python.org/downloads/
  * On Windows during installation select "Add Python to PATH"
* Install required Python libraries, by opening Command Prompt or PowerShell and typing:
  * `python -m pip install --upgrade pip` (optional)
  * `pip install psutil`
    * If this fails due to `Microsoft Visual C++ 14.0 or greater is required`, install it (large download):
      * https://visualstudio.microsoft.com/visual-cpp-build-tools
      * Select the Individual components tab and select:
        * MSVC v142 - VS 2019 C++ x64/x86 build tools (latest)
        * Windows 10 SDK (any should work, I grabbed the highest version)
  * `pip install colorama`
* Download [D2R_ip.py](https://github.com/nocawy/D2R-IP-logger/blob/master/D2R_ip.py?raw=true) file.

## How to use

On Windows you can either:
* double-click `D2R_ip.py` or `D2R_ip.exe` in File Explorer
* open PowerShell (`Windows Key + r`, type `powershell`, press enter), navigate to the directory where you downloaded the file (i.e. type `cd C:\Users\YourUsername\Downloads\`) then type `python D2R_ip.py` or `py D2R_ip.py` or `D2R_ip.exe`.

To stop the program press `CTRL+C` or simply close the console window.

To hunt for a specific ip address:
* Run the script or application from PowerShell and add the IP after the command:
  * `python D2R_ip.py 34.93.241.196`
  * `D2R_ip.exe 34.93.241.196`

## Info

In the last line a clock is displayed, followed by the number of seconds that has passed since the last entry.

The logfiles appear in the same folder where the program is located, with filenames `D2R_ip_*.log` where `*` is today's date.  
If you don't want any logfiles created then modify the code, the instructions are in comments.

When `Diablo II: Resurrected` is launched and connects to battle.net it begins opening and closing connections to multiple IPs for about 20 seconds. The script might display some of them. If you create or join a game during that period, wait until no new IPs appear, the last (most recent) one will be your current game's IP.

Next to region a number is displayed, e.g. `Asia,79` or `Europe,180`, associated with what some call a *subregion* or a different *lobby*. When `Diablo II: Resurrected` is launched it connects to one of the two possible addresses for each region:
* Americas:
  * `137.221.106.88`
  * `137.221.106.188`
* Europe:
  * `37.244.28.80`
  * `37.244.28.180`
* Asia:
  * `117.52.35.79`
  * `117.52.35.179`

Whether this *subregion* has any significance is yet to be discovered. Some players report problems with joining games across lobbies (e.g. from .79 to .179). Although some game IPs can be found regardless of it (e.g. `34.93.229.25` can be found from both .79 and .179).


## How it works

The script in essence works the same way as `netstat`, [TCPView](https://docs.microsoft.com/en-us/sysinternals/downloads/tcpview) or `Resource Monitor` (a built-in Windows tool).  
It asks your operating system what TCP connections are open by which processes using a standard Python library `psutil`. It does not require admin rights, inject or modify anything, or break TOS.

## Other software

If you don't care about creating logs, you may try:
* [TCPView](https://docs.microsoft.com/en-us/sysinternals/downloads/tcpview) -  for more detailed overview of your system's TCP connections
* [D2R-IPTool](https://github.com/VideoGameRoulette/D2RTools) - for an in-game D2R overlay display of your IP, aimed to help in DClone hunting

## Thanks

Thanks to [sir-wilhelm](https://github.com/sir-wilhelm) for improvements in his [fork](https://github.com/sir-wilhelm/D2R-IP-logger).
