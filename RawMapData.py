import numpy as np
from LandChunk import LandChunk

class RawMapData:
    def __init__(self, sw, ne):
        self.sw = sw
        self.ne = ne

        self.elevationDataNPArray: np.array = self.createMapData(sw, ne)



        pass

    def createMapData(self, sw, ne):
        """
        Create a 2d numpy array of the given shape to store 64 equally sized rectangles of the given sw and ne coordinates.
        
        Given a sw and ne coordinate, this function will create a 2d numpy array of shape (8,8) with each element being a tuple 
        of two tuples that represent the sw and ne coordinates of each equally sized rectangle in the 2d array. The 2d array
        is structured such that the first index of the array (i) represents the row number of the rectangle, and the second index
        of the array (j) represents the column number of the rectangle. Thus, the element at array[i][j] is the sw and ne coordinates
        of the rectangle at row i and column j in the 2d array.

        Parameters:
        sw (tuple): The sw coordinates of the 2d array.
        ne (tuple): The ne coordinates of the 2d array.

        Returns:
        np.array: A 2d numpy array of shape (8,8) with each element being a tuple of two tuples that represent the sw and ne
        coordinates of each equally sized rectangle in the 2d array.
        """

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

        return largeNPArray