import numpy as np
from LandChunk import LandChunk

class RawMapData:
    def __init__(self, sw, ne):
        self.sw = sw
        self.ne = ne

        self.elevationDataNPArray: np.array = self.createMapData(sw, ne)



        pass

    def createMapData(self, sw, ne):
        """used chuncks to create map data"""

        # given that the shape given be the sw and ne cooridnates, make an 8x8 2d array of touples of touples coordinates
        # so that the sw ne coords can be split into 64 equaly sized rectangles
        latWidth = (ne[0] - sw[0]) / 8
        longWidth = (ne[1] - sw[1]) / 8
        mapDataChunkCoords = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(((sw[0] + (i * latWidth), sw[1] + (j * longWidth)), 
                            (sw[0] + ((i+1) * latWidth), sw[1] + ((j+1) * longWidth))))
            mapDataChunkCoords.append(row)

        mapDataNPArray = np.zeros((8, 8), dtype=object)
        for i, row in enumerate(mapDataChunkCoords):
            for j, coordPair in enumerate(row):
                landChunk = LandChunk(coordPair[0], coordPair[1])
                mapDataNPArray[i, j] = landChunk.getElevationDataNPArray()

        largeNPArray = np.concatenate([np.concatenate(row, axis=0) for row in mapDataNPArray], axis=0)
        

        pass