import matplotlib.pyplot as plt
from models.plot3d import Plot3D
import models.target as target
import models.interceptor as interceptor
import models.radar as radar


plot = Plot3D()
ax = plot.get_axis()

targets = [
    target.Target(plot_area=ax, speed=1, x=50, y=50, z=50, size=100, label="Target 1"),
    target.Target(plot_area=ax, speed=1.15, x=20, y=20, z=20, size=50, color="purple", label="Target 2")
]

interceptors = [
    interceptor.Interceptor(plot_area=ax, speed=2, label="Interceptor 1"),
]

# Attach radar(s) to interceptor(s)
for i in interceptors:
    i.radar = radar.Radar(owner=i, range=100)


'''
RUN LOOP
'''

def update(frame):
    dots = []
    positions = []
    for t in targets:
        t.update(frame)
        positions.append(f"{t.label}: ({t.x:.1f}, {t.y:.1f}, {t.z:.1f})")
        dots.append(t.dot)

    for i in interceptors:
        i.update(frame, targets=targets)
        closest = i.radar.detect(targets)
        if closest:
            positions.append(f"{i.label}: ({i.x:.1f}, {i.y:.1f}, {i.z:.1f}) | Closest: {closest.label}")
        else:
            positions.append(f"{i.label}: ({i.x:.1f}, {i.y:.1f}, {i.z:.1f}) | Closest: None")
        dots.append(i.dot)

    plot.set_title(" | ".join(positions))
    return dots


ani = plot.animate(update, frames=300, interval=30, blit=False)
plt.show()
