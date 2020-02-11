import math
import os
import random
# from os import tmpfile
import tempfile

import pathlib
import pyglet
import sys
from PIL import Image, ImageDraw
from io import BytesIO

from perlin import SimplexNoise
from utils.advBuiltins import AdvFloat

UPDATE_INTERVAL = 1 / 120
AUTO_SAVE_INTERVAL = 60
TICKS_PER_SEC = 1 / 5

PLAYER_SPEED = 2

MIN_BUBBLE_SIZE = 21  # 21
MAX_BUBBLE_SIZE = 80  # 80
MAXIMAL_BUBBLES = 125

ROTATION_SPEED = 5
MOTION_SPEED = 10

HORIZONTAL = "horizontal"
VERTICAL = "vertical"
EAST = "east"
WEST = "west"
NORTH = "north"
SOUTH = "south"
TRUE = True
FALSE = False


import io
from typing import Union, List, Tuple, Optional, Dict


def split_path(path: str):
    return tuple(path.replace("\\", "/").split("/"))


class EditableClass(object):
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__[item]


class Font(object):
    def __init__(self, family, size, bold=False, italic=False, color=(255, 255, 255, 255)):
        self.family = family
        self.size = size

        self.bold = bold
        self.italic = italic

        self.color = color

    def get_label(self, text, x=0, y=0, width=None, height=None, anchor_x='left', anchor_y='baseline', align='left',
                  multiline=False, dpi=None, batch=None, group=None):
        return pyglet.text.Label(text=text, font_name=self.family, font_size=self.size,
                                 bold=self.bold, italic=self.italic, color=self.color,
                                 x=x, y=y, height=height, width=width,
                                 anchor_x=anchor_x, anchor_y=anchor_y, align=align, multiline=multiline, dpi=dpi,
                                 batch=batch, group=group)


class Text(object):
    def __init__(self, text, font: Font, align='left', multiline=False, dpi=None):
        self.font = font
        self.text = text

        self.align = align
        self.multiline = multiline
        self.dpi = dpi

    def get_label(self, x=0, y=0, width=None, height=None, anchor_x='left', anchor_y='baseline',
                  batch=None, group=None):
        return self.font.get_label(self.text, x=x, y=y, width=width, height=height,
                                   anchor_x=anchor_x, anchor_y=anchor_y, align=self.align,
                                   multiline=self.multiline, dpi=self.dpi, batch=batch, group=group)


class Directory(object):
    def __init__(self, path):
        import os
        self.os = os

        self.path = path
        self.dirName = os.path.split(path)[-1]

        self.absPath: str = os.path.abspath(path)
        try:
            self.relPath: str = os.path.relpath(path)
        except ValueError:
            self.relPath: Optional[str] = None

    def delete(self, ignore_errors: bool = False):
        import shutil
        shutil.rmtree(self.path, ignore_errors)

    def copy(self, to):
        import shutil
        shutil.copy(self.path, to)

    def move(self, to):
        import shutil
        shutil.move(self.path, to)

    def rename(self, name, change_path=True):
        if not self.os.path.isabs(name):
            name = self.os.path.abspath(name)
        else:
            if not self.os.path.abspath(self.os.path.join(*self.os.path.split(name)[:-1])) == self.upper().path:
                raise IOError("Can't rename file to another directory")
        self.os.rename(self.os.path.abspath(self.path), name)

        if change_path:
            if self.os.path.isabs(self.path):
                self.path = self.os.path.abspath(name)
            else:
                self.path = self.os.path.relpath(name)

    def listdir(self):
        return self.index()

    def index(self):
        list_ = []
        list_.extend(self.listdirs())
        list_.extend(self.listfiles())
        return list_

    def listdirs(self):
        list_: List[Directory] = []
        for item in self.os.listdir(self.path):
            if self.os.path.isdir(self.os.path.join(self.path, item)):
                list_.append(Directory(self.os.path.join(self.path, item)))
        return list_

    def listfiles(self):
        list_: List[File] = []
        for item in self.os.listdir(self.path):
            if self.os.path.isfile(self.os.path.join(self.path, item)):
                list_.append(File(self.os.path.join(self.path, item)))
        return list_

    @staticmethod
    def _split_path(path: str):
        return tuple(path.replace("\\", "/").split("/"))

    def upper(self):
        s_path = self._split_path(self.path)
        print(s_path)
        if len(s_path) >= 2:
            up = self.os.path.split(self.path)[0]
            print(up)
            return Directory(up)
        return Directory(self.path)


class File(object):
    def __init__(self, path):
        import os
        import mimetypes

        self.directory = Directory(os.path.abspath(os.path.join(*os.path.split(path)[:-1])))
        self.path: str = path
        self.fileName = os.path.split(path)[-1]
        self.absPath: str = os.path.abspath(path)
        try:
            self.relPath: str = os.path.relpath(path)
        except ValueError:
            self.relPath: Optional[str] = None
        self.os = os

        self._fd: Optional[io.IOBase] = None
        self._fileOpen = False

        try:
            self.mimeType = mimetypes.read_mime_types(self.path)
        except UnicodeDecodeError:
            pass

    def get_json(self):
        return JsonFile(self.path)

    def start_file(self):
        self.os.startfile(self.path)

    def open(self, mode="w"):
        file_was_open = self._fileOpen
        if not self._fileOpen:
            self._fd = open(self.path, mode)
            self._fileOpen = True
        else:
            pass
        return file_was_open

    def close(self):
        self._fd.close()
        self._fileOpen = False

    def exists(self):
        return self.os.path.exists(self.path)

    def read(self, size=None):
        file_was_open = self._fileOpen
        if not self._fileOpen:
            self.open(mode="r")

        self._fd.read(size)

        if not file_was_open:
            self.close()

    def write(self, data):
        if type(data) == str:
            data: str
            self._fd.write(data.encode())
        elif type(data) in [bytes, bytearray]:
            self._fd.write(data)
        elif type(data) in [int, float, bool]:
            self._fd.write(str(data).encode())
        elif type(data) in [dict, list]:
            import json
            self._fd.write((json.JSONEncoder().encode(data)).encode())
        elif type(data) in [tuple]:
            import json
            self._fd.write((json.JSONEncoder().encode(list(data))).encode())
        else:
            self._fd.write(repr(data))

    def subprocess(self, *args):
        import subprocess
        subprocess.call([self.absPath, *args], cwd=self.directory.absPath)

    def execute(self, *args):
        self.os.system(" ".join([*args]))

    def write_lines(self, data: Union[List, Tuple]):
        for obj in data:
            self.write(obj)

    def write_yaml(self, data):
        import yaml

        file_was_open = self._fileOpen
        if not self._fileOpen:
            self.open(mode="r")

        yaml.dump(data, self._fd)

        if file_was_open:
            self.close()

    def write_at(self, offset: int, data):
        file_was_open = self.open(mode="r+b")
        self._fd.seek(offset)

        if type(data) == str:
            data: str
            self._fd.write(data.encode())
        elif type(data) in [bytes, bytearray]:
            self._fd.write(data)
        elif type(data) in [int, float, bool]:
            self._fd.write(str(data).encode())

        if not file_was_open:
            self.close()

    def read_at(self, offset: int, size: int = -1) -> bytes:
        file_was_open = self.open(mode="r+b")
        self._fd.seek(offset)

        data = self._fd.read(size)
        if not file_was_open:
            self.close()

        return data

    def create(self, size=0):
        file_was_open = self.open("w+")

        if size == 0:
            self.close()
            return
        self._fd.seek(size - 1)
        self._fd.write(chr(0))

        if not file_was_open:
            self.close()

    def remove(self):
        self.os.remove(self.path)

    def delete(self):
        self.remove()

    def rename(self, name, change_path=True):
        if not self.os.path.isabs(name):
            name = self.os.path.abspath(name)
        else:
            if not self.os.path.abspath(self.os.path.join(*self.os.path.split(name)[:-1])) == self.directory.path:
                raise IOError("Can't rename file to another directory")
        self.os.rename(self.os.path.abspath(self.path), name)

        if change_path:
            if self.os.path.isabs(self.path):
                self.path = self.os.path.abspath(name)
            else:
                self.path = self.os.path.relpath(name)

    def get_size(self):
        return self.os.path.getsize(self.path)

    def get_ctime(self):
        return self.os.path.getctime(self.path)

    def get_atime(self):
        return self.os.path.getatime(self.path)

    def get_mtime(self):
        return self.os.path.getmtime(self.path)

    def get_dev(self):
        return os.lstat(self.path).st_dev

    def get_uid(self):
        return os.lstat(self.path).st_uid

    def get_gid(self):
        return os.lstat(self.path).st_gid

    def get_mode(self):
        return os.lstat(self.path).st_mode

    def get_owner(self):
        return pathlib.Path(self.path).owner()


class JsonFile(File):
    def __init__(self, path):
        super().__init__(path)

        del self.subprocess
        del self.execute

        import json
        self._mJson = json

        self.json: Optional[Union[List, Dict]] = None
        self.json = self._mJson.JSONDecoder().decode(self.read())

    def read_json(self):
        self.json = self._mJson.JSONDecoder().decode(self.read())

        return self.json

    def write_json(self):
        self.write(self._mJson.JSONEncoder().encode(self.json))

        return self.json


class DataFile(File):
    def __init__(self, path):
        super().__init__(path)

        del self.subprocess
        del self.execute

        import pickle
        self._pickle = pickle

        self.data: Optional[object] = None
        self.read_data()

    def read_data(self):
        file_was_open = self._fileOpen
        if not file_was_open:
            self.open("rb")

        self.data = self._pickle.load(self._fd)

        if not file_was_open:
            self.close()

    def write_data(self, o: object):
        file_was_open = self._fileOpen
        if not file_was_open:
            self.open("wb")

        self.data = self._pickle.dump(o, self._fd)

        if not file_was_open:
            self.close()


def randint_lookup(value_in, min_, max_):
    # value_in2 = (value_in / 2) + 0.5
    sys.stderr.write(str(value_in) + " ")
    value_in2 = value_in
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


def createbubble_image(size, inner=None, *colors):
    im = _new('RGBA', size, '#ffffff00')
    # im.putalpha(0)
    if inner is not None:
        inner_im = _open(inner)
    # draw = ImageDraw.Draw(im, "RGBA")
    i = 2

    # Drawung ellipses for Bubble.
    width = 0.75
    ex_w = width / 2
    w = width
    if len(colors) == 1:
        draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[0], width=w, antialias=4)
        i += width+ex_w
        # print("Single circle")
    else:
        for index in range(0, len(colors)):

            if len(colors)-1 > index > 0:  # .OOO.
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w+ex_w, antialias=4)
            elif index == len(colors)-1:  # ....O
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w, antialias=4)
            else:  # First:  O....
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w+ex_w, antialias=4)
            i += width+(ex_w*2)

    i += 10

    if inner is not None:
        png2 = _new('RGBA', size, (0, 0, 0, 0))
        # noinspection PyUnboundLocalVariable
        if size[0] - int(i) < png2.width:
            inner_im = inner_im.resize((size[0] - int(i), size[1] - int(i)))
        png2.paste(inner_im, (int(i / 2), int(i / 2)))
        im = Image.alpha_composite(png2, im)

    return pillow2pyglet(im=im)


def pillow2pyglet(im: Image.Image):
    raw_image = BytesIO()  # tostring is deprecated
    if not os.path.exists("assets/temp"):
        os.makedirs("assets/temp")

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
    return AdvFloat((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2).sqrt()


# fast math algorithms
class FastRandom(object):
    def __init__(self, seed):
        self.seed = seed

    def randint(self):
        self.seed = (214013 * self.seed + 2531011)
        return (self.seed >> 16) & 0x7FFF


# rand.randint()


class Seed(object):
    def __init__(self, seed):
        self._seed = seed

    def randint(self, x, y):
        h: int = self._seed + x * 374761393 + y * 668265263
        h = (h**(h >> 16))*1274126177
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


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2
