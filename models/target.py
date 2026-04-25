import numpy as np
from .dot import Dot

class Target(Dot):
    def __init__(self, plot_area, speed, x, y, z, size=100, color="blue", label="Target"):
        super().__init__(plot_area, speed, x, y, z, size, color, label)

    def update(self, frame):
        x = 50 + 30 * np.cos(frame * 0.05 * self.speed)
        y = 50 + 30 * np.sin(frame * 0.05 * self.speed)
        z = 50 + 20 * np.sin(frame * 0.03 * self.speed)
        self.move_to(x, y, z)
        return self.dot