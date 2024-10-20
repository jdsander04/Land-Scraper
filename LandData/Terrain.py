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
        max = self.terrainInfo.elevationDataNPArray.max()
        min = self.terrainInfo.elevationDataNPArray.min()
        self.transformedTerrainInfo.elevationDataNPArray = (self.terrainInfo.elevationDataNPArray - min) / (max - min) 

    def MakePngFile(self, filename):
        """given a numpy array, make a grey scale png file"""

        print(f"Making PNG file {filename}.png")
        array = self.transformedTerrainInfo.elevationDataNPArray

        image = Image.fromarray((array * 255).astype(np.uint8))
        image.save(f"{filename}.png")

    def MakeObjFile(self, filename):
        """given a numpy array, export it as a 3D object in an OBJ file"""
        
        print(f"Making OBJ file {filename}.obj")
        array = self.transformedTerrainInfo.elevationDataNPArray
        with open(f"{filename}.obj", 'w') as obj_file:
            obj_file.write("# OBJ file\n")
            rows, cols = array.shape
            for i in range(rows):
                for j in range(cols):
                    z = array[i, j]
                    obj_file.write(f"v {i} {j} {z}\n")
            
            for i in range(rows - 1):
                for j in range(cols - 1):
                    obj_file.write(f"f {i * cols + j + 1} {(i + 1) * cols + j + 1} {i * cols + (j + 1) + 1}\n")
                    obj_file.write(f"f {(i + 1) * cols + j + 1} {(i + 1) * cols + (j + 1) + 1} {i * cols + (j + 1) + 1}\n")
