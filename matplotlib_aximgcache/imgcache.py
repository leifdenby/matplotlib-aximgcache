from PIL.PngImagePlugin import PngInfo
import matplotlib.pyplot as plt
import io
from PIL import Image


def create_image_from_ax(ax, **kwargs):
    """
    Create an Image object from the content of a matplotlib.Axes which can be saved to a PNG-file
    source: https://stackoverflow.com/a/43099136/271776
    """
    ax.axis("off")
    ax.figure.canvas.draw()
    trans = ax.figure.dpi_scale_trans.inverted()
    bbox = ax.bbox.transformed(trans)
    buff = io.BytesIO()
    ax.figure.savefig(buff, format="png", dpi=ax.figure.dpi, bbox_inches=bbox, **kwargs)
    ax.axis("on")
    buff.seek(0)
    return Image.open(buff)


def save_ax_to_image(ax, fpath, **kwargs):
    """
    Store content of axes `ax` into a PNG image in filepath `fpath`
    so that the axes content can be plotted in a different axes
    """
    if not str(fpath).lower().endswith(".png"):
        raise NotImplementedError("Only PNG images are supported for now")

    img = create_image_from_ax(ax=ax)
    metadata = dict(xlim=ax.get_xlim, ylim=ax.get_ylim())

    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    metadata = dict(xmin=xlim[0], xmax=xlim[1], ymin=ylim[0], ymax=ylim[1])

    png_info = PngInfo()
    for (k, v) in metadata.items():
        png_info.add_text(k, str(v))

    img.save(fpath, pnginfo=png_info, **kwargs)

    
def load_and_plot_image(ax, fpath, zorder=1):
    """
    Load axes content from image stored in filepath `fpath` and plot
    into axes `ax`
    """
    img = Image.open(fpath)
    png_info = img.info
    xlim = (float(png_info["xmin"]), float(png_info["xmax"]))
    ylim = (float(png_info["ymin"]), float(png_info["ymax"]))
    ax.imshow(img, extent=[xlim[0], xlim[1], ylim[0], ylim[1]], zorder=zorder)