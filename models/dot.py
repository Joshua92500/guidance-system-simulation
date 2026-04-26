import math
import numpy as np
from .physics import limit_turn

class Dot:
    def __init__(self, plot_area, speed, x, y, z, size=100, color="grey", label="Dot", radius=None):
        self.plot_area = plot_area
        self.speed = speed
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.label = label

        if radius is not None:
            self.radius = radius
        else:
            # Derive world-space collision radius from the matplotlib marker size.
            # matplotlib size is area in points², so the visual radius is sqrt(s/π) points.
            # Convert points to world units using the axis range and figure width.
            try:
                fig = plot_area.get_figure()
                fig_width_pts = fig.get_size_inches()[0] * 72  # inches → points
                x_min, x_max = plot_area.get_xlim()
                world_range = x_max - x_min
                # ~80 % of the figure width is occupied by the actual 3D plot area
                world_units_per_pt = world_range / (fig_width_pts * 0.8)
                self.radius = math.sqrt(self.size / math.pi) * world_units_per_pt
            except Exception:
                self.radius = 2.0

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