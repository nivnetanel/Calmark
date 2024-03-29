from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime, timedelta
import calendar
import time
import smtplib
from email.mime.text import MIMEText

from config import GMAIL_USER, GMAIL_PASSWORD, BASE_URL, BUSINESS_ID, SERVICE_ID, HEADERS, REFERER
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, body):
    # Create a MIME multipart message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER

    # Create HTML version of the email body with enhanced styling
    html_body = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f7f7f7;
                    padding: 20px;
                }}
                h1, h2, ul {{
                    margin-bottom: 10px;
                }}
                ul {{
                    list-style-type: none;
                    padding-left: 0;
                }}
                li {{
                    padding: 5px 0;
                }}
                .current-month {{
                    background-color: #fff;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 20px;
                }}
                .next-month {{
                    background-color: #f2f2f2;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="current-month">
                <h1>Availability for Current Month:</h1>
                <ul>
    """

    for date_key, data in input_strings[0].items():
        weekday = data.get("weekday", "")
        times = ", ".join(data.get("times", []))
        html_body += f'<li>{date_key}: {weekday} - {times}</li>'

    html_body += """
                </ul>
            </div>
            <div class="next-month">
                <h1>Availability for Next Month:</h1>
                <ul>
    """

    for date_key, data in input_strings[1].items():
        weekday = data.get("weekday", "")
        times = ", ".join(data.get("times", []))
        html_body += f'<li>{date_key}: {weekday} - {times}</li>'

    html_body += f"""
                </ul>
            </div>
            <br>
            {REFERER}
        </body>
    </html>
    """

    # Create a MIMEText object for the HTML content
    html_part = MIMEText(html_body, 'html')

    # Attach HTML part to the email
    msg.attach(html_part)

    # Connect to SMTP server and send email
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
        response = requests.post(BASE_URL, headers=HEADERS, json=data)
        response.raise_for_status()        
        result_string = response.json().get('d', '')
        return result_string
       
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
    time.sleep(10)
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