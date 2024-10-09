import numpy as np

class LandChunk:
    def __init__(self, data: np.ndarray, origin: tuple):
        if data.shape[0] > 128 or data.shape[1] > 128:
            raise ValueError("data must be a 2D numpy array up to 128x128")
        self.data = data
        self.origin = origin
