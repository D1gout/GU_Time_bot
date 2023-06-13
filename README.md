![Header](https://github.com/D1gout/TGBot/blob/main/icon.PNG)

# Telegram Bot

This bot sends the schedule in a telegram

## Requirements

Python (3.10 or later)

### Python packages

[requirements.txt](https://github.com/D1gout/TGBot/blob/main/requirements.txt)

## Start

1. Clone repository
   <br>`$ git clone https://github.com/D1gout/TGBot.git`
2. Install packages
   <br>`$ pip install -r requirements.txt`
   <br><strong>or</strong>
   <br>`$ pip3 install -r requirements.txt`
3. Open utils\settings.ini and insert 
   <br>`token = YOUR_TOKEN_HERE`
4. Run project
   <br>`$ python Bot.py`
   <br><strong>or</strong>
   <br>`$ python3 Bot.py`

## Holidays
#### Turn on
1. Open utils\settings.ini and change
   <br>`stop = 1`
#### Turn off
1. Open utils\settings.ini and change
   <br>`sleep_mode = False`
   <br>`stop = 0`

## Testing

[![Python application](https://github.com/D1gout/TGBot/actions/workflows/python-app.yml/badge.svg)](https://github.com/D1gout/TGBot/actions/workflows/python-app.yml)
