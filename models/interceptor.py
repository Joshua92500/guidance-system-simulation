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
        max_turn_rate_deg=10,
        show_aim=False,
        radius=None,
    ):
        super().__init__(plot_area, speed, x, y, z, size, color, label, radius)
        self.radar = radar
        self.fuse_time_seconds = fuse_time
        self.max_turn_rate_deg = max_turn_rate_deg
        self.fused = False
        self.origin = (x, y, z)
        self.fuse_armed = False
        self.fuse_start_time = None
        self.guidance = []
        self.show_aim = bool(show_aim)
        self._aim_outer = None
        self._aim_center = None

    def add_guidance(self, guidance_module):
        """
        Register a guidance module for the interceptor.
        """
        self.guidance.append(guidance_module)

    def update(self, elapsed_seconds, targets=None):
        if self.fused:
            return self.dot

        # Arm the fuse only after the interceptor launches (velocity becomes non-zero).
        if self.fuse_time_seconds is not None:
            try:
                vx, vy, vz = self.velocity()
                speed_now = np.linalg.norm(np.array([vx, vy, vz]))
            except Exception:
                speed_now = 0.0

            if (not self.fuse_armed) and (speed_now > 1e-6):
                self.fuse_armed = True
                self.fuse_start_time = elapsed_seconds

            if self.fuse_armed and self.fuse_start_time is not None:
                if (elapsed_seconds - self.fuse_start_time) >= self.fuse_time_seconds:
                    self.set_velocity(0.0, 0.0, 0.0)
                    self.fused = True
                    return self.dot

        max_turn_rate_rad = np.deg2rad(self.max_turn_rate_deg)

        if self.radar and targets:
            closest = self.radar.detect(targets)
            if closest:
                '''
                Guidance logic:
                1. Check for guidance modules that implement `compute_aim_point`.
                2. If found, use it to compute the aim point based on the closest target and elapsed time.
                3. If no guidance module is available or it fails, default to aiming at the target's current position.
                '''
                aim_point = None
                guidance_module = next((g for g in self.guidance if hasattr(g, "compute_aim_point")), None)
                if guidance_module is not None:
                    try:
                        aim_point = guidance_module.compute_aim_point(self, closest, elapsed_seconds)
                    except Exception:
                        aim_point = None

                if aim_point is None:
                    aim_point = closest.position()

                # Draw/update aiming marker if enabled
                if getattr(self, "show_aim", False):
                    try:
                        px, py, pz = float(aim_point[0]), float(aim_point[1]), float(aim_point[2])
                        # initialize marker objects if not present
                        if self._aim_outer is None:
                            try:
                                self._aim_outer = self.plot_area.scatter(
                                    px, py, pz,
                                    s=max(12, int(self.size * 0.5)),
                                    facecolors='none',
                                    edgecolors='lightgrey'
                                )
                            except Exception:
                                self._aim_outer = self.plot_area.scatter(px, py, pz, s=max(12, int(self.size * 0.5)), color='none')
                            self._aim_center = self.plot_area.scatter(px, py, pz, s=max(4, int(self.size * 0.08)), color='lightgrey')
                        else:
                            if self._aim_outer is not None:
                                self._aim_outer._offsets3d = ([px], [py], [pz])
                            if self._aim_center is not None:
                                self._aim_center._offsets3d = ([px], [py], [pz])
                    except Exception:
                        pass

                self.update_velocity_towards(aim_point, max_turn_rate_rad)
        vx, vy, vz = self.velocity()
        new_pos = np.array(self.position()) + np.array([vx, vy, vz])
        self.move_to(*new_pos)
        return self.dot