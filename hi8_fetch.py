import os
import sys
import shutil
import requests as req
from PIL import Image
from dateutil.parser import parse
from io import BytesIO

# hi8-fetch.py <date> <zoom level> <output>
# hi8-fetch.py <string> <int> <string>
# E.g.: hi8-fetch.py 2016-01-13T22:10:00 8 2016-01-13T221000-z8.png
# Fetch Himawari-8 full disks at a given zoom level.
# Valid zoom levels seem to be powers of 2, 1..16, and 20.
#
# To do:
# - Better errors (e.g., catch the "No Image" image).
# - Don't ignore seconds, and/or:
# - option to snap to nearest valid time.
# - Librarify.

def fetch_day(time, scale, out):
    # Tile size for this dataset:
    width = 550
    height = 550
    time = parse(time)
    base = 'http://himawari8.nict.go.jp/img/D531106/%sd/550' % (scale)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
    }

    def pathfor(t, x, y):
      return "%s/%s/%02d/%02d/%02d%02d00_%s_%s.png" \
      % (base, t.year, t.month, t.day, t.hour, t.minute, x, y)


    # Create cache directory
    if not os.path.exists("./output/"):
       os.makedirs("./output/")
    if not os.path.exists("./compile/"):
       os.makedirs("./compile/")

    # Check to see if we have ouputed an image for this day
    # If so we don't need to download anything
    if os.path.isfile("./output/"+out):
        return

    # Make our tile cache folder
    if not os.path.exists("./cache/"):
       os.makedirs("./cache/")
    if not os.path.exists("./cache/"+out+"/"):
       os.makedirs("./cache/"+out+"/")

    # Create request so it will reuse the connection
    sess = req.Session() 
    # Create new image, or read in the current compiled one
    if os.path.isfile("./compile/"+out):
        png = Image.open(open("./compile/"+out, 'rb'))
    else:
        png = Image.new('RGB', (width*scale, height*scale))

    for x in range(scale):
      for y in range(scale):

        # Check to see if we have already downloaded the cach
        if os.path.isfile("./cache/"+out+"/tile-"+str(x)+"-"+str(y)+".png"):
            continue
        # If we do not have the cache, download the file
        path = pathfor(time, x, y)
        print("fetching %s" % (path))
        tiledata = sess.get(path, headers=headers).content
        
        # Open tile, and save to our cache
        tile = Image.open(BytesIO(tiledata))
        tile.save("./cache/"+out+"/tile-"+str(x)+"-"+str(y)+".png", 'PNG')
        
        # Paste it onto our master image, and save that image
        png.paste(tile, (width*x, height*y, width*(x+1), height*(y+1)))
        png.save("./compile/"+out, 'PNG')

    # Save the final image
    png.save("./output/"+out, 'PNG')
    # Delete our tiles, and compiled image
    os.remove("./compile/"+out)
    shutil.rmtree("./cache/"+out+"/")