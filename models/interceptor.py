from .dot import Dot

class Interceptor(Dot):
    def __init__(self, plot_area, speed, x=0, y=0, z=0, size=20, color="red", label="Interceptor", radar=None):
        super().__init__(plot_area, speed, x, y, z, size, color, label)
        self.radar = radar

    def update(self, frame):
        # Placeholder movement towards (100, 100, 100)
        x = self.x + self.speed * 0.5
        y = self.y + self.speed * 0.5
        z = self.z + self.speed * 0.5
        self.move_to(x, y, z)
        return self.dot