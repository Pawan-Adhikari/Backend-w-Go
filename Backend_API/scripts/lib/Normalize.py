import rasterio
import numpy as np
from pathlib import Path
from scipy.ndimage import uniform_filter
from scipy.ndimage import variance

def lee_filter(img, size=2):
    """
    Applies a Standard Lee Filter to remove SAR speckle.
    """
    # Ensure image is float to avoid overflow during math
    img = img.astype(np.float32)
    
    # Calculate local mean and variance
    img_mean = uniform_filter(img, (size, size))
    img_sqr_mean = uniform_filter(img**2, (size, size))
    img_variance = img_sqr_mean - img_mean**2
    
    # Calculate overall image variance (sigma^2)
    overall_variance = variance(img)
    
    # Calculate weights (K)
    # K = Var_local / (Var_local + Var_overall)
    # 1e-10 prevents division by zero
    img_weights = img_variance / (img_variance + overall_variance + 1e-10)
    
    # Calculate output: Mean + K * (Pixel - Mean)
    img_output = img_mean + img_weights * (img - img_mean)
    
    return img_output

def normalize_leefilter(input_tif, outDir):
    try:
        with rasterio.open(input_tif) as src:
            # Read the data from the first band
            data = src.read(1)

            # Get the original nodata value
            nodata_val = src.nodata
            
            # --- STEP 1: APPLY LEE FILTER ---
            # We filter the RAW data immediately to remove speckle before statistics
            print(f"Applying Lee Filter to {Path(input_tif).name}...")
            filtered_data = lee_filter(data, size=5)

            # --- STEP 2: MASKING ---
            # Create a mask for valid data pixels using the ORIGINAL source logic
            if nodata_val is not None:
                valid_mask = data != nodata_val
                # Use the FILTERED data for the histogram stats
                valid_pixels = filtered_data[valid_mask]
            else:
                valid_mask = np.ones_like(data, dtype=bool)
                valid_pixels = filtered_data

            # --- STEP 3: NORMALIZATION (Histogram Equalization) ---
            # Get the minimum and maximum values from the valid filtered data
            min_val = np.min(valid_pixels)
            max_val = np.max(valid_pixels)

            # Create a histogram of the valid pixels
            hist, bins = np.histogram(valid_pixels, bins=256, range=(min_val, max_val))
            
            # Calculate the cumulative distribution function (CDF)
            cdf = hist.cumsum()
            
            # Normalize the CDF to the full 0-255 range
            cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())

            # Use the CDF to map the FILTERED data to the new range
            equalized_data = np.interp(filtered_data, bins[:-1], cdf_normalized)

            # --- STEP 4: CLEANUP ---
            # Ensure nodata values are cleaned up (set to 0) in the new data
            # The filter might have smeared values into nodata areas, so we hard-reset them.
            if nodata_val is not None:
                equalized_data[~valid_mask] = 0
            
            # Get the original metadata
            profile = src.profile

            # Update the profile for the new 8-bit output
            profile.update(
                dtype=rasterio.uint8,
                nodata=0,
                count=1,
            )

            output_tif_name = f"{Path(input_tif).stem}_filtered_normalised.tif"
            output_tif_path = Path(outDir) / output_tif_name

            # Save the equalized data to the new file
            with rasterio.open(output_tif_path, 'w', **profile) as dst:
                dst.write(equalized_data.astype(rasterio.uint8), 1)

        print(f"Successfully processed '{input_tif}' -> '{output_tif_path}'.")

    except rasterio.RasterioIOError as e:
        print(f"Rasterio error: Could not open or process '{input_tif}'. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
        
    return output_tif_path