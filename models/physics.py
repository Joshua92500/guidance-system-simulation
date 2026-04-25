import numpy as np

def limit_turn(current_vel, desired_dir, speed, max_turn_rate_rad):
    """
    Returns a new velocity vector, rotated from current_vel toward desired_dir by at most max_turn_rate_rad.
    """
    if np.linalg.norm(desired_dir) == 0:
        return current_vel
    desired_dir = desired_dir / np.linalg.norm(desired_dir)
    if np.linalg.norm(current_vel) == 0:
        # If not moving, instantly set velocity in desired direction
        return desired_dir * speed
    current_dir = current_vel / np.linalg.norm(current_vel)
    dot = np.clip(np.dot(current_dir, desired_dir), -1.0, 1.0)
    angle = np.arccos(dot)
    if angle < 1e-6:
        new_dir = desired_dir
    else:
        turn_angle = min(angle, max_turn_rate_rad)
        axis = np.cross(current_dir, desired_dir)
        if np.linalg.norm(axis) < 1e-6:
            new_dir = desired_dir
        else:
            axis = axis / np.linalg.norm(axis)
            # Rodrigues' rotation formula
            new_dir = (
                current_dir * np.cos(turn_angle)
                + np.cross(axis, current_dir) * np.sin(turn_angle)
                + axis * np.dot(axis, current_dir) * (1 - np.cos(turn_angle))
            )
    return new_dir / np.linalg.norm(new_dir) * speed
