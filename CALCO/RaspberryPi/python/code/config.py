from waveshare_epd import epd7in5_V2
import math
import requests
import json
from urllib.request import urlopen
import pytz # timezone
import datetime
import locale
locale.setlocale(locale.LC_TIME,'')
import time

BEGIN_DAY = 8
END_DAY = 20
DAYS = 2
TIMEZONE = 'Europe/Paris'
ALLDAY_MAX = 2

timezone = pytz.timezone(TIMEZONE)
basetime = datetime.datetime.now(timezone)
basetime.astimezone(timezone)
now = datetime.datetime.today()
start = basetime.replace(hour=BEGIN_DAY,minute=0)
print(now)

end = start + datetime.timedelta(days=DAYS)

header = {
    'prefer': 'outlook.timezone=\"Europe/Paris\"',
    'Authorization': 'Bearer '
 }


query_params = {
    'startDateTime': start,
    'endDateTime': end,
    '$select': 'subject,organizer,start,end',
    '$orderby': 'start/dateTime',
    '$top': '50',
  }



#myUrl = "https://graph.microsoft.com/v1.0/me/events?$select=subject,organizer,start,end"
myUrl = "https://graph.microsoft.com/v1.0/me/calendarview"
#URLS =  ["https://graph.microsoft.com/v1.0/me/events?$select=subject,organizer,start,end,location"]


response = requests.get(myUrl, headers=header,params=query_params)
json_obj = response.json()
data = json_obj["value"]




width = epd7in5_V2.EPD_WIDTH
height = epd7in5_V2.EPD_HEIGHT

offset_top =0 
offset_left =360
bar_top = 20
bar_left = 20
allday_size = 15
offset_allday = ALLDAY_MAX * allday_size
hours_day = END_DAY - BEGIN_DAY
per_hour = math.floor((height - bar_top - offset_top - offset_allday) / hours_day)
per_day = math.floor((width - bar_left - offset_left) / DAYS)

headline_size = 15
text_size = 12
