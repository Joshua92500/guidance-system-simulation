import numpy as np

def compute_aim_point(interceptor, target, elapsed_seconds):
    """Predictive guidance: estimate where the target will be when
    the interceptor arrives and return that point.

    This uses a simple linear extrapolation of the target's current
    velocity. Time-to-intercept is approximated as distance / interceptor_speed.
    """
    try:
        pos_t = np.array(target.position(), dtype=float)
        vel_t = np.array(target.velocity(), dtype=float)
        pos_i = np.array(interceptor.position(), dtype=float)
    except Exception:
        return None

    speed_i = getattr(interceptor, "speed", None)
    if not speed_i or speed_i <= 1e-6:
        return None

    r = pos_t - pos_i
    dist = np.linalg.norm(r)
    if dist <= 1e-6:
        return tuple(pos_t)

    time_to_intercept = dist / speed_i
    predicted = pos_t + vel_t * time_to_intercept
    return (float(predicted[0]), float(predicted[1]), float(predicted[2]))
