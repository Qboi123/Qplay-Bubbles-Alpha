#!/bin/python3

"""
 ________                                        ______                       ______     __
|        \                                      /      \                     /      \   |  \
 \$$$$$$$$______    ______    ______   ______  |  $$$$$$\  ______   ______  |  $$$$$$\ _| $$_
   | $$  /      \  /      \  /      \ |      \ | $$   \$$ /      \ |      \ | $$_  \$$|   $$ \
   | $$ |  $$$$$$\|  $$$$$$\|  $$$$$$\ \$$$$$$\| $$      |  $$$$$$\ \$$$$$$\| $$ \     \$$$$$$
   | $$ | $$    $$| $$   \$$| $$   \$$/      $$| $$   __ | $$   \$$/      $$| $$$$      | $$ __
   | $$ | $$$$$$$$| $$      | $$     |  $$$$$$$| $$__/  \| $$     |  $$$$$$$| $$        | $$|  \
   | $$  \$$     \| $$      | $$      \$$    $$ \$$    $$| $$      \$$    $$| $$         \$$  $$
    \$$   \$$$$$$$ \$$       \$$       \$$$$$$$  \$$$$$$  \$$       \$$$$$$$ \$$          \$$$$


Copyright (C) 2013 Michael Fogleman
Copyright (C) 2018/2019 Stefano Peris <xenonlab.develop@gmail.com>

Github repository: <https://github.com/XenonLab-Studio/TerraCraft>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from random import Random

from pyglet.graphics import Batch
from typing import Dict, Tuple, Union, Type, List

import pyglet
import pickle
import json
import os

import globals as g

from time import gmtime, strftime

# from block import Block
from bubble import BubbleObject
from effects import Effect
from events import AutoSaveEvent
from sprites.player import Player
from map import Map


class SaveManager(object):
    def __init__(self):
        """SaveManager handles saving/loading of saves and options.

        An internal dictionary (self._data) holds persistent data
        such as options, inventory, etc. To make accessing this easier,
        the "magic methods" `__getitem__` and `__setitem__` are used to
        add dictionary-like behavior to `SaveManager`.
        """

        # Get the appropriate OS specific save path:
        self.save_path = os.path.join(pyglet.resource.get_settings_path('Qplay Bubbles'), "saves")
        print(f"Save Path: {self.save_path}")
        self.save_file = 'Save-{}.dat'
        self.config_file = 'config.json'
        self.save_name = "TEST"

        self._data = {'revision': 0,
                      'options': {},
                      'inventory': {}}

        AutoSaveEvent.bind(self.save_save)

    @staticmethod
    def timestamp_print(txt):
        print(("Save Manager: " + str(txt)))

    def has_save_game(self):
        """Returns True if the save path and file exist."""
        save_file = self.save_file.format(self.save_name)
        return os.path.exists(os.path.join(self.save_path, save_file))

    def load_save(self, scene):
        # Initialize loading save
        save_file = self.save_file.format(self.save_name)
        save_file_path = os.path.join(self.save_path, save_file)
        self.timestamp_print('Start loading')

        # try:
        if 1:
            # Load file
            with open(save_file_path, 'rb') as file:
                loaded_save: Dict[str, Union[List[Tuple], Tuple, Random]] = pickle.load(file)

            # print(f"Loaded Save Data: {loaded_save}")

            # Bubbles
            for name, size, speed, position in loaded_save["bubbles"]:
                scene.game_objects.append(
                    scene.map.create_bubble(position.x, position.y, g.NAME2BUBBLE[name], scene.batch, size, speed,
                                            scene))

            # Player
            lives = loaded_save["player"][0][0]
            score = loaded_save["player"][0][1]

            pos = loaded_save["player"][0][2]
            rot = loaded_save["player"][0][3]

            ghost_mode = loaded_save["player"][0][4]

            scene.player._Player__position = pos
            scene.player.rotation = rot
            scene.player.score = score
            scene.player.lives = lives
            scene.player.ghostMode = ghost_mode

            scene.player.refresh()

            # Effects
            for effect, time, strength in loaded_save["effects"]:
                effect: str
                scene.player.add_effect(g.NAME2EFFECT[effect](time, strength, scene))

            # Random
            scene.random.setstate(loaded_save["random"])

            # Completed
            self.timestamp_print('Loading completed.')
            return True
        # except Exception as e:  # If loading fails for ANY reason, return False
        #     self.timestamp_print('Loading failed! Generating a new map.')
        #     self.timestamp_print(e.__class__.__name__ + ": " + e.__str__())
        #     return False

    def save_save(self, event: AutoSaveEvent):
        save_file = self.save_file.format(self.save_name)
        save_file_path = os.path.join(self.save_path, save_file)
        self.timestamp_print('Start saving')

        # If the save directory doesn't exist, create it
        if not os.path.exists(self.save_path):
            self.timestamp_print(
                'Creating directory: {}'.format(self.save_path))
            os.makedirs(self.save_path)

        # Efficiently save the save to a binary file
        with open(save_file_path, 'wb+') as file:
            # noinspection PyProtectedMember,SpellCheckingInspection
            pickle.dump({"player": [(event.player.lives, event.player.score, event.player._Player__position,
                                     event.player.rotation, event.player.ghostMode)],
                         "bubbles": [(bubbleobject.name,
                                      bubbleobject.size,
                                      bubbleobject.speed,
                                      bubbleobject.position
                                      ) for bubbleobject in event.map.bubbles],
                         "random": event.scene.random.getstate(),
                         "effects": [(appliedeffect.baseEffectClass.get_unlocalized_name(),
                                      appliedeffect._get_time_remaining(),
                                      appliedeffect.strengthMultiply
                                      ) for appliedeffect in event.player.activeEffects]
                         }, file)

        self.timestamp_print('Saving completed')

    def __getitem__(self, item):
        return self._data.get(item)

    def __setitem__(self, key, item):
        self._data[key] = item

    def get(self, item, default):
        return self._data.get(item, default)

    def keys(self):
        return self._data.keys()
