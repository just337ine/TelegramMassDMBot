#!/bin/env python3

import os
import sys
import csv
import time
import atexit
import configparser
from random import randint
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import FloodWaitError

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

sent_member_ids = set()
SENT_MEMBERS_CSV_FILE = 'sent_members.csv'

def clear_screen():
    """
    Function for clearing screen
    """

    os.system('cls' if os.name == 'nt' else 'clear')

def generate_random_delay():
    """
    Generates a random delay between 47.5 and 70 seconds.

    Returns:
        float: A random delay in seconds.
    """

    return randint(95, 140) / 2

class Main:
    """
    Main class for sending SMS messages using Telegram.
    """

    @staticmethod
    def banner():
        """
        Prints the program banner.
        """

        print(f"""
{re}░█▄█░█▀█░█▀▀░█▀▀░░░{cy}█▀▀░█▄█░█▀▀░░░{gr}█▀▄░█▀█░▀█▀
{re}░█░█░█▀█░▀▀█░▀▀█░░░{cy}▀▀█░█░█░▀▀█░░░{gr}█▀▄░█░█░░█░
{re}░▀░▀░▀░▀░▀▀▀░▀▀▀░░░{cy}▀▀▀░▀░▀░▀▀▀░░░{gr}▀▀░░▀▀▀░░▀░
                                             
                version: 2.0
        https://t.me/just337ine
                """)

    @staticmethod
    def send_sms():
        """
        Sends SMS messages to Telegram users based on input CSV data.
        """

        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            clear_screen()
            Main.banner()
            print(re + "[!] run python3 setup.py first !!\n")
            sys.exit(1)

        def load_sent_members():
            try:
                with open(SENT_MEMBERS_CSV_FILE, 'r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        sent_member_ids.add(int(row[0]))
            except FileNotFoundError:
                pass

        def save_sent_members():
            with open(SENT_MEMBERS_CSV_FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                for member_id in sent_member_ids:
                    writer.writerow([member_id])

        atexit.register(save_sent_members)
        load_sent_members()

        client = TelegramClient(phone, api_id, api_hash)
        client.connect()

        if not client.is_user_authorized():
            client.send_code_request(phone)
            clear_screen()
            Main.banner()
            client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))

        clear_screen()
        Main.banner()
        input_file = sys.argv[1]
        users = []

        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)

        print(gr + "[1] send sms by user ID\n[2] send sms by username ")
        mode = int(input(gr + "Input : " + re))
        message = input(gr + "[+] Enter Your Message : " + re)

        def send_message_to_user(user):
            """
            Sends a message to a Telegram user.

            Args:
                user (dict): User information.

            Raises:
                FloodWaitError: If a flood error occurs.
            """

            try:
                print(gr + "[+] Sending Message to:", user['name'])

                if user['id'] not in sent_member_ids:
                    random_delay = generate_random_delay()
                    client.send_message(receiver, message.format(user['name']))
                    sent_member_ids.add(user['id'])
                    print(gr + "[+] Waiting {} seconds".format(random_delay))
                    time.sleep(random_delay)
            except FloodWaitError as e:
                print(re + f"[!] Getting Flood Error from telegram. Waiting for {e.seconds} seconds.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re + "[!] Error:", e)
                print(re + "[!] Trying to continue...")

        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'], user['access_hash'])
            else:
                print(re + "[!] Invalid Mode. Exiting.")
                client.disconnect()
                sys.exit()

            send_message_to_user(user)

        client.disconnect()
        save_sent_members()
        print("Done. Message sent to all users.")

Main.banner()

if len(sys.argv) != 2:
    print(re + "Usage: python smsbot.py <input_csv_file>")
    sys.exit(1)

input_file = sys.argv[1]

if not input_file.endswith(".csv"):
    print(re + "Error: Please provide a valid .csv file.")
    sys.exit(1)

if __name__ == "__main__":
    Main.send_sms()
