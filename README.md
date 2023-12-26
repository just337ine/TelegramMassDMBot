## TeleGram Scraper and SMS Bot

This project consists of three scripts: `setup.py`, `scraper.py`, and `smsbot.py`, which serve different purposes for Telegram scraping and sending SMS messages to Telegram users.

### Setup

1. Install Python 3 if you haven't already. You can download it from the official website: https://www.python.org/downloads/

2. Clone or download this repository to your local machine.

3. Navigate to the project directory.

4. Install the required dependencies by running the setup script:

   ```
   python3 setup.py --install
   ```

5. Setup your Telegram API credentials by running the configuration script:
   ```
   python3 setup.py --config
   ```
   Follow the prompts to enter your API ID, API Hash, and phone number. If you don't have API credentials yet, you can create them at https://my.telegram.org/apps.

### Scraping Active Members

1. Make sure you have completed the setup steps mentioned above.

2. Run the scraper script and select the groups you want to scrape active members from:
   ```
   python3 scraper.py
   ```
   Follow the on-screen instructions to select the groups. Active members from the selected groups will be saved in a customized file name with `.csv`.

### Sending SMS Messages

1. Make sure you have completed the setup steps mentioned above.

2. Prepare a CSV file with the list of users to whom you want to send SMS messages. The file should have the following format:

   ```
   username,user id,access hash,name,group,group id
   ```

3. Run the SMS bot script and provide the CSV file as input:
   ```
   python smsbot.py file.csv
   ```
   Follow the on-screen instructions to select the mode (by User ID or Username) and enter your message. The bot will send the message to each user in the CSV file.

### Important Notes

- Be cautious while using the SMS bot. Sending messages too frequently might result in Telegram blocking your account for a certain period (Flood Error). Always use the `SLEEP_TIME` variable to add a delay between messages to avoid such issues.

- The scraping script considers users active if they have been online in the last 30 days. You can modify the `is_active` function in `scraper.py` to adjust this threshold if needed.

- Before using the SMS bot, ensure you have permission to contact the users you are sending messages to. Spamming or sending unsolicited messages may violate Telegram's terms of service and can lead to account restrictions.

### Disclaimer

This project is intended for educational and research purposes only. The authors are not responsible for any misuse or illegal activities done with the tool.           
