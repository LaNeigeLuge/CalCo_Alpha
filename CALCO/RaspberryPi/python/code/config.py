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
#print(now)

end = start + datetime.timedelta(days=DAYS)

header = {
    'prefer': 'outlook.timezone=\"Europe/Paris\"',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJub25jZSI6ImtNWXFIN1FxeFo3OWVKWFlxMFN1ZER4TTJHM1B6Qmh3LW5PenB0SVZsQnMiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8wN2U5YjZhNC02ZTlkLTQ1N2ItOWU5OC04MzZhNjVmYmMwOWEvIiwiaWF0IjoxNjIwMTIyNDY4LCJuYmYiOjE2MjAxMjI0NjgsImV4cCI6MTYyMDEyNjM2OCwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsidXJuOnVzZXI6cmVnaXN0ZXJzZWN1cml0eWluZm8iLCJ1cm46bWljcm9zb2Z0OnJlcTEiLCJ1cm46bWljcm9zb2Z0OnJlcTIiLCJ1cm46bWljcm9zb2Z0OnJlcTMiLCJjMSIsImMyIiwiYzMiLCJjNCIsImM1IiwiYzYiLCJjNyIsImM4IiwiYzkiLCJjMTAiLCJjMTEiLCJjMTIiLCJjMTMiLCJjMTQiLCJjMTUiLCJjMTYiLCJjMTciLCJjMTgiLCJjMTkiLCJjMjAiLCJjMjEiLCJjMjIiLCJjMjMiLCJjMjQiLCJjMjUiXSwiYWlvIjoiRTJaZ1lIRHkxZmlkc3Y0RVExTEQyczdrZXdYMUdSTzlmMjl0S3VpdG5MVlV2ZWJlcTJnQSIsImFtciI6WyJwd2QiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggZXhwbG9yZXIgKG9mZmljaWFsIHNpdGUpIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IlBFUkVJUkEiLCJnaXZlbl9uYW1lIjoiS2V2aW4iLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiI5Mi4xNzAuMjE0LjIxMiIsIm5hbWUiOiJQRVJFSVJBIEtldmluIiwib2lkIjoiMDdkNDE3MTEtZmNkOS00ZmJhLTg0MTktNTA0NDhkNzU0MTFkIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTg2MTU2NzUwMS01MDc5MjE0MDUtMTk1Nzk5NDQ4OC00MzExNCIsInBsYXRmIjoiNSIsInB1aWQiOiIxMDAzMjAwMDk0NUMzQThEIiwicmgiOiIwLkFYTUFwTGJwQjUxdWUwV2VtSU5xWmZ2QW1yWElpOTc1MmJGSXFLMjNTTnB5VUdSekFMcy4iLCJzY3AiOiJDYWxlbmRhcnMuUmVhZCBDYWxlbmRhcnMuUmVhZFdyaXRlIG9wZW5pZCBwcm9maWxlIFNlY3VyaXR5RXZlbnRzLlJlYWQuQWxsIFNlY3VyaXR5RXZlbnRzLlJlYWRXcml0ZS5BbGwgVXNlci5SZWFkIFVzZXIuUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWRXcml0ZSBlbWFpbCIsInN1YiI6IjB2MXptVUJveWlvdHlyYWl2WFpHSXZPSG9Ma1oxQy1iUHJRc2VrM2E0amciLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiRVUiLCJ0aWQiOiIwN2U5YjZhNC02ZTlkLTQ1N2ItOWU5OC04MzZhNjVmYmMwOWEiLCJ1bmlxdWVfbmFtZSI6ImtldmluLnBlcmVpcmFAaW5mb3RlbC5jb20iLCJ1cG4iOiJrZXZpbi5wZXJlaXJhQGluZm90ZWwuY29tIiwidXRpIjoiaU1pTllDR0NGa1c2UXZiVTJXQmhBUSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19zdCI6eyJzdWIiOiItbXpOak9lZVlpV3VHdEZva2hfOGlPZlVuTllGTkNOTTRxbEJXYzlvc2IwIn0sInhtc190Y2R0IjoxNDg3MzI2NDMyfQ.HuZJJ34fIZDQCAup80-wOJ86Adk_DtejFVBL9Yeen8dDEkHub0hrpv6IN65XH2ukyT4fYCFuHmmIY2MH1pSo1nZQ1iZeeYBkZlzVu2RNrNMojg7eYCdsqdkJtrJxYlf90DfvHOcCpNJRqc7dF-M4KwnTW5Ap8KNwKTqN46r-OYLYwNJvDd7UY-E952q0b6NiPXO-kI-oR-cE-x4GXBHrGYsjbyA_5zeJTdswywV__J-OF75_33MkeRyKR5VNNmdWvkkievzXdwHcHyk3z8D9BB-C0_hupq_J0UBsjOSHFDD1UmaWq_fKh9l-HBnIWWTTodHtxnCEQAMzVS1NeK_CHQ'
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
