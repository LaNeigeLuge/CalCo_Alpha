#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copier ce fichier en epd2
# Garder le fichier config
# Le fichier request devient le nouveau ical_worker
# Mettre à jour le fichier config par les configurations mise sur request 
# Importer toutes les bibliothques nécéssaires au fichier request
# Changer le nom du fichier request


# Commencer par afficher le tableau et les jours de la semaine 
# Fonction prepare_table, quelques ajustement et devrait etre opé
# Gros travail à faire sur les fonctions de ical_worker




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
import ical_worker


logging.basicConfig(level=logging.DEBUG)

 
logging.info("epd7in5_V2 Demo")
epd = epd7in5_V2.EPD()

logging.info("init and Clear")
epd.init()
epd.Clear()

font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
fheadline = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', headline_size)
ftext = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', text_size)
fbold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', text_size)

def prepare_table(draw): 
    logging.info("1.Drawing on the Horizontal image...")

    #Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    #draw = ImageDraw.Draw(Himage)
    #Draw Infotel Logo
    #Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'infotel.bmp'))
    Himage.paste(bmp, (0,0))
    #epd.display(epd.getbuffer(Himage2))


    # separate top bar from rest
    draw.line([(offset_left, offset_top + bar_top - 1), (width, offset_top + bar_top - 1)], width=2)
    # separate all-day events from grid
    draw.line([(offset_left, offset_top + bar_top + offset_allday), (width, offset_top + bar_top + offset_allday)], width=2)
    # separate the left bar from the rest
    draw.line([(offset_left + bar_left -1, offset_top), (offset_left + bar_left - 1, height)], width=2)

    day0 = ical_worker.basetime
    heads = day0.strftime('%A %d %B %Y')
    draw.text((100,90), heads, font = font18, fill = 0)

    draw.line([(50,140),(350,140)], width=2) #bottom line

    #Draw name of room
    draw.text((100, 40), 'SALLE TURING', font = font24, fill = 0)

    draw.text((10, 160), '• Eteindre les lumières', font = font24, fill = 0)
    draw.text((10, 220), '• Personnes max: 5 ', font = font24, fill = 0)
    draw.text((10, 290), '• Interdiction de manger !', font = font24, fill = 0)
    draw.text((100, 400), 'Bonne journée ! ;)', font = font24, fill = 0)
    # draw the vertical day separators and day headlines
    for i in range(0, DAYS):
        x = offset_left + bar_left + per_day * i
        # for every but the first, draw separator to the left
        if i > 0: 
            draw.line([(x, offset_top), (x, height)])
        # draw date headline
        day = ical_worker.basetime + datetime.timedelta(days=i)
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
        textoffs_y = math.floor((per_hour - text_size) / 2)
        draw.text((offset_left, y + textoffs_y - 1), "%02d" % (BEGIN_DAY + i), font=fheadline)

    # clear the all-day events space
    draw.rectangle((offset_left + bar_left + 1, offset_top + bar_left + 1, width, offset_top + bar_left + offset_allday - 1), fill=200, width=0)

    #epd.display(epd.getbuffer(Himage))

def draw_short_event(d, e):
    """
    Internal function for drawing events into the grid.

    Not to be used for drawing events manually, please use draw_event for that.

    This function cannot draw events lasting across midnight. Instead, such events are split up
    into several calls of draw_short_event and draw_allday_event.

    """
    x_start = offset_left + bar_left + e["day"] * per_day + e["column"] * per_day / e["max_collision"]
    y_start = offset_top + bar_top + offset_allday + math.floor((e["start"] - (BEGIN_DAY * 60)) * per_hour / 60)
    width = per_day / e["max_collision"]
    y_end = offset_top + bar_top + offset_allday + math.floor((e["end"] - (BEGIN_DAY * 60)) * per_hour / 60)
    # clear the event's area and make the outline
    d.rectangle((x_start, y_start, x_start + width, y_end), outline=0, width=2, fill=200)

    textoffs_x = 5
    textoffs_y = (per_hour - text_size) // 2 - 1
    fulltext = e["title"]
    while d.textsize(fulltext, font=ftext)[0] > width - 2 * textoffs_x and len(fulltext) > 0:
        fulltext = fulltext[:-1]
    if e["end"] - e["start"] >= 90:
        begintext = "%02d:%02d" % (e["start"] // 60, e["start"] % 60)
        endtext = "%02d:%02d" % (e["end"] // 60, e["end"] % 60)
        datetext = "\n%s-%s" % (begintext, endtext)
        if d.textsize(datetext, font=ftext)[0] > width - 2 * textoffs_x:
           datetext = "\n%s" % begintext
        if d.textsize(datetext, font=ftext)[0] <= width - 2 * textoffs_x:
            fulltext += datetext
    d.text((x_start + textoffs_x, y_start + textoffs_y), fulltext, font=ftext)
    print(fulltext)
    #d.text((x_start + 5, y_start + text_size + textoffs_y), begintext + "-" + endtext, font=ftext)

    print(e)


if __name__ == "__main__":
    (drawables, all_days) = ical_worker.get_drawable_events()
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    #Draw Infotel Logo
    #Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    #bmp = Image.open(os.path.join(picdir, 'infotel.bmp'))
    #Himage2.paste(bmp, (0,40))
    #epd.display(epd.getbuffer(Himage2))
    draw = ImageDraw.Draw(Himage)
   # drawing_logo(Him,logo)
    prepare_table(draw)
    for l in drawables:
       for e in l:
          draw_short_event(draw, e)
    for e in all_days:
       draw_allday_event(draw, e)
    Himage.save(open("out.jpg","w+"))
    epd.init()
    epd.display(epd.getbuffer(Himage))
#    epd.display(epd.getbuffer(Himage2)) 
    epd.sleep()


#except IOError as e:
#    logging.info(e)
    
#except KeyboardInterrupt:    
#    logging.info("ctrl + c:")
#    epd7in5_V2.epdconfig.module_exit()
#    exit()

