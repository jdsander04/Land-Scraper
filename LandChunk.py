import numpy as np
from elevationAPI import Tessadem as Tessadem

class LandChunk:
    def __init__(self, sw: tuple, ne: tuple):
        self.sw = sw
        self.ne = ne

        self.elevationDataNPArray = Tessadem.getGeoTIFF(self.sw, self.ne)

    def getElevationDataNPArray(self, ):
        return self.elevationDataNPArray