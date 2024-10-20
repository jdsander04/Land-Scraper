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

    def _build_url(self, **kwargs) -> str:
        url = "https://tessadem.com/api/elevation"

        url += f"?key={self.api_key}"

        for kwarg in kwargs:
            url += f"&{kwarg}={kwargs[kwarg]}"

        return url

    def _build_kwargs(self, mode, rows, columns, locations, format) -> dict:
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

    def getGeoTIFF(self, sw: tuple, ne: tuple, HorizontalStretchFactor) -> np.array:
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
            with rasterio.MemoryFile(response.content) as memfile:
                with memfile.open() as dataset:
                    elevation_data = dataset.read(1)  # Read the first band

            logging.info(f"Retrieved GeoTIFF data of shape {elevation_data.shape}")

            return elevation_data
        else:
            logging.error(f"Failed to retrieve data: {response.status_code} - {response.text}")
            return None
