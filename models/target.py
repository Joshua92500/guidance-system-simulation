import numpy as np
from .dot import Dot

class Target(Dot):
    def __init__(
        self,
        plot_area,
        speed,
        x,
        y,
        z,
        size=100,
        color="blue",
        label="Target",
        max_turn_rate_deg=5
    ):
        super().__init__(plot_area, speed, x, y, z, size, color, label)
        self.max_turn_rate_deg = max_turn_rate_deg

    def update(self, elapsed_seconds):
        max_turn_rate_rad = np.deg2rad(self.max_turn_rate_deg)

        # Desired position on the path
        x = 50 + 30 * np.cos(elapsed_seconds * (5 / 3) * self.speed)
        y = 50 + 30 * np.sin(elapsed_seconds * (5 / 3) * self.speed)
        z = 50 + 20 * np.sin(elapsed_seconds * self.speed)
        desired_pos = (x, y, z)

        self.update_velocity_towards(desired_pos, max_turn_rate_rad)
        vx, vy, vz = self.velocity()
        new_pos = np.array(self.position()) + np.array([vx, vy, vz])
        self.move_to(*new_pos)
        return self.dot