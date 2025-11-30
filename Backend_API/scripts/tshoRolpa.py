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


#Initiation:
config = configparser.ConfigParser()
config.read('config_tshoRolpa.ini')
start_date=config.get('Other','last_product_date')
usr = config.get('Login','user')
pas = config.get('Login','password')
wkt = config.get('Other','wkt')   
loc=config.get('Other','store_location')

today=date.today()
end_date = today
if (start_date==str(end_date)):
    print("Scanned just today!!")
    exit()

#Searching:
results = asf.geo_search(intersectsWith=wkt,
                        platform=[asf.PLATFORM.SENTINEL1],
                        processingLevel=[asf.PRODUCT_TYPE.RTC,asf.PRODUCT_TYPE.RTC_STATIC],
                        start=start_date,
                        end=end_date)


#Crash if no results found
if not results:
    print("No scenes found. Exiting.")
    exit()


#Display found products:
first_result = results[0]
print(first_result)


#Choosing _VV.tif files to download:
date = re.sub("T.*", "", first_result.properties['startTime'])
url = first_result.properties['additionalUrls'][2]
tifPath = loc + date + "/" + date + '.tif'
tifDir = loc + date


#Creating directiory to store backup:
Path(tifDir).mkdir(exist_ok=True)


#Download:
subprocess.run([
    "wget", "-O", tifPath, "-c", url
])


#Preprocessing:
tifPathCropped = crop(tifPath, "./Response/tshoRolpa/tshoRolpaAOI.geojson", tifDir)
tifPathPadded = pad(tifPathCropped, tifDir)
tifPathNormalized = normalize_leefilter(tifPathPadded, tifDir)


#Final Copy:
finalPath = '../public/data/TshoRolpa/'
finalTIFF = finalPath + tifPathNormalized.name
finalPNG = finalPath + tifPathNormalized.stem + ".png"
subprocess.run(["cp", tifPathNormalized, finalPath])
subprocess.run(["gdal_translate", "-of", "PNG", str(finalTIFF), str(finalPNG)])


#Finalization:
config['Other']['last_product_date'] = date

with open('config_tshoRolpa.ini', 'w') as configfile:
    config.write(configfile)