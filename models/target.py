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
        max_turn_rate_deg=5,
        show_prediction=False,
        prediction_time=0.25,
        radius=None,
    ):
        super().__init__(plot_area, speed, x, y, z, size, color, label, radius)
        self.max_turn_rate_deg = max_turn_rate_deg
        # Prediction marker settings
        self.show_prediction = show_prediction
        self.prediction_time = prediction_time
        self._pred_outer = None
        self._pred_center = None
        self._pred_line = None
        # For accurate per-second velocity, track previous position/time
        self._last_pos = np.array([self.x, self.y, self.z], dtype=float)
        self._last_time = None
        if self.show_prediction:
            # initial predicted position equals current
            px, py, pz = self.position()
            # hollow outer marker
            try:
                self._pred_outer = self.plot_area.scatter(
                    px, py, pz, s=max(20, int(self.size * 0.5)), facecolors='none', edgecolors='red'
                )
            except Exception:
                self._pred_outer = self.plot_area.scatter(px, py, pz, s=max(20, int(self.size * 0.5)), color='none')
            # small center dot
            self._pred_center = self.plot_area.scatter(px, py, pz, s=max(6, int(self.size * 0.08)), color='red')
            # dotted line from predicted point to actual target
            self._pred_line = self.plot_area.plot([px, px], [py, py], [pz, pz], linestyle=':', color='red')[0]

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

        # Update prediction marker based on measured velocity in units/sec
        if self.show_prediction:
            try:
                pos = np.array(self.position(), dtype=float)
                pred = pos
                if self._last_time is not None:
                    dt = elapsed_seconds - self._last_time
                    if dt > 1e-6:
                        vel_per_sec = (pos - self._last_pos) / dt
                        pred = pos + vel_per_sec * float(self.prediction_time)
                px, py, pz = float(pred[0]), float(pred[1]), float(pred[2])
                # update outer and center
                if self._pred_outer is not None:
                    self._pred_outer._offsets3d = ([px], [py], [pz])
                if self._pred_center is not None:
                    self._pred_center._offsets3d = ([px], [py], [pz])
                # update line between predicted point and current target
                if self._pred_line is not None:
                    self._pred_line.set_data([px, self.x], [py, self.y])
                    self._pred_line.set_3d_properties([pz, self.z])
            except Exception:
                pass

        # record last pos/time for next update
        try:
            self._last_pos = np.array(self.position(), dtype=float)
            self._last_time = elapsed_seconds
        except Exception:
            pass

        return self.dot