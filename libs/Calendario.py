import os
from dotenv import load_dotenv
import caldav
from datetime import datetime
load_dotenv()

caldav_url = os.getenv('caldav_url')
username = os.getenv('username')
password = os.getenv('password')


def addObjectToCalender(title,date):
    with caldav.DAVClient(
        url=caldav_url,
        username=username,
        password=password
    ) as client:
        calendar=client.calendar(url=caldav_url)
        
        may_event = calendar.save_event(
            dtstart=date,
            dtend=date,
            summary=title,
        )