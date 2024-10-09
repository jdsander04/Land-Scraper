import RawMapData as RMD
from PIL import Image

class Terrain:
    terrainInfo = RMD.RawMapData()
    transformedTerrainInfo = RMD.RawMapData()

    def MakePngFile(self, filename):
        """given a numpy array, make a black and whitepng file"""

        array = self.terrainInfo.terrain

        # convert to black and white
        bwArray = (array > 0).astype('uint8') * 255
        # make and save image
        img = Image.fromarray(bwArray)
        img.save(filename + '.png')

    def __init__(self):
        pass