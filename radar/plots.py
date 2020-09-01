import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.colors import to_rgb

import radar.connection.constants as c_constants

plt.style.use('dark_background')


class RadarCanvas(FigureCanvasQTAgg):
    SHOW_LAST_NDOTS: int = 45
    WIDTH: float = 5.
    HEIGHT: float = 5.
    DPI: int = 72

    def __init__(self):
        self._fig, self._ax = plt.subplots(subplot_kw={'projection': 'polar'})
        super(RadarCanvas, self).__init__(self._fig)

        self._scatter = self._ax.scatter(
            [],
            [],
            s=25,
            edgecolors='w'
        )

        self._alphas = np.linspace(0, 1, self.SHOW_LAST_NDOTS)

        self._facecolor = to_rgb(self._scatter.get_facecolors()[0])
        self._edgecolor = to_rgb(self._scatter.get_edgecolors()[0])

        self._line, = self._ax.plot(
            [],
            []
        )

        self._data = np.array([[], []])

        self.configure_axis()

        self.draw()
        self._background = self.copy_from_bbox(self._fig.bbox)

    @property
    def fig(self):
        return self._fig

    @property
    def ax(self):
        return self._ax

    def append_data(self, angle: float, distance: float):
        angle = np.deg2rad(angle)
        distance = distance if distance < c_constants.MAX_DISTANCE else np.nan
        self._data = np.hstack(
            [
                self._data,
                [[angle], [distance]]
            ]
        )[:, -self.SHOW_LAST_NDOTS:]

        self._update_plot(angle)

    def _update_plot(self, angle: float):
        self._scatter.set_offsets(
            self._data.T
        )
        self._line.set_data(
            [angle, angle],
            [0, c_constants.MAX_DISTANCE]
        )

        i = self._data.shape[1]
        if i < self.SHOW_LAST_NDOTS:
            alphas = self._alphas[self.SHOW_LAST_NDOTS - i:].reshape(-1, 1)

            self._scatter.set_facecolor(
                np.hstack(
                    [np.tile(self._facecolor, (i, 1)), alphas]
                )
            )

            self._scatter.set_edgecolor(
                np.hstack(
                    [np.tile(self._edgecolor, (i, 1)), alphas]
                )
            )
        self.blit_draw()

    def blit_draw(self):
        self.restore_region(self._background)
        self._ax.draw_artist(self._scatter)
        self._ax.draw_artist(self._line)
        self.blit(self._fig.bbox)
        self.flush_events()

    def rotate_plot(self, angle: float):
        self.redraw(self._ax.set_theta_offset, np.deg2rad(angle))

    def configure_axis(self):
        self._ax.set_ylim(0, c_constants.MAX_DISTANCE)

        x = np.arange(0, 136, 15)

        self._ax.set_xticks(np.deg2rad(x))
        self._ax.set_xticklabels(x)

        self._ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=4))

        self._ax.grid(
            ls='-.', lw=0.25
        )

    def redraw(self, func=None, *args, **kwargs):
        self._ax.clear()
        if func is not None:
            func(*args, **kwargs)

        self.configure_axis()
        self.draw()
        self._background = self.copy_from_bbox(self._fig.bbox)

        self.flush_events()
