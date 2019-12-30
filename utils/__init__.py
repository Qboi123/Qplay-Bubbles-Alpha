import pyglet
from PIL import Image, ImageDraw, ImageTk
from typing import Tuple

UPDATE_INTERVAL = 60
TICKS_PER_SEC = 5


def version2name(version: Tuple[str, int, int, int]):  #releasetype: str, a: int, b: int, c: int=0):
    rt: str = version[0]
    rt = rt.title()
    a: int = version[1]
    b: int = version[2]
    c: int = version[3]
    return "%s %s.%s.%s" % (rt, a, b, c)


def draw_ellipse(image, bounds, width=1.0, outline='white', antialias=4):
    """Improved ellipse drawing function, based on PIL.ImageDraw."""

    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results.
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width / -1.5, '#ffffffff'), (width / 1.5, '#000000ff'):  # Note: Was first white, black
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)


def _new(mode, size, color):
    return Image.new(mode, size, color)


def _open(fp, mode: str = "r"):
    return Image.open(fp, mode)


def createbackground(size, color):
    return _new("RGBA", size, color)


def createcolorfield(size, color):
    return createbackground(size, color)


def createellipse(size, bg, fill=None, outline=None, width: int = 0):
    im = _new('RGBA', size, bg)
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.ellipse((0, 0, *size), fill, outline, width)


def createbubble_image(size, fp2png=None, *colors):
    im = _new('RGBA', size, '#ffffff00')
    # im.putalpha(0)
    if fp2png is not None:
        png = _open(fp2png)
    # draw = ImageDraw.Draw(im, "RGBA")
    i = 2

    # Drawung ellipses for Bubble.
    width = 1
    w = width
    for circ_color in colors:
        if circ_color != colors[0]:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        elif circ_color != colors[-1]:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        else:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        i += 1.5

    i += 10

    if fp2png is not None:
        png2 = _new('RGBA', size, (0, 0, 0, 0))
        # noinspection PyUnboundLocalVariable
        png = png.resize((size[0] - int(i), size[1] - int(i)))
        png2.paste(png, (int(i / 2), int(i / 2)))

        im = Image.alpha_composite(png2, im)

    return pillow2pyglet(im=im)


def pillow2pyglet(im: Image.Image):
    raw_image = im.tobytes()  # tostring is deprecated
    image = pyglet.image.ImageData(im.width, im.height, 'RGBA', raw_image, pitch=-im.width * 4)