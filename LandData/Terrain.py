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

    def MakeJpgFile(self, filename, folder=None):
        """given a numpy array, make a grey scale png file"""

        print(f"Making JPG file {filename}.jpg")
        array = self.transformedTerrainInfo.elevationDataNPArray

        image = Image.fromarray((array * 255).astype(np.uint8))
        if folder:
            image.save(f"{folder}/{filename}.jpg")
        else:
            image.save(f"{filename}.jpg")

    def MakeObjFile(self, filename, folder=None, scale=0.01, step=3, sample_size=5):
        """
        Export a numpy array as a scaled 3D object in an OBJ file.

        Args:
            filename (str): The name of the OBJ file (without extension).
            folder (str): Optional folder to save the file.
            scale (float): Scaling factor for the output geometry.
            step (int): Step size for iterating over the grid (controls density of vertices).
            sample_size (int): Size of the region for averaging elevation values.
        """
        print(f"Making OBJ file {filename}.obj")

        array = self.terrainInfo.elevationDataNPArray

        if folder:
            filepath = f"{folder}/{filename}.obj"
        else:
            filepath = f"{filename}.obj"

        rows, cols = array.shape
        vertex_rows = (rows - 1) // step + 1
        vertex_cols = (cols - 1) // step + 1

        vertices = []
        faces = []

        # Generate vertices
        for i in range(0, rows - sample_size + 1, step):
            for j in range(0, cols - sample_size + 1, step):
                z = np.mean(array[i:i + sample_size, j:j + sample_size])
                vertices.append((i * scale, j * scale, z * scale))

        # Generate faces
        vert_index = lambda r, c: r * vertex_cols + c + 1
        for r in range(vertex_rows - 1):
            for c in range(vertex_cols - 1):
                # Define two triangles for each cell
                top_left = vert_index(r, c)
                top_right = vert_index(r, c + 1)
                bottom_left = vert_index(r + 1, c)
                bottom_right = vert_index(r + 1, c + 1)

                # Add faces only if they stay within the same row
                if c < vertex_cols - 1:
                    faces.append((top_left, bottom_left, top_right))
                    faces.append((bottom_left, bottom_right, top_right))

        # Write to the OBJ file
        with open(filepath, 'w') as obj_file:
            obj_file.write("# OBJ file\n")
            # Write vertices
            for v in vertices:
                obj_file.write(f"v {v[0]} {v[1]} {v[2]}\n")
            # Write faces
            for f in faces:
                obj_file.write(f"f {f[0]} {f[1]} {f[2]}\n")


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
            crs="EPSG:4326",  # Replace with your actual CRS
            transform=rasterio.transform.from_bounds(
                self.terrainInfo.sw[1], self.terrainInfo.sw[0], 
                self.terrainInfo.ne[1], self.terrainInfo.ne[0], 
                geotiff.shape[1], geotiff.shape[0]
            )
        ) as dst:
            dst.write(geotiff, 1)
