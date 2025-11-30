from osgeo import gdal, ogr
from pathlib import Path

def crop(input_tif, aoi_geojson, outDir):
    output_tif_name = f"{Path(input_tif).stem}_cropped.tif"
    output_tif_path = Path(f"{outDir}/{output_tif_name}")
    # Warp options
    warp_options = gdal.WarpOptions(
        format='GTiff',
        cutlineDSName=aoi_geojson,
        cropToCutline=True,
        dstNodata=0,
        multithread=True,
        xRes=20,            
        yRes=20
    )

    # Perform warp (crop) by passing the input file path as a string
    gdal.Warp(
        destNameOrDestDS=output_tif_path, 
        srcDSOrSrcDSTab=input_tif, 
        options=warp_options
    )
    

    print(f"Cropped raster saved to: {output_tif_path}")
    return output_tif_path
