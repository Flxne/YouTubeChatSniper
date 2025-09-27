import time
import pytchat
import requests
import json
import os
import re
from termcolor import colored
from colorama import init

init(autoreset=True)

CONFIG_FILE = 'config.json'

DISCORD_WEBHOOK_URL = ''
VIDEO_ID = ''
KEYWORD = ''

def load_config():
    global DISCORD_WEBHOOK_URL, VIDEO_ID, KEYWORD
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
                DISCORD_WEBHOOK_URL = config.get("DISCORD_WEBHOOK_URL", "")
                VIDEO_ID = config.get("VIDEO_ID", "")
                KEYWORD = config.get("KEYWORD", "")
                print(colored("Configuration loaded successfully.", 'green'))
        except json.JSONDecodeError:
            print(colored("Error reading the configuration file.", 'red'))
        except Exception as e:
            print(colored(f"Unknown error while loading configuration: {e}", 'red'))
    else:
        print(colored(f"The configuration file '{CONFIG_FILE}' does not exist.", 'red'))

def save_config():
    config = {
        "DISCORD_WEBHOOK_URL": DISCORD_WEBHOOK_URL,
        "VIDEO_ID": VIDEO_ID,
        "KEYWORD": KEYWORD
    }
    try:
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)
            print(colored("Configuration saved successfully.", 'green'))
    except Exception as e:
        print(colored(f"Error while saving configuration: {e}", 'red'))

def send_to_discord(message):
    try:
        data = {'content': message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10) 
        if response.status_code == 204:
            print(colored("Message successfully sent to Discord.", 'green'))
        else:
            print(f"Error sending message to Discord: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(colored(f"Connection error with the Discord webhook: {e}", 'red'))

def monitor_chat(video_id):
    global KEYWORD
    while True:
        try:
            print(f"Starting monitoring for video ID: {video_id}")
            chat = pytchat.create(video_id=video_id)
            
            if not chat.is_alive():
                print(colored("The live stream is not active or has no live chat.", 'red'))
                time.sleep(10)
                continue

            print(f"Chat monitoring started... (looking for keyword: '{KEYWORD}')")
            last_sent_time = 0

            while chat.is_alive():
                for c in chat.get().sync_items():
                    print(f"Message received: '{c.message}' from {c.author.name}")
                    if re.search(rf'\b{re.escape(KEYWORD)}\b', c.message, re.IGNORECASE):
                        current_time = time.time()
                        if current_time - last_sent_time >= 10:
                            discord_message = f"Found message: '{c.message}' from {c.author.name}."
                            print(colored(discord_message, 'green'))
                            send_to_discord(discord_message)
                            last_sent_time = current_time
                        else:
                            print(colored("Cooldown active, message ignored.", 'red'))
            print(colored("Live chat is no longer active or the stream has ended.", 'yellow'))
            time.sleep(10)
        except pytchat.exceptions.InvalidVideoIdException:
            print(colored("Error: Invalid live video ID. Please check and try again.", 'red'))
            break
        except Exception as e:
            print(colored(f"Error while monitoring chat: {e}", 'red'))
            time.sleep(10)

def configure():
    global DISCORD_WEBHOOK_URL, VIDEO_ID, KEYWORD
    DISCORD_WEBHOOK_URL = input("Enter your Discord Webhook URL: ")
    VIDEO_ID = input("Enter the live video ID: ")
    KEYWORD = input("Enter the keyword to search in chat messages: ")
    save_config()
    print(colored(f"Configuration updated:\nWebhook URL: {DISCORD_WEBHOOK_URL}\nVideo ID: {VIDEO_ID}\nKeyword: '{KEYWORD}'", 'yellow'))

if __name__ == "__main__":
    load_config()
    if not DISCORD_WEBHOOK_URL or not VIDEO_ID or not KEYWORD:
        print(colored("Missing configuration. Running setup now.", 'yellow'))
        configure()
    monitor_chat(VIDEO_ID)
