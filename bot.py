import requests
import json
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from colorama import Fore
import pyfiglet

console = Console()

Ab = '\033[1;92m'
aB = '\033[1;91m'
AB = '\033[1;96m'
aBbs = '\033[1;93m'
AbBs = '\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def watermark(text, status="INFO", color="white"):
    timestamp = get_time()
    status_emoji = ""
    if status == "INFO":
        status_emoji = "ℹ️"
    elif status == "SUCCESS":
        status_emoji = "✅"
    elif status == "ERROR":
        status_emoji = "❌"
    return f"[{timestamp}] [{status}] {status_emoji} [bold {color}]{text}[/]"

def login(query_id):
    url = "https://kitty-api.bfp72q.com/api/login/tg"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://kitty-web.bfp72q.com",
        "referer": "https://kitty-web.bfp72q.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    data = {
        "init_data": query_id,
        "referrer": ""
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    return response_data.get("data", {}).get("token", {}).get("token")

def get_eggs(token):
    url = "https://kitty-api.bfp72q.com/api/scene/info"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://kitty-web.bfp72q.com",
        "referer": "https://kitty-web.bfp72q.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    data = {"token": token}
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    eggs = []
    for i in range(9):
        try:
            eggs.extend(response_data.get("data", [])[i].get("eggs", []))
        except (IndexError, AttributeError):
            continue
    return [egg.get("uid") for egg in eggs]

def claim_egg_reward(token, egg_uid):
    url = "https://kitty-api.bfp72q.com/api/scene/egg/reward"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://kitty-web.bfp72q.com",
        "referer": "https://kitty-web.bfp72q.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    data = {"token": token, "egg_uid": egg_uid}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def main(query_id):
    token = login(query_id)
    console.print(watermark(f"Logging in account with ID: {query_id} 🔑", "INFO", "yellow"))
    if not token:
        console.print(watermark("Failed to retrieve token. 🚫", "ERROR", "red"))
        return
    console.print(watermark("Token retrieved! ✨", "SUCCESS", "green"))
    console.print(watermark("Getting eggs... 🥚", "INFO", "yellow"))
    eggs = get_eggs(token)
    console.print(watermark("Selling eggs... 💰", "INFO", "yellow"))
    if not eggs:
        console.print(watermark("No eggs found. 🤔", "INFO", "yellow"))
        return

    for egg_uid in eggs:
        reward_response = claim_egg_reward(token, egg_uid)
        console.print(watermark(f"Egg {egg_uid}: {reward_response} 🎉", "SUCCESS", "green"))
    time.sleep(5)

if __name__ == "__main__":
    ab = pyfiglet.figlet_format("Digital Miners")
    print(a_bSa + ab)
    print(Fore.GREEN + " ✯ KITTY SCRIPT BOT ✯ ")
    print(Fore.RED + f"TELEGRAM GROUP {Fore.GREEN}✯ @DigitalMiners777 ✯")
    print(Fore.YELLOW + " ✯ DEVELOPED BY @Anaik7777 ✯ ")
    print(f"{Fore.WHITE}✯" * 60)
    print("✯ 𝑰𝒇 𝒀𝒐𝒖 𝑯𝒂𝒗𝒆 𝒂𝒏𝒚 𝑰𝒔𝒔𝒖𝒆, 𝑷𝒍𝒆𝒂𝒔𝒆 𝑽𝒊𝒔𝒊𝒕 𝑮𝒓𝒐𝒖𝒑 𝑨𝒏𝒅 𝑫𝒊𝒔𝒔𝒄𝒖𝒔𝒔 ✯")
    print(f"{Fore.WHITE}✯" * 60)

    query_id = input("Enter your Query ID: ")

    while True:
        try:
            main(query_id)
            console.print(watermark("Waiting 1 minute before restarting... ⏳", "INFO", "yellow"))
            for remaining in range(59, -1, -1):
                console.print(f"[bold cyan]Restarting in: {remaining} seconds...[/]", end="\r")
                time.sleep(1)
            print()
        except Exception as e:
            console.print(watermark(f"An error occurred: {e} ⚠️", "ERROR", "red"))
