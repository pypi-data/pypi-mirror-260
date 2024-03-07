from matplotlib.cm import ScalarMappable, get_cmap
from matplotlib.colors import Normalize, rgb2hex, hex2color


class GridColormap(dict):
    def __init__(self, colormap, vmin, vmax):
        if colormap and isinstance(colormap, str):
            colormap = ScalarMappable(Normalize(vmin, vmax), get_cmap(colormap))
        if not isinstance(colormap, ScalarMappable):
            raise ("colormap must be a matplotlib colormap name or a ScalarMappable")
        super().__init__(
            {
                "scale": [rgb2hex(c) for c in colormap.cmap.colors],
                "domain": [vmin, vmax],
            }
        )
