from pystyle import Write, System, Colors
import aiohttp
import re
import requests
import random
import time
import fake_useragent
import asyncio
import datetime
def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))
def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee
def create_proxies():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        proxies = response.text.splitlines()
        save_proxies(proxies)
    else:
        time.sleep(1)
        create_proxies()

async def mass_report(reporturl, amount, isproxies):
    if isproxies in ['y','yes','1']:
        create_proxies()
    
    # Read proxies once outside the loop
    proxies = []
    if isproxies in ['y','yes','1']:
        with open('proxies.txt', 'r') as f:
            proxies = f.read().splitlines()

    for i in range(1,int(amount)+1):
        useragent = fake_useragent.UserAgent
        match_nickname = re.search(r'nickname=([^&]+)', reporturl)
        match_user_id = re.search(r'owner_id=([^&]+)', reporturl)
        headers = {
            "User-Agent": useragent.random
        }
        try:
            async with aiohttp.ClientSession() as session:
                # If we have proxies, use them
                if proxies:
                    proxy = f"http://{random.choice(proxies)}"
                    async with session.get(reporturl, proxy=proxy, headers=headers) as response:
                        if response.status == 200:
                            Write.Print(f"{get_time_rn()}| Successfully sent report to {match_nickname.group(1)}(userid: {match_user_id.group(1)})\n", Colors.blue_to_red, interval=0.0001)
                        else:
                            Write.Print(f"{get_time_rn()}| Could not send report to {match_nickname.group(1)}(userid: {match_user_id.group(1)})\n", Colors.red, interval=0.0001)
                else:
                    async with session.get(reporturl, headers=headers) as response:
                        if response.status == 200:
                            Write.Print(f"{get_time_rn()}| Successfully sent report to {match_nickname.group(1)}(userid: {match_user_id.group(1)})\n", Colors.blue_to_red, interval=0.0001)
                        else:
                            Write.Print(f"{get_time_rn()}| Could not send report to {match_nickname.group(1)}(userid: {match_user_id.group(1)})\n", Colors.red, interval=0.0001)
        except Exception as e:
            Write.Print(f"{get_time_rn()}| Error: {str(e)}\n", Colors.red, interval=0.0001)
    Write.Input(f"{get_time_rn()}| Mass report ended. Press enter to continue", Colors.blue_to_red, interval=0.001)




async def mainUI():
    while True:
        System.Clear()
        Write.Print("""
                                                                                                                                                            
                                                                                                                                                                               
@@@@@@@  @@@  @@@  @@@  @@@@@@@   @@@@@@   @@@  @@@  @@@@@@@@@@    @@@@@@    @@@@@@    @@@@@@   @@@@@@@   @@@@@@@@  @@@@@@@    @@@@@@   @@@@@@@   @@@@@@@  @@@@@@@@  @@@@@@@   
@@@@@@@  @@@  @@@  @@@  @@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@   @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@  @@@@@@@@  @@@@@@@@  
  @@!    @@!  @@!  !@@    @@!    @@!  @@@  @@!  !@@  @@! @@! @@!  @@!  @@@  !@@       !@@       @@!  @@@  @@!       @@!  @@@  @@!  @@@  @@!  @@@    @@!    @@!       @@!  @@@  
  !@!    !@!  !@!  @!!    !@!    !@!  @!@  !@!  @!!  !@! !@! !@!  !@!  @!@  !@!       !@!       !@!  @!@  !@!       !@!  @!@  !@!  @!@  !@!  @!@    !@!    !@!       !@!  @!@  
  @!!    !!@  @!@@!@!     @!!    @!@  !@!  @!@@!@!   @!! !!@ @!@  @!@!@!@!  !!@@!!    !!@@!!    @!@!!@!   @!!!:!    @!@@!@!   @!@  !@!  @!@!!@!     @!!    @!!!:!    @!@!!@!   
  !!!    !!!  !!@!!!      !!!    !@!  !!!  !!@!!!    !@!   ! !@!  !!!@!!!!   !!@!!!    !!@!!!   !!@!@!    !!!!!:    !!@!!!    !@!  !!!  !!@!@!      !!!    !!!!!:    !!@!@!    
  !!:    !!:  !!: :!!     !!:    !!:  !!!  !!: :!!   !!:     !!:  !!:  !!!       !:!       !:!  !!: :!!   !!:       !!:       !!:  !!!  !!: :!!     !!:    !!:       !!: :!!   
  :!:    :!:  :!:  !:!    :!:    :!:  !:!  :!:  !:!  :!:     :!:  :!:  !:!      !:!       !:!   :!:  !:!  :!:       :!:       :!:  !:!  :!:  !:!    :!:    :!:       :!:  !:!  
   ::     ::   ::  :::     ::    ::::: ::   ::  :::  :::     ::   ::   :::  :::: ::   :::: ::   ::   :::   :: ::::   ::       ::::: ::  ::   :::     ::     :: ::::  ::   :::  
   :     :     :   :::     :      : :  :    :   :::   :      :     :   : :  :: : :    :: : :     :   : :  : :: ::    :         : :  :    :   : :     :     : :: ::    :   : :  
                                                                                                                                                                                                                                                                                            
                                                by wndkx; https://t.me/wndkx ; https://github.com/wndkx/TikTokMassReport \n
""", Colors.blue_to_red, interval=0.0001)
        amount = Write.Input("Amount of requests: ", Colors.blue_to_red, interval=0.0001)
        proxies = Write.Input("Use proxies?(y or n): ", Colors.blue_to_red, interval=0.0001)
        if proxies not in ["y", "n", "yes", "no", "1", "2"]:
            mainUI()
        else:
            with open('reporturl.txt', 'r') as f:
                reporturl = f.read()
            await mass_report(reporturl, amount, proxies)

if __name__ == "__main__":
    asyncio.run(mainUI())