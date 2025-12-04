# Imports and libraries
import asf_search as asf
from pathlib import Path
from lib.Normalize import normalize_leefilter
from lib.Padding import pad
from lib.Cropping import crop
from datetime import date, datetime, timedelta
import subprocess
import configparser
import re
import sys
import os


#Initiation:
config = configparser.ConfigParser()
script_dir = os.path.dirname(os.path.abspath(__file__))
config.read(os.path.join(script_dir, 'config_tshoRolpa.ini'))

start_date=config.get('Other','last_product_date')
usr = config.get('Login','user')
pas = config.get('Login','password')
wkt = config.get('Other','wkt')   

loc = Path(script_dir)/"Response"/"tshoRolpa"/"Backup"
geojsonPath = Path(script_dir)/"Response"/"tshoRolpa"/ "tshoRolpaAOI.geojson"
end_date = date.today()

print("start_date:", start_date, "end_date:", end_date)

if (start_date==str(end_date)):
    #print("Scanned just today!!")
    sys.exit(2)

#Searching:
results = asf.geo_search(intersectsWith=wkt,
                        platform=[asf.PLATFORM.SENTINEL1],
                        processingLevel=[asf.PRODUCT_TYPE.RTC,asf.PRODUCT_TYPE.RTC_STATIC],
                        start=start_date,
                        end=end_date)

print("No of results:", len(results))

#Crash if no results found
if not results:
    #print("No scenes found. Exiting.")
    sys.exit(3)


#Display found products:
first_result = results[0]
#print(first_result)


#Choosing _VV.tif files to download:
date = re.sub("T.*", "", first_result.properties['startTime'])
url = first_result.properties['additionalUrls'][2]
tifPath = loc / date / f"{date}.tif"
tifDir = loc / date



#Creating directiory to store backup:
tifDir.mkdir(exist_ok=True)


#Download:
subprocess.run([
    "wget",
    "-O", str(tifPath),
    "-c",
    url
], check=True)


#Preprocessing:
tifPathCropped = crop(tifPath, geojsonPath, tifDir)
tifPathPadded = pad(tifPathCropped, tifDir)
tifPathNormalized = normalize_leefilter(tifPathPadded, tifDir)


#Final Copy:    
finalPath = Path(script_dir).parent / "public" / "data" / "TshoRolpa"
finalPath.mkdir(exist_ok=True)
finalTIFF = finalPath / f"{date}.tiff"
finalPNG = finalPath / f"{date}.png"
subprocess.run(["cp", tifPathNormalized, finalTIFF])
subprocess.run(["gdal_translate", "-of", "PNG", str(finalTIFF), str(finalPNG)])


#Finalization:
# 1. Parse the date string (YYYY-MM-DD) into a datetime object
processed_date_obj = datetime.strptime(date, '%Y-%m-%d').date()

# 2. Add one day
next_start_date_obj = processed_date_obj + timedelta(days=1)

# 3. Convert back to string
next_start_date_str = next_start_date_obj.strftime('%Y-%m-%d')

config['Other']['last_product_date'] = next_start_date_str

with open(os.path.join(script_dir, 'config_tshoRolpa.ini'), 'w') as configfile:
    config.write(configfile)

with open(finalPath/"date.txt", 'w') as dateFile:
    dateFile.write(date)

