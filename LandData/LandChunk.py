import numpy as np
from LandData.elevationAPI import Tessadem
class LandChunk:

    API: Tessadem = Tessadem()

    def __init__(self, sw: tuple, ne: tuple):
        self.sw = sw
        self.ne = ne

        print(f"Creating LandChunk with sw={sw} and ne={ne}")
        self.elevationDataNPArray = self.API.getGeoTIFF(sw=self.sw, ne=self.ne)
        print(f"Finished creating LandChunk with sw={sw} and ne={ne}")

    def getElevationDataNPArray(self, ):
        return self.elevationDataNPArray
