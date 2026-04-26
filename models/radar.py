import numpy as np

class Radar:
    def __init__(self, owner, range=10):
        self.owner = owner
        self.range = range

    def detect(self, objects):
        closest = None
        min_dist = float('inf')
        for obj in objects:
            if obj is self.owner:
                continue
            dist = np.linalg.norm(np.array(self.owner.position()) - np.array(obj.position()))
            if dist < min_dist and dist <= self.range:
                min_dist = dist
                closest = obj
        return closest