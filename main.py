import matplotlib.pyplot as plt
from models.plot3d import Plot3D
import models.target as target
import models.interceptor as interceptor
import models.radar as radar
import models.guidance.predictive as predictive

ANIMATION_INTERVAL_MS = 30
plot = Plot3D()
ax = plot.get_axis()

targets = [
    target.Target(plot_area=ax, speed=0.8, x=50, y=50, z=50, size=100, label="Target 1", show_prediction=True),
    target.Target(plot_area=ax, speed=1.5, x=80, y=80, z=50, size=50, color="purple", label="Target 2", show_prediction=True)
]

interceptors = [
    interceptor.Interceptor(plot_area=ax, speed=1.5, label="Interceptor 1", fuse_time=None, show_aim=True),
]

# Attach radar(s) to interceptor(s)
for i in interceptors:
    i.radar = radar.Radar(owner=i, range=80)
    i.add_guidance(predictive)


'''
RUN LOOP
'''

def update(frame):
    dots = []
    objects = []
    positions = []
    elapsed_seconds = frame * ANIMATION_INTERVAL_MS / 1000
    timer_str = f"Time: {elapsed_seconds:.2f}s"

    for t in targets:
        t.update(elapsed_seconds)
        positions.append(f"{t.label}: ({t.x:.1f}, {t.y:.1f}, {t.z:.1f})")
        objects.append(t)
        dots.append(t.dot)

    for i in interceptors:
        i.update(elapsed_seconds, targets=targets)
        closest = i.radar.detect(targets)
        if closest:
            positions.append(f"{i.label}: ({i.x:.1f}, {i.y:.1f}, {i.z:.1f}) | Closest: {closest.label}")
        else:
            positions.append(f"{i.label}: ({i.x:.1f}, {i.y:.1f}, {i.z:.1f}) | Closest: None")
        objects.append(i)
        dots.append(i.dot)

    # Collision detection between all object pairs
    n = len(objects)
    for a in range(n):
        for b in range(a+1, n):
            oa = objects[a]
            ob = objects[b]
            dx = oa.x - ob.x
            dy = oa.y - ob.y
            dz = oa.z - ob.z
            dist_sq = dx*dx + dy*dy + dz*dz
            thresh = (getattr(oa, "radius", 1.0) + getattr(ob, "radius", 1.0))
            if dist_sq <= thresh * thresh:
                plot.set_title(f"{timer_str} | COLLISION: {oa.label} & {ob.label} @ {elapsed_seconds:.2f}s")
                try:
                    ani.event_source.stop()
                except Exception:
                    pass
                return dots

    plot.set_title(f"{timer_str} | " + " | ".join(positions))
    return dots


ani = plot.animate(update, frames=3000, interval=ANIMATION_INTERVAL_MS, blit=False, repeat=False)
plt.show()
