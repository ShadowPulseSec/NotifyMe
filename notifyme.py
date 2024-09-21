"""
NotifyMe Script

This script allows you to run any command and receive a notification on your Telegram bot when the command completes.
It is particularly useful for long-running tasks where you want to be notified upon completion.

Setup Instructions:
1. Create a Telegram bot:
   a. Open Telegram and search for the BotFather (@BotFather).
   b. Start a chat with the BotFather and send the command /newbot.
   c. Follow the instructions to set a name and username for your bot.
   d. After completing the setup, you will receive a bot token. Keep this token safe.

2. Get your chat ID:
   a. Start a chat with your bot and send any message.
   b. Go to https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates in your browser.
   c. Look for the "chat" object in the response to find your chat ID.

3. Replace the BOT_TOKEN and CHAT_ID placeholders in the script with your actual bot token and chat ID.

Usage:
    python3 notifyme.py "command_to_run"

Examples:
    python3 notifyme.py "sqlmap -u http://example.com/vulnerable --batch"
    python3 notifyme.py "ping -c 4 google.com"
    python3 notifyme.py "nmap -sV -p 1-65535 example.com"
    python3 notifyme.py "curl -I http://example.com"

Replace 'command_to_run' with the actual command you want to execute, enclosed in quotes.

Example Notification:
    Command 'ping -c 4 google.com' completed successfully.
    Duration: 4.02 seconds.
"""

import subprocess
import requests
import argparse
import time

# Replace with your bot token and chat ID
BOT_TOKEN = 'BOT_TOKEN'
CHAT_ID = 'CHAT_ID'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")

def run_command(command):
    start_time = time.time()
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            print(line.strip())
        
        stdout, stderr = process.communicate()
        end_time = time.time()
        duration = end_time - start_time
        
        if process.returncode == 0:
            message = (f"Command '{command}' completed successfully.\n"
                       f"Duration: {duration:.2f} seconds.")
            send_telegram_message(message)
        else:
            message = (f"Command '{command}' failed with error: {stderr}\n"
                       f"Duration: {duration:.2f} seconds.")
            send_telegram_message(message)
            print(f"Error: {stderr}")
    
    except FileNotFoundError:
        message = f"Command '{command}' not found."
        print(message)
        send_telegram_message(message)
    except Exception as e:
        message = f"An unexpected error occurred: {e}"
        print(message)
        send_telegram_message(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run any command and send Telegram notifications.",
        epilog="Example usage:\n"
               "  python3 notifyme.py \"sqlmap -u http://example.com/vulnerable --batch\"\n"
               "  python3 notifyme.py \"ping -c 4 google.com\"\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('command', help="Full command to run, enclosed in quotes.")
    
    args = parser.parse_args()
    
    run_command(args.command)
