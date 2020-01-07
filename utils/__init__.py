import random

import sys

import io
import math
import os
# from os import tmpfile
import tempfile

import PIL
import pyglet
from PIL import Image, ImageDraw, ImageTk, PngImagePlugin, _imaging
from typing import Tuple

from pyglet.image import Texture
from pyglet.image.codecs.bmp import BMPImageDecoder
from pyglet.image.codecs.pil import PILImageDecoder
from pyglet.image.codecs.png import PNGImageDecoder
from io import BytesIO

from perlin import SimplexNoise

UPDATE_INTERVAL = 60
TICKS_PER_SEC = 5

PLAYER_SPEED = 2

HORIZONTAL = "horizontal"
VERTICAL = "vertical"
EAST = "east"
WEST = "west"
NORTH = "north"
SOUTH = "south"
TRUE = True
FALSE = False


def randint_lookup(value_in, min_, max_):
    value_in2 = (value_in / 2) + 0.5
    sys.stderr.write(str(value_in2) + " ")
    # value_in2 = value_in
    return int(round(value_in2 * (max_ - min_) + min_))


def version2name(version: Tuple[str, int, int, int]):  # releasetype: str, a: int, b: int, c: int=0):
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
    raw_image = BytesIO()  # tostring is deprecated
    if not os.path.exists("assets/temp"):
        os.makedirs("assets/temp")

    from PIL import _imaging

    # _imaging.

    file = tempfile.TemporaryFile("w+", suffix=".png", dir=os.path.abspath("assets/temp"), delete=False)
    file.close()

    pyglet.resource.reindex()
    im.save(file.name)
    # file.name

    # image: pyglet.image.ImageData = pyglet.image.ImageData(im.width, im.height, 'RGBA', raw_image, pitch=-im.width * 4)
    image = pyglet.resource.image(os.path.join("temp", os.path.split(file.name)[-1]).replace("\\", "/"))
    # pyglet.image.TextureRegion()
    os.remove(file.name)
    return image


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


# fast math algorithms
class FastRandom(object):
    def __init__(self, seed):
        self.seed = seed

    def randint(self):
        self.seed = (214013 * self.seed + 2531011)
        return (self.seed >> 16) & 0x7FFF


# random.randint()


class Seed(object):
    def __init__(self, seed):
        self._seed = seed

    def randint(self, x, y):
        h: int = self._seed + x * 374761393 + y * 668265263
        h = (h**(h >> 13))*1274126177
        return h**(h >> 16)


# Factory class utilizing perlin.SimplexNoise
class SimplexNoiseGen(object):
    def __init__(self, seed, octaves=0, zoom_level=1):  # octaves = 6,
        perm = list(range(255))
        random.Random(seed).shuffle(perm)
        self.noise = SimplexNoise(permutation_table=perm).noise2

        self.PERSISTENCE = 2 # 2.1379201 # AKA lacunarity
        self.H = 0.836281
        self.OCTAVES = octaves       # Higher linearly increases calc time; increases apparent 'randomness'
        self.weights = [self.PERSISTENCE ** (-self.H * n) for n in range(self.OCTAVES)]

        self.zoom_level = zoom_level # Smaller will create gentler, softer transitions. Larger is more mountainy

    def fBm(self,x,z):
        x *= self.zoom_level
        z *= self.zoom_level
        y = 0
        for weight in self.weights:
            y += self.noise(x, z) * weight

            x *= self.PERSISTENCE
            z *= self.PERSISTENCE
        return y


