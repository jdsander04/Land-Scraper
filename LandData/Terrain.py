import LandData.RawMapData as RMD
from PIL import Image
import numpy as np

class Terrain:
    terrainInfo: RMD.RawMapData
    transformedTerrainInfo: RMD.RawMapData

    def __init__(self, sw, ne):
        print(f"Initializing terrain with sw={sw} and ne={ne}")
        self.terrainInfo = RMD.RawMapData(sw, ne)
        self.transformedTerrainInfo = RMD.RawMapData()
        self.transformedTerrainInfo.elevationDataNPArray = self.terrainInfo.elevationDataNPArray / self.terrainInfo.elevationDataNPArray.max()

    def MakePngFile(self, filename):
        """given a numpy array, make a grey scale png file"""

        print(f"Making PNG file {filename}.png")
        array = self.transformedTerrainInfo.elevationDataNPArray

        image = Image.fromarray((array * 255).astype(np.uint8))
        image.save(f"{filename}.png")
