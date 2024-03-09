import requests
from datetime import datetime, timedelta
import calendar
import json
import time
import smtplib
from email.mime.text import MIMEText

from config import GMAIL_USER, GMAIL_PASSWORD, BASE_URL, BUSINESS_ID, SERVICE_ID, HEADERS, MARCH_DUMMY_RESPONSE, APRIL_DUMMY_RESPONSE
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


MARCH_DUMMY_RESPONSE = {
    "d": "[[\"2024-03-27T11:40:00\",\"2024-03-27T13:40:00\",\"2024-03-31T11:00:00\",\"2024-03-31T12:20:00\",\"2024-03-31T12:40:00\",\"2024-03-31T13:00:00\",\"2024-03-31T13:20:00\",\"2024-03-31T13:40:00\"],null]"
}

APRIL_DUMMY_RESPONSE = {
    "d": "[[\"2024-04-02T12:00:00\",\"2024-04-02T12:20:00\",\"2024-04-02T12:40:00\",\"2024-04-02T13:00:00\",\"2024-04-02T13:20:00\",\"2024-04-02T13:40:00\",\"2024-04-02T14:00:00\",\"2024-04-02T14:20:00\",\"2024-04-02T16:00:00\",\"2024-04-02T16:20:00\",\"2024-04-02T16:40:00\",\"2024-04-03T11:00:00\",\"2024-04-03T11:20:00\",\"2024-04-03T11:40:00\",\"2024-04-03T12:00:00\",\"2024-04-03T12:20:00\",\"2024-04-03T12:40:00\",\"2024-04-03T13:00:00\",\"2024-04-03T13:20:00\",\"2024-04-03T13:40:00\",\"2024-04-03T14:00:00\",\"2024-04-03T14:20:00\",\"2024-04-03T14:40:00\",\"2024-04-03T16:00:00\",\"2024-04-03T16:20:00\",\"2024-04-03T16:40:00\",\"2024-04-03T17:20:00\",\"2024-04-03T17:40:00\",\"2024-04-03T19:20:00\",\"2024-04-04T10:00:00\",\"2024-04-04T10:20:00\",\"2024-04-04T10:40:00\",\"2024-04-04T12:00:00\",\"2024-04-04T12:20:00\",\"2024-04-04T13:20:00\",\"2024-04-04T13:40:00\",\"2024-04-04T16:00:00\",\"2024-04-04T16:20:00\",\"2024-04-04T16:40:00\",\"2024-04-04T18:00:00\",\"2024-04-04T18:20:00\",\"2024-04-04T20:00:00\",\"2024-04-04T20:20:00\",\"2024-04-05T10:40:00\",\"2024-04-05T11:00:00\",\"2024-04-05T11:40:00\",\"2024-04-05T12:00:00\",\"2024-04-05T12:20:00\",\"2024-04-05T12:40:00\",\"2024-04-05T13:00:00\",\"2024-04-05T14:40:00\",\"2024-04-05T15:00:00\",\"2024-04-07T11:20:00\",\"2024-04-07T11:40:00\",\"2024-04-07T12:00:00\",\"2024-04-07T12:20:00\",\"2024-04-07T12:40:00\",\"2024-04-07T13:20:00\",\"2024-04-07T13:40:00\",\"2024-04-07T14:20:00\",\"2024-04-07T16:00:00\",\"2024-04-07T17:20:00\",\"2024-04-07T18:00:00\",\"2024-04-07T18:20:00\",\"2024-04-07T19:00:00\",\"2024-04-07T19:20:00\",\"2024-04-07T19:40:00\",\"2024-04-07T20:00:00\",\"2024-04-09T11:00:00\",\"2024-04-09T11:20:00\",\"2024-04-09T11:40:00\",\"2024-04-09T12:20:00\",\"2024-04-09T12:40:00\",\"2024-04-09T13:00:00\",\"2024-04-09T13:20:00\",\"2024-04-09T13:40:00\",\"2024-04-09T14:00:00\",\"2024-04-09T14:20:00\",\"2024-04-09T14:40:00\",\"2024-04-09T17:00:00\",\"2024-04-09T17:20:00\",\"2024-04-09T17:40:00\",\"2024-04-09T18:00:00\",\"2024-04-09T18:20:00\",\"2024-04-09T18:40:00\",\"2024-04-09T19:00:00\",\"2024-04-09T19:40:00\",\"2024-04-10T11:00:00\",\"2024-04-10T11:20:00\",\"2024-04-10T11:40:00\",\"2024-04-10T12:00:00\",\"2024-04-10T12:20:00\",\"2024-04-10T12:40:00\",\"2024-04-10T13:00:00\",\"2024-04-10T13:20:00\",\"2024-04-10T14:00:00\",\"2024-04-10T14:20:00\",\"2024-04-10T14:40:00\",\"2024-04-10T16:20:00\",\"2024-04-10T19:00:00\",\"2024-04-10T19:20:00\",\"2024-04-10T19:40:00\",\"2024-04-11T10:00:00\",\"2024-04-11T10:20:00\",\"2024-04-11T10:40:00\",\"2024-04-11T11:00:00\",\"2024-04-11T11:20:00\",\"2024-04-11T11:40:00\",\"2024-04-11T12:00:00\",\"2024-04-11T12:20:00\",\"2024-04-11T12:40:00\",\"2024-04-11T13:00:00\",\"2024-04-11T13:20:00\",\"2024-04-11T13:40:00\",\"2024-04-11T14:00:00\",\"2024-04-11T14:20:00\",\"2024-04-11T16:00:00\",\"2024-04-11T16:40:00\",\"2024-04-11T19:20:00\",\"2024-04-12T10:20:00\",\"2024-04-12T11:20:00\",\"2024-04-12T11:40:00\",\"2024-04-12T12:00:00\",\"2024-04-12T12:20:00\",\"2024-04-12T12:40:00\",\"2024-04-12T13:20:00\",\"2024-04-14T11:00:00\",\"2024-04-14T11:20:00\",\"2024-04-14T12:00:00\",\"2024-04-14T12:20:00\",\"2024-04-14T12:40:00\",\"2024-04-14T13:00:00\",\"2024-04-14T13:20:00\",\"2024-04-14T13:40:00\",\"2024-04-14T14:00:00\",\"2024-04-14T14:20:00\",\"2024-04-14T16:00:00\",\"2024-04-14T16:20:00\",\"2024-04-14T16:40:00\",\"2024-04-14T17:00:00\",\"2024-04-14T17:20:00\",\"2024-04-14T17:40:00\",\"2024-04-14T18:00:00\",\"2024-04-14T18:20:00\",\"2024-04-14T18:40:00\",\"2024-04-14T19:20:00\",\"2024-04-14T19:40:00\",\"2024-04-16T11:00:00\",\"2024-04-16T11:20:00\",\"2024-04-16T11:40:00\",\"2024-04-16T12:00:00\",\"2024-04-16T12:20:00\",\"2024-04-16T12:40:00\",\"2024-04-16T13:00:00\",\"2024-04-16T13:20:00\",\"2024-04-16T13:40:00\",\"2024-04-16T14:00:00\",\"2024-04-16T14:20:00\",\"2024-04-16T14:40:00\",\"2024-04-16T16:00:00\",\"2024-04-16T16:20:00\",\"2024-04-16T16:40:00\",\"2024-04-16T17:00:00\",\"2024-04-16T17:40:00\",\"2024-04-16T18:00:00\",\"2024-04-16T18:20:00\",\"2024-04-16T18:40:00\",\"2024-04-16T19:40:00\",\"2024-04-17T11:00:00\",\"2024-04-17T11:20:00\",\"2024-04-17T11:40:00\",\"2024-04-17T12:00:00\",\"2024-04-17T12:20:00\",\"2024-04-17T13:00:00\",\"2024-04-17T13:20:00\",\"2024-04-17T13:40:00\",\"2024-04-17T14:00:00\",\"2024-04-17T14:20:00\",\"2024-04-17T14:40:00\",\"2024-04-17T16:00:00\",\"2024-04-17T16:20:00\",\"2024-04-17T16:40:00\",\"2024-04-17T17:00:00\",\"2024-04-17T17:20:00\",\"2024-04-17T17:40:00\",\"2024-04-17T18:40:00\",\"2024-04-17T19:20:00\",\"2024-04-17T19:40:00\",\"2024-04-18T10:20:00\",\"2024-04-18T10:40:00\",\"2024-04-18T11:20:00\",\"2024-04-18T12:00:00\",\"2024-04-18T12:20:00\",\"2024-04-18T12:40:00\",\"2024-04-18T13:00:00\",\"2024-04-18T13:20:00\",\"2024-04-18T13:40:00\",\"2024-04-18T14:00:00\",\"2024-04-18T14:20:00\",\"2024-04-18T16:00:00\",\"2024-04-18T16:20:00\",\"2024-04-18T16:40:00\",\"2024-04-18T17:00:00\",\"2024-04-18T17:20:00\",\"2024-04-18T18:00:00\",\"2024-04-18T18:20:00\",\"2024-04-18T19:20:00\",\"2024-04-18T19:40:00\",\"2024-04-18T20:00:00\",\"2024-04-18T20:20:00\",\"2024-04-19T10:00:00\",\"2024-04-19T10:20:00\",\"2024-04-19T11:00:00\",\"2024-04-19T11:20:00\",\"2024-04-19T11:40:00\",\"2024-04-19T12:00:00\",\"2024-04-19T12:20:00\",\"2024-04-19T14:40:00\",\"2024-04-19T15:00:00\",\"2024-04-19T15:20:00\",\"2024-04-21T11:20:00\",\"2024-04-21T11:40:00\",\"2024-04-21T12:00:00\",\"2024-04-21T12:20:00\",\"2024-04-21T12:40:00\",\"2024-04-21T13:00:00\",\"2024-04-21T13:20:00\",\"2024-04-21T13:40:00\",\"2024-04-21T14:00:00\",\"2024-04-21T14:40:00\",\"2024-04-21T16:00:00\",\"2024-04-21T16:20:00\",\"2024-04-21T16:40:00\",\"2024-04-21T17:00:00\",\"2024-04-21T17:20:00\",\"2024-04-21T18:40:00\",\"2024-04-21T19:00:00\",\"2024-04-21T19:20:00\",\"2024-04-21T19:40:00\",\"2024-04-21T20:00:00\",\"2024-04-23T11:00:00\",\"2024-04-23T11:20:00\",\"2024-04-23T11:40:00\",\"2024-04-23T12:00:00\",\"2024-04-23T12:20:00\",\"2024-04-23T12:40:00\",\"2024-04-23T13:00:00\",\"2024-04-23T13:20:00\",\"2024-04-23T13:40:00\",\"2024-04-23T14:00:00\",\"2024-04-23T14:20:00\",\"2024-04-23T14:40:00\",\"2024-04-23T16:00:00\",\"2024-04-23T16:40:00\",\"2024-04-23T17:00:00\",\"2024-04-23T17:20:00\",\"2024-04-23T17:40:00\",\"2024-04-23T18:00:00\"],null]"
}


def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER 

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())


def transform_date_string(input_string):
    date_dict = {}

    if input_string:
        # Convert the input string to a list of dates
        date_list = eval(input_string.replace("null", "None"))

        if date_list and date_list[0]:
            for date_str in date_list[0]:
                if date_str:
                    # Parse the date string
                    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

                    # Extract date, weekday, and time components
                    date_key = date_obj.strftime("%Y-%m-%d")
                    weekday = date_obj.strftime("%A")
                    time_value = date_obj.strftime("%H:%M")

                    # Update the dictionary
                    date_dict.setdefault(date_key, {"weekday": weekday, "times": []})["times"].append(time_value)

    return date_dict

def make_http_request(date):
    current_date = date.strftime("%d/%m/%Y") + " 00:00"
    print(current_date)

    data = {
        "businessId": BUSINESS_ID,
        "services": [SERVICE_ID],
        "date": current_date,
        "waitingList": False
    }

    try:
        # response = requests.post(BASE_URL, headers=HEADERS, json=data)
        # response.raise_for_status()        
        # result_string = response.json().get('d', '')
        # return result_string
        if (date.month == 3):
          dummy_result_string = MARCH_DUMMY_RESPONSE.get('d', '')
        else:
          dummy_result_string = APRIL_DUMMY_RESPONSE.get('d', '')

        return dummy_result_string
       
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        return None

# Get the current date
current_date = datetime.now()

# Get the first day of the next month
next_month = current_date.replace(day=1) + timedelta(days=calendar.monthrange(current_date.year, current_date.month)[1])
next_month_string = next_month.strftime("%B %Y")



# Example usage for both the current month and the next month
input_strings = []
for date in [current_date, next_month]:
    input_string = make_http_request(date)
    # time.sleep(6)
    if input_string:
        result_dict = transform_date_string(input_string)
        input_strings.append(result_dict)

# Prepare the email body
email_body = "Availability for Current Month:\n\n"
for date_key, data in input_strings[0].items():
    weekday = data.get("weekday", "")
    times = ", ".join(data.get("times", []))
    email_body += f'{date_key}: {weekday} - {times}\n\n'

email_body += "\n\nAvailability for Next Month:\n\n"
for date_key, data in input_strings[1].items():
    weekday = data.get("weekday", "")
    times = ", ".join(data.get("times", []))
    email_body += f'{date_key}: {weekday} - {times}\n\n'

# Send the email
send_email(f"Availability for {current_date.strftime('%B')} and {next_month_string}", email_body)