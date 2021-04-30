import requests
import json
from urllib.request import urlopen
import locale
locale.setlocale(locale.LC_TIME,'')
import time
import requests
import pytz # timezone
import datetime

TIMEZONE= "Europe/Paris"

BEGIN_DAY = 8
END_DAY = 20
DAYS = 1
DAY = 1
TIMEZONE = 'Europe/Paris'
ALLDAY_MAX = 2

timezone = pytz.timezone(TIMEZONE)
#basetime = datetime.datetime.strptime("Apr 23 2019 01:15AM", '%b %d %Y %I:%M%p').replace(tzinfo=timezone)
basetime = datetime.datetime.now(timezone)
basetime.astimezone(timezone)
now = datetime.datetime.today()
start = basetime.replace(hour=BEGIN_DAY,minute=0)
#print(now)

end = start + datetime.timedelta(days=DAYS)
end1 = start + datetime.timedelta(days=DAY)
query_params = {
    'startDateTime': start,
    'endDateTime': end,
    '$select': 'subject,organizer,start,end',
    '$orderby': 'start/dateTime',
    '$top': '50'
  }

count_events = {
    'startDateTime': start,
    'endDateTime': end1,
    '$select': 'subject,organizer,start,end',
    '$orderby': 'start/dateTime',
    '$top': '50'
 }

myUrl = "https://graph.microsoft.com/v1.0/me/calendarview"
#token = 'Bearer eyJ0eXAiOiJKV1QiLCJub25jZSI6ImEtMVlJWmZ3aDhmc1F0dUx2dWp0MVRVcFZHN1pZbXRZUy11TXZfNnhJSGMiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8wN2U5YjZhNC02ZTlkLTQ1N2ItOWU5OC04MzZhNjVmYmMwOWEvIiwiaWF0IjoxNjE5NTEyMTk1LCJuYmYiOjE2MTk1MTIxOTUsImV4cCI6MTYxOTUxNjA5NSwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsidXJuOnVzZXI6cmVnaXN0ZXJzZWN1cml0eWluZm8iLCJ1cm46bWljcm9zb2Z0OnJlcTEiLCJ1cm46bWljcm9zb2Z0OnJlcTIiLCJ1cm46bWljcm9zb2Z0OnJlcTMiLCJjMSIsImMyIiwiYzMiLCJjNCIsImM1IiwiYzYiLCJjNyIsImM4IiwiYzkiLCJjMTAiLCJjMTEiLCJjMTIiLCJjMTMiLCJjMTQiLCJjMTUiLCJjMTYiLCJjMTciLCJjMTgiLCJjMTkiLCJjMjAiLCJjMjEiLCJjMjIiLCJjMjMiLCJjMjQiLCJjMjUiXSwiYWlvIjoiRTJaZ1lORE9PSjRreFY1MlBvejc2SnV0cjNhZWp5MWptcXE1NkE1alFNK1Y5M1hGck5ZQSIsImFtciI6WyJwd2QiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggZXhwbG9yZXIgKG9mZmljaWFsIHNpdGUpIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IlBFUkVJUkEiLCJnaXZlbl9uYW1lIjoiS2V2aW4iLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiI5Mi4xNzAuMjE0LjIxMiIsIm5hbWUiOiJQRVJFSVJBIEtldmluIiwib2lkIjoiMDdkNDE3MTEtZmNkOS00ZmJhLTg0MTktNTA0NDhkNzU0MTFkIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTg2MTU2NzUwMS01MDc5MjE0MDUtMTk1Nzk5NDQ4OC00MzExNCIsInBsYXRmIjoiNSIsInB1aWQiOiIxMDAzMjAwMDk0NUMzQThEIiwicmgiOiIwLkFYTUFwTGJwQjUxdWUwV2VtSU5xWmZ2QW1yWElpOTc1MmJGSXFLMjNTTnB5VUdSekFMcy4iLCJzY3AiOiJDYWxlbmRhcnMuUmVhZCBDYWxlbmRhcnMuUmVhZFdyaXRlIG9wZW5pZCBwcm9maWxlIFNlY3VyaXR5RXZlbnRzLlJlYWQuQWxsIFNlY3VyaXR5RXZlbnRzLlJlYWRXcml0ZS5BbGwgVXNlci5SZWFkIFVzZXIuUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWRXcml0ZSBlbWFpbCIsInN1YiI6IjB2MXptVUJveWlvdHlyYWl2WFpHSXZPSG9Ma1oxQy1iUHJRc2VrM2E0amciLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiRVUiLCJ0aWQiOiIwN2U5YjZhNC02ZTlkLTQ1N2ItOWU5OC04MzZhNjVmYmMwOWEiLCJ1bmlxdWVfbmFtZSI6ImtldmluLnBlcmVpcmFAaW5mb3RlbC5jb20iLCJ1cG4iOiJrZXZpbi5wZXJlaXJhQGluZm90ZWwuY29tIiwidXRpIjoiOENMc25hN0d1RXFQa2FjSl9ldVlBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19zdCI6eyJzdWIiOiItbXpOak9lZVlpV3VHdEZva2hfOGlPZlVuTllGTkNOTTRxbEJXYzlvc2IwIn0sInhtc190Y2R0IjoxNDg3MzI2NDMyfQ.WkMYNKj_cxAIm5pgaHeFp9zNLWw7He0u4s3NGh3P_lKrB_UJ2_Qvrcf-wtDJ1tRCdoQe2j3tWXeAa0Ly3q7tH00e5yWEY7ZhMgLnQYCTBl6PcoEXpyQo4SoT9sfG9zzoOdvp8EILs2T0rnDZWFOvsiTIQwlXWSHjtZVPOo5kZQDZePXuLGtnphDxC3gUjcmCsopyRnXX_Wi1lrlEkZJ72CCX6KUfXvV1rCuwSFEkhi3msFqXHYG2z7SsQrYvkHnITMGmF06Zv7h_-DVUVc_iZSqUrO0laD1fwXXceKC-HbLBRfmdf-Vg7D9xWNUlecqJEkpBzhmKpWnIwj3__djb3A'
#response = requests.get(myUrl, headers={ 'Authorization': token},params=query_params)
#json_obj = response.json()
#data = json_obj["value"]
#print(data)




def get_calendar_events():

    response = requests.get(myUrl, headers={ 'Authorization': token},params=query_params)
    json_obj = response.json()
    data = json_obj["value"]
    return data

def get_events_a_day():

    response = requests.get(myUrl, headers={ 'Authorization': token},params=count_events)
    json_obj = response.json()
    data = json_obj["value"]
    length = len(data)
    return length


#for i in get_calendar_events():
#   print (i["organizer"])
#   print (i["subject"])
#    print (i["start"]["dateTime"])
#    print (i["end"]["dateTime"])


#length = get_events_a_day()
#print(length)
