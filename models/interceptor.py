import numpy as np
from .dot import Dot

class Interceptor(Dot):
    def __init__(self, plot_area, speed, x=0, y=0, z=0, size=20, color="red", label="Interceptor", radar=None):
        super().__init__(plot_area, speed, x, y, z, size, color, label)
        self.radar = radar

    def update(self, frame, targets=None):
        # Move toward the closest target if radar and targets are provided
        if self.radar and targets:
            closest = self.radar.detect(targets)
            if closest:
                # Vector from self to target
                direction = np.array(closest.position()) - np.array(self.position())
                dist = np.linalg.norm(direction)
                if dist > 0:
                    # Normalize direction vector
                    direction = direction / dist
                    
                    # Set speed to either self.speed or the distance to the target, whichever is smaller
                    step = min(self.speed, dist)

                    # Move towards the target
                    new_pos = np.array(self.position()) + direction * step
                    self.move_to(*new_pos)
        return self.dot