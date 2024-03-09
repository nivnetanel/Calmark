# config.py

import os

GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

BASE_URL = 'https://calmark.co.il/Pages/Page.aspx/GetTimeForAppointment'
BUSINESS_ID = 2688
SERVICE_ID = 29992

HEADERS = {
    'authority': 'calmark.co.il',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'he,he-IL;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
    'content-type': 'application/json; charset=UTF-8',
    'key': 'undefined',
    'origin': 'https://calmark.co.il',
    'referer': 'https://calmark.co.il/p/VBHxF',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

MARCH_DUMMY_RESPONSE = {
    'd': 'your_march_dummy_response_here',
}

APRIL_DUMMY_RESPONSE = {
    'd': 'your_april_dummy_response_here',
}