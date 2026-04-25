import numpy as np
from .physics import limit_turn

class Dot:
    def __init__(self, plot_area, speed, x, y, z, size=100, color="grey", label="Dot"):
        self.plot_area = plot_area
        self.speed = speed
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.label = label

        # Initialize velocity vectors
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0

        self.dot = self.plot_area.scatter(
            self.x,
            self.y,
            self.z,
            s=self.size,
            color=self.color,
            label=self.label
        )

    def set_velocity(self, vx, vy, vz):
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def velocity(self):
        return self.vx, self.vy, self.vz

    def update_velocity_towards(self, target_pos, max_turn_rate_rad):
        """
        Update velocity vector to turn toward target_pos, limited by max_turn_rate_rad (in radians per update).
        Sets velocity to self.speed in the new direction.
        """
        current_vel = np.array([self.vx, self.vy, self.vz])
        pos = np.array([self.x, self.y, self.z])
        desired_dir = np.array(target_pos) - pos
        new_vel = limit_turn(current_vel, desired_dir, self.speed, max_turn_rate_rad)
        self.vx, self.vy, self.vz = new_vel

    def move_to(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dot._offsets3d = ([self.x], [self.y], [self.z])

    def update(self):
        return self.dot

    def position(self):
        return self.x, self.y, self.z