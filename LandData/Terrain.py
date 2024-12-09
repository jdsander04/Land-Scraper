import LandData.RawMapData as RMD
from PIL import Image
import numpy as np
import rasterio


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

    def MakePngFile(self, filename, folder=None):
        """given a numpy array, make a grey scale png file"""

        print(f"Making PNG file {filename}.png")
        array = self.transformedTerrainInfo.elevationDataNPArray

        image = Image.fromarray((array * 255).astype(np.uint8))
        if folder:
            image.save(f"{folder}/{filename}.png")
        else:
            image.save(f"{filename}.png")

    def MakeObjFile(self, filename, folder=None):
        """Given a numpy array, export it as a scaled 3D object in an OBJ file"""

        print(f"Making OBJ file {filename}.obj")
        array = self.terrainInfo.elevationDataNPArray
        if folder:
            filepath = f"{folder}/{filename}.obj"
        else:
            filepath = f"{filename}.obj"

        # Scaling factor to reduce size to 1%
        scale = 0.01

        with open(filepath, 'w') as obj_file:
            obj_file.write("# OBJ file\n")
            rows, cols = array.shape
            for i in range(0, rows - 4, 3):
                for j in range(0, cols - 4, 3):
                    z = np.mean(array[i:i+5, j:j+5])
                    obj_file.write(f"v {i * scale} {j * scale} {z * scale}\n")

            for i in range(0, rows - 4, 3):
                for j in range(0, cols - 4, 3):
                    obj_file.write(f"f {i * cols + j + 1} {(i + 3) * cols + j + 1} {i * cols + (j + 3) + 1}\n")
                    obj_file.write(f"f {(i + 3) * cols + j + 1} {(i + 3) * cols + (j + 3) + 1} {i * cols + (j + 3) + 1}\n")

    def MakeGeotiffFile(self, filename, folder=None):
        print(f"Making GeoTIFF file {filename}.tif")
        geotiff = self.terrainInfo.elevationDataNPArray

        if folder:
            filepath = f"{folder}/{filename}.tif"
        else:
            filepath = f"{filename}.tif"
        with rasterio.open(
            filepath,
            'w',
            driver='GTiff',
            height=geotiff.shape[0],
            width=geotiff.shape[1],
            count=1,
            dtype=geotiff.dtype,
            crs=self.terrainInfo.sw[0],  # This is the crs of the data
            transform=rasterio.transform.from_bounds(
                self.terrainInfo.sw[1], self.terrainInfo.sw[0], self.terrainInfo.ne[1], self.terrainInfo.ne[0], 
                geotiff.shape[1], geotiff.shape[0]
            )
        ) as dst:
            dst.write(geotiff, 1)
