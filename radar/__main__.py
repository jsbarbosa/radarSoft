import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import to_rgb

from radar.connection.constants import MAX_DISTANCE
from radar.connection.core import find_devices, RadarSerial

plt.style.use('dark_background')

device = find_devices()[0]

serial = RadarSerial(device)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

dots = ax.scatter(
    [],
    [],
    s=25,
    edgecolors='w'
)

show_last = 120
all_alphas = np.linspace(0, 1, show_last)

facecolor = to_rgb(dots.get_facecolors()[0])
edgecolor = to_rgb(dots.get_edgecolors()[0])

dots_points = np.array([[], []])

line, = ax.plot(
    [],
    []
)

ax.set_ylim(0, MAX_DISTANCE)

x = np.arange(0, 136, 15)

ax.set_xticks(np.deg2rad(x))
ax.set_xticklabels(x)

ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=4))

ax.grid(
    ls='-.', lw=0.25
)


def anim(i):
    global dots, serial, dots_points, line
    try:
        angle, distance = serial.read_angle_distance()
        angle = np.deg2rad(angle)

        if distance == MAX_DISTANCE:
            distance *= 1.1

        dots_points = np.hstack(
            [
                dots_points,
                [[angle], [distance]]
            ]
        )[:, -show_last:]

        dots.set_offsets(
            dots_points.T
        )

        line.set_data(
            [angle, angle],
            [0, MAX_DISTANCE]
        )

        i = dots_points.shape[1]
        if i < show_last:
            alphas = all_alphas[show_last - i:].reshape(-1, 1)

            dots.set_facecolor(
                np.hstack(
                    [np.tile(facecolor, (i, 1)), alphas]
                )
            )

            dots.set_edgecolor(
                np.hstack(
                    [np.tile(edgecolor, (i, 1)), alphas]
                )
            )

    except UnicodeDecodeError:
        pass

    return dots, line


ani = FuncAnimation(
    fig,
    anim,
    blit=True,
    interval=0
)

plt.show()
