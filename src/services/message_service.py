import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

url = os.getenv("DISCORD_URL")
auth = os.getenv("DISCORD_AUTH")

def send_message(message_content: str, tag: bool = False, date: bool = True) -> bool:
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    if tag:
        message_content = "@everyone\n" + message_content
    if date: message_content += "\n### Data: " + formatted_datetime + "\n"
    payload = {"content": message_content}
    header = {"authorization": auth}

    try:
        r = requests.post(url, data=payload, headers=header)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", e)
        return False

def message_builder(scraped_data: list):
    message = ""
    for index, item in enumerate(scraped_data):
        message += f"# {item['product_name']}\n"
        message += f"Product url: {item['url']}\n"
        message += f"## Prices recorded: \n"
        message += f"{item['prices'].to_str()}\n"
        
    return message

