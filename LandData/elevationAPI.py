import requests
import settings
import numpy as np
import rasterio
import logging
from io import BytesIO

logging.basicConfig(level=logging.INFO)

class Tessadem:
    api_key: str = settings.get_elevation_api_key()
    base_url = "https://api.tessadem.xyz"

    def _build_url(self, key=None, **kwargs, ) -> str:
        url = "https://tessadem.com/api/elevation"

        if key:
            url += f"?key={key}"
        else:
            url += f"?key={self.api_key}"

        for kwarg in kwargs:
            url += f"&{kwarg}={kwargs[kwarg]}"

        return url

    def _build_kwargs(self, mode = None, rows = None, columns = None, locations = None, format = None) -> dict:
        kwargs = {}

        if mode:
            kwargs["mode"] = mode

        if rows:
            kwargs["rows"] = rows

        if columns:
            kwargs["columns"] = columns

        if locations:
            kwargs["locations"] = locations

        if format:
            kwargs["format"] = format

        return kwargs

    def getGeoTIFF(self, sw: tuple, ne: tuple, HorizontalStretchFactor) -> rasterio.io.MemoryFile:
        # Calculate the latDiff and longDiff of the bounding box
        width = ne[1] - sw[1]
        height = (ne[0] - sw[0]) * HorizontalStretchFactor

        if width > height:
            columns = 128
            rows = int(height * (columns / width))
        else:
            rows = 128
            columns = int(width * (rows / height))
        
        

        # Build the bounding box for the request
        sw_str = f"{sw[0]:.3f},{sw[1]:.3f}"
        ne_str = f"{ne[0]:.3f},{ne[1]:.3f}"
        url = self._build_url(**self._build_kwargs(mode="area", rows=rows, columns=columns, locations=f"{sw_str}|{ne_str}", format="geotiff"))

        logging.info(f"Requesting GeoTIFF data from {url}")

        response = requests.get(url)

        # Check for request success
        if response.status_code == 200:
            # Read the GeoTIFF data using rasterio from the byte stream
            return rasterio.MemoryFile(response.content)
        else:
            logging.error(f"Failed to retrieve data: {response.status_code} - {response.text}")
            return None
    
    def CheckAPIKeyValidity(self, API_KEY: str):
        url = self._build_url(key=API_KEY, **self._build_kwargs(locations="0,0|0,0"))
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
        
    def getElevationNPArray(self, sw: tuple, ne: tuple, HorizontalStretchFactor):
    # Get the GeoTIFF as a MemoryFile
        tiff = self.getGeoTIFF(sw, ne, HorizontalStretchFactor)
        if tiff is None:
            logging.error("Failed to retrieve GeoTIFF data.")
            return None

        # Open the dataset from the MemoryFile
        with tiff.open() as dataset:
            # Read the first band (elevation data) into a NumPy array
            elevation_data = dataset.read(1)  # Assuming the elevation data is in the first band
        return elevation_data

    
    def getElevationDataGEOTIFF(self, sw: tuple, ne: tuple, HorizontalStretchFactor):
        tiff = self.getGeoTIFF(sw, ne, HorizontalStretchFactor)
        return tiff