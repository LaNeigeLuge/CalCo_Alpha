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
DAYS = 1
TIMEZONE = 'Europe/Paris'
ALLDAY_MAX = 2

timezone = pytz.timezone(TIMEZONE)
basetime = datetime.datetime.now(timezone)
basetime.astimezone(timezone)
now = datetime.datetime.today()
start = basetime.replace(hour=BEGIN_DAY,minute=0)
print(now)

end = start + datetime.timedelta(days=DAYS)

query_params = {
    'startDateTime': start,
    'endDateTime': end,
    '$select': 'subject,organizer,start,end',
    '$orderby': 'start/dateTime',
    '$top': '50',
#    'prefer': outlook.timezone: "Europe/Paris"
  }



#myUrl = "https://graph.microsoft.com/v1.0/me/events?$select=subject,organizer,start,end"
myUrl = "https://graph.microsoft.com/v1.0/me/calendarview"
#URLS =  ["https://graph.microsoft.com/v1.0/me/events?$select=subject,organizer,start,end,location"]


response = requests.get(myUrl, headers={ 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJub25jZSI6IkpjazBINi1wQlFTNkxnWTdCbzJLalEtSm9aVUdFRWxMcTNvb0NCbWltRE0iLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8wN2U5YjZhNC02ZTlkLTQ1N2ItOWU5OC04MzZhNjVmYmMwOWEvIiwiaWF0IjoxNjE5NzY5OTU1LCJuYmYiOjE2MTk3Njk5NTUsImV4cCI6MTYxOTc3Mzg1NSwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsidXJuOnVzZXI6cmVnaXN0ZXJzZWN1cml0eWluZm8iLCJ1cm46bWljcm9zb2Z0OnJlcTEiLCJ1cm46bWljcm9zb2Z0OnJlcTIiLCJ1cm46bWljcm9zb2Z0OnJlcTMiLCJjMSIsImMyIiwiYzMiLCJjNCIsImM1IiwiYzYiLCJjNyIsImM4IiwiYzkiLCJjMTAiLCJjMTEiLCJjMTIiLCJjMTMiLCJjMTQiLCJjMTUiLCJjMTYiLCJjMTciLCJjMTgiLCJjMTkiLCJjMjAiLCJjMjEiLCJjMjIiLCJjMjMiLCJjMjQiLCJjMjUiXSwiYWlvIjoiQVNRQTIvOFRBQUFBTUI5WHlNekxkNjZUNm11eFlGLzljOFhFOG8rVGJkL040UmdKNjdjWDZlcz0iLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIGV4cGxvcmVyIChvZmZpY2lhbCBzaXRlKSIsImFwcGlkIjoiZGU4YmM4YjUtZDlmOS00OGIxLWE4YWQtYjc0OGRhNzI1MDY0IiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJQRVJFSVJBIiwiZ2l2ZW5fbmFtZSI6IktldmluIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiOTIuMTcwLjIxNC4yMTIiLCJuYW1lIjoiUEVSRUlSQSBLZXZpbiIsIm9pZCI6IjA3ZDQxNzExLWZjZDktNGZiYS04NDE5LTUwNDQ4ZDc1NDExZCIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS04NjE1Njc1MDEtNTA3OTIxNDA1LTE5NTc5OTQ0ODgtNDMxMTQiLCJwbGF0ZiI6IjUiLCJwdWlkIjoiMTAwMzIwMDA5NDVDM0E4RCIsInJoIjoiMC5BWE1BcExicEI1MXVlMFdlbUlOcVpmdkFtclhJaTk3NTJiRklxSzIzU05weVVHUnpBTHMuIiwic2NwIjoiQ2FsZW5kYXJzLlJlYWQgQ2FsZW5kYXJzLlJlYWRXcml0ZSBvcGVuaWQgcHJvZmlsZSBTZWN1cml0eUV2ZW50cy5SZWFkLkFsbCBTZWN1cml0eUV2ZW50cy5SZWFkV3JpdGUuQWxsIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgZW1haWwiLCJzdWIiOiIwdjF6bVVCb3lpb3R5cmFpdlhaR0l2T0hvTGtaMUMtYlByUXNlazNhNGpnIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkVVIiwidGlkIjoiMDdlOWI2YTQtNmU5ZC00NTdiLTllOTgtODM2YTY1ZmJjMDlhIiwidW5pcXVlX25hbWUiOiJrZXZpbi5wZXJlaXJhQGluZm90ZWwuY29tIiwidXBuIjoia2V2aW4ucGVyZWlyYUBpbmZvdGVsLmNvbSIsInV0aSI6Imlyb3p4b0JYUEVpZmVlemVQbzRUQVEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfc3QiOnsic3ViIjoiLW16TmpPZWVZaVd1R3RGb2toXzhpT2ZVbk5ZRk5DTk00cWxCV2M5b3NiMCJ9LCJ4bXNfdGNkdCI6MTQ4NzMyNjQzMn0.GZWo8-SBhpNfbtvE4g7LmI8yTIph4BizeMPT75gaTFIYg0hgx5dD5hbiTuWilPQbMxvHSJ35TH83h3fbZMegjhj5T4bWi6GyZsMUSbyFBXuDJuflZxY11VAYDZycr2ko1TibluvUTlxnMCwqe9XFBfGNJMSmLiCmesxIbfzfQy72H7_RlBlRdn5nLv1XH-bt98SzMONF9sAB782DknO8wUKwIgdtxSNCE8Ixr363ALzbtfx_sfHW2il-vStbE6ZnHo0CJl9czaDfaOd0Xp4klTEOoN44ieCR8eD0pZVxozyELvmb8LJNyFRz3BPLGtSv_Y0FskU0CPJznnP_e9GSSw'},params=query_params)
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
