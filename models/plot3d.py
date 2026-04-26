import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Plot3D:
    def __init__(self, x_min=0, x_max=100, y_min=0, y_max=100, z_min=0, z_max=100, title='PLOT'):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.title = title
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self._setup_plot()

    def _setup_plot(self):
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        self.ax.set_zlim(self.z_min, self.z_max)
        self.ax.set_box_aspect((1, 1, 1))
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title(self.title)

    def set_title(self, title):
        self.ax.set_title(title)

    def get_figure(self):
        return self.fig

    def get_axis(self):
        return self.ax

    def animate(self, update_func, frames=300, interval=30, blit=False, repeat=True):
        return FuncAnimation(self.fig, update_func, frames=frames, interval=interval, blit=blit, repeat=repeat)