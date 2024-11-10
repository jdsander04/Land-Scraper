import numpy as np
from LandData.LandChunk import LandChunk
from multiprocessing import Pool, cpu_count

class RawMapData:

    def __init__(self, sw=None, ne=None):
        """
        Create a new RawMapData object from a given bounding box.

        :param sw: tuple of (longitude, latitude) of the southwest corner of the bounding box
        :param ne: tuple of (longitude, latitude) of the northeast corner of the bounding box
        """
        if sw is not None and ne is not None:
            self.sw = sw
            self.ne = ne
            self.elevationDataNPArray: np.array = self.createMapData(sw, ne)

    def create_chunk(self, coords):
        """
        Helper method to create a LandChunk and retrieve its elevation data.
        
        :param coords: Tuple containing SW and NE coordinates for a chunk
        :return: NumPy array with elevation data for the chunk
        """
        chunk_sw, chunk_ne, stretch_factor = coords
        land_chunk = LandChunk(chunk_sw, chunk_ne, stretch_factor)
        return land_chunk.getElevationDataNPArray()

    def createMapData(self, sw, ne):
        print(f"Creating map data for sw={sw} and ne={ne}")

        # Compute the average latitude and horizontal stretch factor
        averageLat = (ne[0] + sw[0]) / 2
        HorizontalStretchFactor = 1 / (np.cos(averageLat * np.pi / 180))

        # Define the width of each chunk
        latWidth = (ne[0] - sw[0]) / 8
        longWidth = (ne[1] - sw[1]) / 8
        chunk_coords = []

        # Create coordinate pairs for each LandChunk
        for i in range(8):
            for j in range(8):
                chunk_sw = (sw[0] + (i * latWidth), sw[1] + (j * longWidth))
                chunk_ne = (sw[0] + ((i + 1) * latWidth), sw[1] + ((j + 1) * longWidth))
                chunk_coords.append((chunk_sw, chunk_ne, HorizontalStretchFactor))

        # Use multiprocessing to fetch elevation data for each chunk
        with Pool(cpu_count()) as pool:
            elevation_data_chunks = pool.map(self.create_chunk, chunk_coords)

        # Arrange elevation data chunks into an 8x8 grid
        elevation_data_chunks_grid = []
        for i in range(8):
            row = elevation_data_chunks[i * 8:(i + 1) * 8]
            elevation_data_chunks_grid.append(row)

        # Flip the order of the chunks vertically (reverse rows of chunks)
        elevation_data_chunks_flipped = elevation_data_chunks_grid[::-1]

        # Stack the chunks into a single large array
        largeNPArray = np.vstack([np.hstack(row) for row in elevation_data_chunks_flipped])

        print(f"Finished creating map data for sw={sw} and ne={ne}")
        print(f"Final shape of largeNPArray: {largeNPArray.shape}")  # Should be (1024, 1024) if chunks are 128x128
        return largeNPArray

    def __copy__(self):
        new_one = type(self)(self.sw, self.ne)
        new_one.elevationDataNPArray = self.elevationDataNPArray.copy()
        return new_one
