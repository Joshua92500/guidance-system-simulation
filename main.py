import matplotlib.pyplot as plt
from models.plot3d import Plot3D
import models.target as target


plot = Plot3D()
ax = plot.get_axis()

targets = [
    target.Target(plot_area=ax, speed=1, x=50, y=50, z=50, size=100, color="red", label="Target 1"),
    target.Target(plot_area=ax, speed=1.5, x=20, y=20, z=20, size=20, color="green", label="Target 2")
]


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
    plot.set_title(" | ".join(positions))
    return dots


ani = plot.animate(update, frames=300, interval=30, blit=False)
plt.show()
