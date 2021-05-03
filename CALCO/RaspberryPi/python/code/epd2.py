#!/usr/bin/python
# -*- coding:utf-8 -*-


import datetime
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import locale
import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import pytz
import math
from config import *
import worker
from dateutil import parser
logging.basicConfig(level=logging.DEBUG)

 
logging.info("epd7in5_V2 Demo")
epd = epd7in5_V2.EPD()

logging.info("init and Clear")
epd.init()
epd.Clear()

font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
fheadline = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', headline_size)
ftext = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', text_size)
fbold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', text_size)


def left_part(draw):
    logging.info("Drawing left part ...")

    bmp = Image.open(os.path.join(picdir, 'infotel.bmp'))
    Himage.paste(bmp, (0,0))


    # separate top bar from rest
    #draw.line([(offset_left, offset_top + bar_top - 1), (width, offset_top + bar_top - 1)], width=2)
    # separate all-day events from grid
    #draw.line([(offset_left, offset_top + bar_top + offset_allday), (width, offset_top + bar_top + offset_allday)], width=2)
    # separate the left bar from the rest
    draw.line([(offset_left + bar_left -1, offset_top), (offset_left + bar_left - 1, height)], width=2)

    day0 = worker.basetime
    heads = day0.strftime('%A %d %B %Y')
    draw.text((100,90), heads, font = font18, fill = 0)

    draw.line([(50,140),(350,140)], width=2) #bottom line

    #Draw name of room
    draw.text((100, 40), 'SALLE TURING', font = font24, fill = 0)

    draw.text((10, 160), '• Eteindre les lumières', font = font24, fill = 0)
    draw.text((10, 220), '• Personnes max: 5 ', font = font24, fill = 0)
    draw.text((10, 290), '• Interdiction de manger !', font = font24, fill = 0)
    draw.text((100, 400), 'Bonne journée ! ;)', font = font24, fill = 0)


def right_part(draw):

    logging.info("Drawing right part ...")
    length = len(data)
    start_hours_tday = []   #List of begin hours of events today
    start_hours = []        #List of begin hours of events tomorrow
    end_hours_tday = []     #List of end  hours of events today
    end_hours = []          #List of end hours of events tomorrow
    tday = worker.basetime

    #Convert str date to dateTime
    #Add the conversion in hours lists 
    for date in data:
         datetime_obj = parser.parse(date['start']["dateTime"])
         if tday.date() == datetime_obj.date():
             start_hours_tday.append( datetime_obj.strftime('%H.%M'))
         else:
             start_hours.append( datetime_obj.strftime(' %H.%M'))

         datetime_obj2 = parser.parse(date['end']["dateTime"])

         if tday.date() == datetime_obj2.date():
             end_hours_tday.append( datetime_obj2.strftime(' %H.%M'))
         else:
             end_hours.append( datetime_obj2.strftime('%H.%M'))

    #Length of events today and tomorrow
    length_today = len(start_hours_tday)
    length_tmorrow = len(start_hours)

    #draw today events
    for k in range(length_today):
        y = offset_top + bar_top + offset_allday + per_hour * k
        textoffs_y = math.floor((per_hour - text_size)/2 )

        hours = float(start_hours_tday[k])
        space = "                    "
        #Concatenation to draw
        today_events = space  + start_hours_tday[k] + "-" + end_hours_tday[k] + "\n " + data[k]["subject"] + "\n"
        #draw.text(((offset_left + bar_left*2), y + textoffs_y - 1),today_events, font=fheadline)

       #Here we have a switch case to put events in a grid
        if hours >= 14 and hours <15:
            print ("Ca marche")
            draw.text(((offset_left - 10 + bar_left*2), 260),today_events, font=font12)



    #draw today events
    for f in range(length_tmorrow):
        y = offset_top + bar_top + offset_allday + per_hour * f
        textoffs_y = math.floor((per_hour - text_size)/2 )

        #Concatenation to draw
        next_events =  start_hours[f] + "-" + end_hours[f] + "\n " + data[f]["organizer"]["emailAddress"]["name"] + "\n"

        #Drawing the events
        draw.text(((2*offset_left - 6*bar_left), y + textoffs_y - 1),next_events, font=fheadline)




     # draw the vertical day separators and day headlines
    for i in range(0, DAYS):
        x = offset_left + bar_left + per_day * i
        # for every but the first, draw separator to the left
        if i > 0:
            draw.line([(x, offset_top), (x, height)])

        # draw date headline
        day = worker.basetime + datetime.timedelta(days=i)
        headline = day.strftime('%A %d')
        textsize_x = draw.textsize(headline, fheadline)[0]
        textoffs_x = math.floor((per_day - textsize_x) / 2)
        draw.text((x + textoffs_x, offset_top), headline, font=fheadline)


     # draw horizontal hour separators and hour numbers
    for i in range(0, hours_day):
        y = offset_top + bar_top + offset_allday + per_hour * i
        # for every but the first, draw separator before
        if i > 0:
            # separator = dotted line with every fourth pixel
            for j in range(offset_left, width, 4):
                draw.point([(j, y)])
        # draw the hour number
        textoffs_y = math.floor((per_hour - text_size)/2 )
        draw.text((offset_left, y + textoffs_y - 1), "%02d" % (BEGIN_DAY + i), font=fheadline)        






#        print (data[i]) 
#        print (i["organizer"])
#        print (i["start"]["dateTime"])
#        print (i["end"]["dateTime"])


    

if __name__ == "__main__":
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    left_part(draw)
    right_part(draw)
#    Himage.save(open("out.jpg","w+"))
    epd.init()
    epd.display(epd.getbuffer(Himage))
    epd.sleep()



