import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Target:
    def __init__(self, plot_area, speed, x, y, z, size=100, color="blue", label="Target"):
        self.plot_area = plot_area
        self.speed = speed
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.label = label

        self.dot = self.plot_area.scatter(
                self.x,
                self.y,
                self.z,
                s=self.size,
                color=self.color,
                label=self.label
        )
    
    def move_to(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.dot._offsets3d = ([self.x], [self.y], [self.z])

    def update(self, frame):
        x = 50 + 30 * np.cos(frame * 0.05 * self.speed)
        y = 50 + 30 * np.sin(frame * 0.05 * self.speed)
        z = 50 + 20 * np.sin(frame * 0.03 * self.speed)

        self.move_to(x, y, z)

        return self.dot

    def position(self):
        return self.x, self.y, self.z


'''
PLOT DEFINITION
'''

# Fixed 100 x 100 x 100 space
X_MIN, X_MAX = 0, 100
Y_MIN, Y_MAX = 0, 100
Z_MIN, Z_MAX = 0, 100

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Fixed axis limits
ax.set_xlim(X_MIN, X_MAX)
ax.set_ylim(Y_MIN, Y_MAX)
ax.set_zlim(Z_MIN, Z_MAX)

ax.set_box_aspect((1, 1, 1))

# Labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_title('PLOT 01')


'''
TARGET DEFINITION
'''

target_1 = Target(
        plot_area=ax,
        speed=1,
        x=50,
        y=50,
        z=50,
        size=100,
        color="red",
        label="Target 1"
)


'''
RUN LOOP
'''

def update(frame):
    target_1.update(frame)

    x, y, z = target_1.position()
    ax.set_title(f'Target Position: ({x:.1f}, {y:.1f}, {z:.1f})')

    return target_1.dot


ani = FuncAnimation(
    fig,
    update,
    frames=300,
    interval=30,
    blit=False
)

plt.show()
