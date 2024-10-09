import requests
import settings
import numpy as np
import geotiff

class Tessadem:
    def __init__(self):
        self.api_key = settings.TESSADEM_API_KEY
        self.base_url = "https://api.tessadem.xyz"

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

    def getGeoTIFF(self, ) -> np.array:
        # example url
        # https://tessadem.com/api/elevation?key=KEY&mode=area&rows=128&columns=128&locations=42.701,2.897|46.268,6.099&format=geotiff
        url = self._build_url(**self._build_kwargs(mode="area", rows=128, columns=128, locations="42.701,2.897|46.268,6.099", format="geotiff"))

        response = requests.get(url)

# Check for request success
        if response.status_code == 200:
            # Save the GeoTIFF data to a file
            # with open('elevation_data.tif', 'wb') as file:
            #     file.write(response.content)

            # Convert the GeoTIFF to a numpy array
            with geotiff.GeoTiffFile('elevation_data.tif') as tif:
                elevation_data = tif.read(band=1)

            return elevation_data
        else:
            print(f"Failed to retrieve data: {response.status_code} - {response.text}")
