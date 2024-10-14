import numpy as np
from LandChunk import LandChunk

class RawMapData:

    def __init__(self, sw, ne):
        """
        Create a new RawMapData object from a given bounding box

        :param sw: tuple of (longitude, latitude) of the southwest corner of the bounding box
        :param ne: tuple of (longitude, latitude) of the northeast corner of the bounding box
        """
        self.sw = sw
        self.ne = ne

        self.elevationDataNPArray: np.array = self.createMapData(sw, ne)

    def __init__(self, other):
        """
        Create a copy of another RawMapData object
        :param other: another RawMapData object to copy
        """
        self.sw = other.sw
        self.ne = other.ne

        self.elevationDataNPArray: np.array = other.elevationDataNPArray.copy()

    def createMapData(self, sw, ne):
        print(f"Creating map data for sw={sw} and ne={ne}")

        latWidth = (ne[0] - sw[0]) / 8  # Divide the range into 8 sections
        longWidth = (ne[1] - sw[1]) / 8
        mapDataChunkCoords = []

        # Create coordinate pairs for each LandChunk
        for i in range(8):
            row = []
            for j in range(8):
                chunk_sw = (sw[0] + (i * latWidth), sw[1] + (j * longWidth))
                chunk_ne = (sw[0] + ((i + 1) * latWidth), sw[1] + ((j + 1) * longWidth))
                row.append((chunk_sw, chunk_ne))
            mapDataChunkCoords.append(row)

        # Initialize a list to hold the elevation data
        elevation_data_chunks = np.zeros((8, 8), dtype=object)

        # Retrieve elevation data from each LandChunk
        for i in range(8):
            for j in range(8):
                coordPair = mapDataChunkCoords[i][j]
                landChunk = LandChunk(coordPair[0], coordPair[1])
                elevation_data_chunks[i, j] = landChunk.getElevationDataNPArray()

                # Debug: Check the shape of each chunk
                print(f"LandChunk at ({i}, {j}) shape: {elevation_data_chunks[i, j].shape}")

        # Flip the order of the chunks vertically (reverse rows of chunks)
        elevation_data_chunks_flipped = elevation_data_chunks[::-1]

        # Stack the chunks into a single 1024x1024 array
        largeNPArray = np.vstack([np.hstack(elevation_data_chunks_flipped[i]) for i in range(8)])

        print(f"Finished creating map data for sw={sw} and ne={ne}")
        print(f"Final shape of largeNPArray: {largeNPArray.shape}")  # Should be (1024, 1024)
        return largeNPArray
    
    
    def __copy__(self):
        new_one = type(self)(self.sw, self.ne)
        new_one.elevationDataNPArray = self.elevationDataNPArray.copy()
        return new_one
