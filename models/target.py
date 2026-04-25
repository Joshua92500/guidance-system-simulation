import numpy as np

class Target:
    def __init__(self, plot_area, speed, x, y, z, size=100, color="blue", label="Target"):
        self.plot_area = plot_area
        self.speed = speed
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.label = label

        self.dot = self.plot_area.scatter(
                self.x,
                self.y,
                self.z,
                s=self.size,
                color=self.color,
                label=self.label
        )
    
    def move_to(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.dot._offsets3d = ([self.x], [self.y], [self.z])

    def update(self, frame):
        x = 50 + 30 * np.cos(frame * 0.05 * self.speed)
        y = 50 + 30 * np.sin(frame * 0.05 * self.speed)
        z = 50 + 20 * np.sin(frame * 0.03 * self.speed)

        self.move_to(x, y, z)

        return self.dot

    def position(self):
        return self.x, self.y, self.z