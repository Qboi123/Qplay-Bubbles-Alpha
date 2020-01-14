import json
import os
import traceback

import pyglet as _pyglet
import sys
from typing import Dict as _Dict

import exceptions
from utils.image.pyglet import center_image


class JsonFile(object):
    def __init__(self, filepath, readnow=True):
        self.decoder = json.JSONDecoder()
        self.encoder = json.JSONEncoder()
        self.fp = filepath

        if os.path.exists(filepath) and readnow:
            self.read()

    def write(self, obj):
        with open(self.fp, "w+") as file:
            file.write(self.encoder.encode(obj))

    def read(self):
        with open(self.fp, "r") as file:
            self.decoder.decode(file.read())


class Resources(object):
    __resources = {}
    loaded = False
    _status = ""

    # status = property()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        print(value)
        # self.infoLabel.text = value
        #
        # glClearColor(0, 0, 0, 0)
        # self.infoLabel.text = self.status
        # self.batch.draw()
        # self.infoLabel.draw()

    def __init__(self):
        _pyglet.resource.path = ['./assets']
        # self.label = label
        # self.scene = scene
        # self.scene.on_draw()
        self.status = "Initializing Resources"

    @classmethod
    def reindex(cls):
        _pyglet.resource.reindex()

    def get_bubble_images(self):
        """Generate and get bubble images

        :return:
        """
        self.status = "Loading bubble resources"

        # Initialize bubble dictionaries
        bub = dict()
        # bub["normal_bubble"] = dict()
        # bub["speedy_bubble"] = dict()
        # bub["triple_bubble"] = dict()
        # bub["double_bubble"] = dict()
        # bub["kill_bubble"] = dict()
        # bub["speedup_bubble"] = dict()
        # bub["slowdown_bubble"] = dict()
        # bub["ultimate_bubble"] = dict()
        # bub["life_bubble"] = dict()
        # bub["teleporter_bubble"] = dict()
        # bub["slow_motion_bubble"] = dict()
        # bub["double_state_bubble"] = dict()
        # bub["protection_bubble"] = dict()
        # bub["shot_speed_status_bubble"] = dict()
        # bub["hyper_mode_bubble"] = dict()
        # bub["game_pause_bubble"] = dict()
        # bub["confusion_bubble"] = dict()
        # bub["paralis_bubble"] = dict()
        # bub["stone_bubble"] = dict()
        # bub["ghost_mode_bubble"] = dict()
        # bub["key_bubble"] = dict()
        # bub["diamond_bubble"] = dict()
        # bub["present_bubble"] = dict()
        # bub["coin_bubble"] = dict()
        # bub["ultra_mode_bubble"] = dict()

        # Import utils, for creating bubble in dynamic resolution
        import utils

        # Initialize minimum and maximum size of the bubbles
        _min = 21
        _max = 80

        data = {}
        files = os.listdir("assets/models/bubbles")
        # print(files)

        self.status = "Loading bubblen model files"
        # Scanning files to index
        for file in files:
            # print(os.path.splitext(file)[-1])
            if os.path.splitext(file)[-1] == ".json":
                with open(os.path.join("assets/models/bubbles", file)) as fd:
                    bubble_id = ''.join(os.path.splitext(file)[0:-1])
                    data[bubble_id] = json.decoder.JSONDecoder().decode(fd.read())
                    bub[bubble_id] = dict()

        model_types = ["bubble/dynamic", "bubble/static"]

        self.status = "Checking for model type errors"
        for bubble_id, bubble_data in data.items():
            if bubble_data["type"] in model_types:
                pass
            else:
                exceptions.ModelWarning("Model type '%s' is unknown for file '%s'." % (
                    bubble_data["type"], os.path.join("assets/models/bubbles", bubble_id + ".json").replace("\\", "/")))

        # Adding the different resolutions to the bubbles

        for bubble_id, bubble_data in data.items():
            self.status = f"Loading bubble '{bubble_id}'"

            if bubble_data["type"] == model_types[0]:
                for i in range(_min, _max + 1):
                    bub[bubble_id][i] = utils.createbubble_image(
                        (i, i), bubble_data["inner"] if "inner" in bubble_data.keys() else None, *bubble_data["colors"]
                    )
                    center_image(bub[bubble_id][i])
            elif bubble_data["type"] == model_types[1]:
                image = _pyglet.resource.image(os.path.join("textures/bubbles", bubble_data["texture"] +
                                                            ".png").replace("\\", "/"))
                bub[bubble_id][image.width] = image

        # print("Bubble dictionary: %s" % bub)
        # bub["normal_bubble"][i] = utils.createbubble_image((i, i), None, "white")
        # bub["speedy_bubble"][i] = utils.createbubble_image((i, i), None, "white")
        # bub["double_bubble"][i] = utils.createbubble_image((i, i), None, "gold")
        # bub["triple_bubble"][i] = utils.createbubble_image((i, i), None, "blue", "#007fff", "#00ffff", "white")
        # bub["slowdown_bubble"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#a7a7a7", "#7f7f7f", "#373737")
        # bub["speedup_bubble"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#7fff7f", "#00ff00", "#007f00")
        # bub["life_bubble"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#00ff00", "#00000000", "#00ff00")
        # bub["ultimate_bubble"][i] = utils.createbubble_image((i, i), None, "gold", "gold", "orange", "gold")
        # bub["kill_bubble"][i] = utils.createbubble_image((i, i), None, "#7f0000", "#7f007f", "#7f0000", )
        # bub["teleporter_bubble"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#ff1020", "#373737")
        # bub["slow_motion_bubble"][i] = utils.createbubble_image((i, i), None, "#ffffffff", "#00000000", "#000000ff")
        # bub["double_state_bubble"][i] = utils.createbubble_image((i, i), None, "gold", "#00000000", "gold", "gold")
        # bub["protection_bubble"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#3fff3f", "#7fff7f", "#9fff9f")
        # bub["shot_speed_status_bubble"][i] = utils.createbubble_image((i, i), None, "#ff7f00", "#ff7f00", "gold")
        # bub["hyper_mode_bubble"][i] = utils.createbubble_image((i, i), None, "black", "black", "white", "black")
        # bub["game_pause_bubble"][i] = utils.createbubble_image((i, i), None, "red", "orange", "yellow", "white")
        # bub["confusion_bubble"][i] = utils.createbubble_image((i, i), None, "black", "purple", "magenta", "white")
        # bub["paralis_bubble"][i] = utils.createbubble_image((i, i), None, "#ffff00", "#ffff00", "#ffff7f", "#ffffff")
        # bub["stone_bubble"][i] = utils.createbubble_image((i, i), None, "black", "orange", "yellow")
        # bub["ghost_mode_bubble"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#7f7f7f", "#373737")
        #
        # center_image(bub["normal_bubble"][i])
        # center_image(bub["speedy_bubble"][i])
        # center_image(bub["double_bubble"][i])
        # center_image(bub["triple_bubble"][i])
        # center_image(bub["slowdown_bubble"][i])
        # center_image(bub["speedup_bubble"][i])
        # center_image(bub["life_bubble"][i])
        # center_image(bub["ultimate_bubble"][i])
        # center_image(bub["kill_bubble"][i])
        # center_image(bub["teleporter_bubble"][i])
        # center_image(bub["slow_motion_bubble"][i])
        # center_image(bub["double_state_bubble"][i])
        # center_image(bub["protection_bubble"][i])
        # center_image(bub["shot_speed_status_bubble"][i])
        # center_image(bub["hyper_mode_bubble"][i])
        # center_image(bub["game_pause_bubble"][i])
        # center_image(bub["confusion_bubble"][i])
        # center_image(bub["paralis_bubble"][i])
        # center_image(bub["stone_bubble"][i])
        # center_image(bub["ghost_mode_bubble"][i])

        self.status = "Loading static-size bubble resource"

        # # Adding the static-resolution-bubbles.
        # bub["key_bubble"][60] = _pyglet.resource.image(name="bubbles/key.png")
        # bub["diamond_bubble"][36] = _pyglet.resource.image(name="bubbles/diamond.png")
        # bub["present_bubble"][40] = _pyglet.resource.image(name="bubbles/present.png")
        # bub["coin_bubble"][42] = _pyglet.resource.image(name="bubbles/coin.png")
        # bub["ultra_mode_bubble"][48] = _pyglet.resource.image(name="bubbles/special_mode.png")
        #
        # center_image(bub["key_bubble"][60])
        # center_image(bub["diamond_bubble"][36])
        # center_image(bub["present_bubble"][40])
        # center_image(bub["coin_bubble"][42])
        # center_image(bub["ultra_mode_bubble"][48])
        return bub

    def load(self):
        Resources.no_image = _pyglet.resource.image("no_image.png")
        Resources.no_image_circle = _pyglet.resource.image("no_image_circle.png")
        self.status = "Indexing resources"

        # Index assets, and generate bubble images for all sizes.
        # NOTE: The bubbles have dynamic size!
        _pyglet.resource.reindex()

        # Bubble images
        self.__resources["bubbles"]: _Dict[str, _Dict[int, _pyglet.image.AbstractImage]] = self.get_bubble_images()

        # Player image
        self.status = "Loading player resource"
        self.__resources["player"]: _pyglet.image.AbstractImage = _pyglet.resource.image(name="sprites/player.png")
        # print(player.__dict__)
        # print(player.__repr__())
        center_image(self.__resources["player"])
        self.loaded = True

    # noinspection PyUnreachableCode
    @classmethod
    def get_resource(cls, *resource_recursion):
        try:
            if len(resource_recursion) > 1:
                return cls._get_resource(cls.__resources[resource_recursion[0]], *resource_recursion[1:])
            elif len(resource_recursion) == 1:
                return cls.__resources[resource_recursion[0]]
            else:
                return cls.__resources
        except KeyError:
            resource_text = resource_recursion[0]
            if len(resource_recursion) > 1:
                for i in resource_recursion[1:]:
                    resource_text += "::%s" % i
            a = exceptions.TextureWarning("Resource %s is not found" % resource_text)
            # a.__traceback__
            if resource_recursion[0] == "bubbles" or resource_recursion[0] == "player":
                if len(resource_recursion) == 3:
                    return cls.no_image_circle
                return {j: cls.no_image_circle for j in range(21, 81)}
            return cls.no_image

    @classmethod
    def _get_resource(cls, dict_, *resource_recursion):
        if len(resource_recursion) > 1:
            return cls._get_resource(dict_[resource_recursion[0]], *resource_recursion[1:])
        else:
            return dict_[resource_recursion[0]]
