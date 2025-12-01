# Imports and libraries
import asf_search as asf
from pathlib import Path
from lib.Normalize import normalize_leefilter
from lib.Padding import pad
from lib.Cropping import crop
from datetime import date
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

if (start_date==str(end_date)):
    #print("Scanned just today!!")
    sys.exit(2)

#Searching:
results = asf.geo_search(intersectsWith=wkt,
                        platform=[asf.PLATFORM.SENTINEL1],
                        processingLevel=[asf.PRODUCT_TYPE.RTC,asf.PRODUCT_TYPE.RTC_STATIC],
                        start=start_date,
                        end=end_date)


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
    "wget", "-O", str(tifPath), "-c", url
])


#Preprocessing:
tifPathCropped = crop(tifPath, geojsonPath, tifDir)
tifPathPadded = pad(tifPathCropped, tifDir)
tifPathNormalized = normalize_leefilter(tifPathPadded, tifDir)


#Final Copy:    
finalPath = Path(script_dir).parent / "public" / "data" / "TshoRolpa"
finalPath.mkdir(exist_ok=True)
finalTIFF = finalPath / tifPathNormalized.name
finalPNG = finalPath / (str(tifPathNormalized.stem) + ".png")
subprocess.run(["cp", tifPathNormalized, finalPath])
subprocess.run(["gdal_translate", "-of", "PNG", str(finalTIFF), str(finalPNG)])


#Finalization:
config['Other']['last_product_date'] = date

with open(os.path.join(script_dir, 'config_tshoRolpa.ini'), 'w') as configfile:
    config.write(configfile)