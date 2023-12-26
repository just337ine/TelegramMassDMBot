#!/usr/bin/env python3
# Code by: Ugwu Justine

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os
import sys
import configparser
import csv
import time

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    clear_screen()
    print(f"""
{re}░▀█▀░█▀▀░█░░{cy}░█▀▀░█▀▀░█▀▄░█▀█░{gr}█▄█░░░█▀▀{re}░█▀▀░█▀▄░█▀█░█▀█{cy}░█▀▀░█▀▄
{re}░░█░░█▀▀░█░░{cy}░█▀▀░█░█░█▀▄░█▀█░{gr}█░█░░░▀▀█{re}░█░░░█▀▄░█▀█░█▀▀{cy}░█▀▀░█▀▄
{re}░░▀░░▀▀▀░▀▀▀{cy}░▀▀▀░▀▀▀░▀░▀░▀░▀░{gr}▀░▀░░░▀▀▀{re}░▀▀▀░▀░▀░▀░▀░▀░░{cy}░▀▀▀░▀░▀

                         Version: 1.5
                     https://t.me/just337ine
        """)


cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    clear_screen()
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    clear_screen()
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))

clear_screen()
banner()
chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup is True:  # edit ==  to is
            groups.append(chat)
    except Exception:
        continue

print(gr+'[+] Choose a group to scrape members :'+re)
i = 0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - ' + g.title)
    i += 1

print('')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group = groups[int(g_index)]

print(gr+'[+] Fetching Members...')
time.sleep(1)
all_participants = []
all_participants = client.get_participants(
        target_group,
        filter=None,
        aggressive=True
        )

# Prompt the user for the desired filename
custom_filename = input(
    gr+"[+] Enter the custom filename (without extension): "+re)

# Modify the file saving part to use the custom filename
output_filename = f"{custom_filename}.csv"
with open(output_filename, "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash',
                    'name', 'group', 'group id'])
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([username, user.id, user.access_hash,
                        name, target_group.title, target_group.id])

print(gr+'[+] Members scraped successfully. Saved in file: ' + output_filename)
