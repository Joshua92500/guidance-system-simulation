import numpy as np
from .dot import Dot

class Interceptor(Dot):
    def __init__(
        self,
        plot_area,
        speed,
        x=0,
        y=0,
        z=0,
        size=20,
        color="red",
        label="Interceptor",
        radar=None,
        fuse_time=None,
        max_turn_rate_deg=5
    ):
        super().__init__(plot_area, speed, x, y, z, size, color, label)
        self.radar = radar
        self.fuse_time_seconds = fuse_time
        self.max_turn_rate_deg = max_turn_rate_deg
        self.fused = False

    def update(self, elapsed_seconds, targets=None):
        if self.fused:
            return self.dot

        if self.fuse_time_seconds is not None and elapsed_seconds >= self.fuse_time_seconds:
            self.set_velocity(0.0, 0.0, 0.0)
            self.fused = True
            return self.dot

        max_turn_rate_rad = np.deg2rad(self.max_turn_rate_deg)

        if self.radar and targets:
            closest = self.radar.detect(targets)
            if closest:
                self.update_velocity_towards(closest.position(), max_turn_rate_rad)
        vx, vy, vz = self.velocity()
        new_pos = np.array(self.position()) + np.array([vx, vy, vz])
        self.move_to(*new_pos)
        return self.dot