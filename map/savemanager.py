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
import os
import pickle
from random import Random
from typing import Dict, Tuple, Union, List, Optional
from typinglib import Integer, Float

import pyglet

import globals as g
# from block import Block
from events import AutoSaveEvent
from nzt import NZTFile
from utils.classes import Position2D


class SaveManager(object):
    def __init__(self):
        """SaveManager handles saving/loading of saves and options.

        An internal dictionary (self._data) holds persistent data
        such as options, inventory, etc. To make accessing this easier,
        the "magic methods" `__getitem__` and `__setitem__` are used to
        add dictionary-like behavior to `SaveManager`.
        """

        # Get the appropriate OS specific save path:
        self.savePath = os.path.join(pyglet.resource.get_settings_path('Qplay Bubbles'), "saves")
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        print(f"Save Path: {self.savePath}")
        self.saveFileOLD = 'Save-{}.dat'
        self.saveFile = 'Save-{}.nzt'
        self.configFile = 'config.json'
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
        save_file = self.saveFileOLD.format(self.save_name)
        return os.path.exists(os.path.join(self.savePath, save_file))

    # noinspection PyUnresolvedReferences
    def load_save(self, scene):
        # Initialize loading save
        save_file_old = self.saveFileOLD.format(self.save_name)
        save_file_old_path = os.path.join(self.savePath, save_file_old)

        save_file = self.saveFile.format(self.save_name)
        save_file_path = os.path.join(self.savePath, save_file)

        if (not os.path.exists(save_file_old_path)) and (not os.path.exists((save_file_path))):
            self.timestamp_print("Can't load, save not exists")
            return False

        self.timestamp_print('Start loading')

        nzt_data: Optional[Dict] = None

        nzt_data: Optional[Dict] = {
            "Player": {
                "Effects": [
                    {
                        "id": str(),
                        "time": float(),
                        "strength": float()
                    }
                ],
                "Abilities": {
                    "ghostMode": bool()
                },
                "rot": int(),
                "pos": [
                    float(),
                    float()
                ],
                "score": int(),
                "lives": int()
            },
            "Map": {
                "Bubbles": [
                    {
                        "id": str(),
                        "size": int(),
                        "speed": float(),
                        "pos": [
                            float(),
                            float()
                        ]
                    }
                ]
            }
        }

        loaded_save: Optional[Dict[str, Union[List[Tuple], Tuple, Random]]] = None

        # try:
        if 1:
            # Load file
            if os.path.exists(save_file_path):
                nzt_file = NZTFile(save_file_path, "r")
                self.timestamp_print("Loading NZT-data")
                nzt_data = nzt_file.load()
                # print(nzt_data)
                nzt_file.close()
            else:
                with open(save_file_old_path, 'rb') as file:
                    # noinspection PyBroadException
                    try:
                        loaded_save = pickle.load(file)
                    except Exception as e:  # If loading fails for ANY reason, return False
                        self.timestamp_print('Loading failed! Generating a new map.')
                        self.timestamp_print(e.__class__.__name__ + ": " + e.__str__())
                        return False

        if loaded_save:
            nzt_data = {
                "Player": {
                    "Effects": [
                        *({
                            "id": id_,
                            "time": time,
                            "strength": strength
                        } for id_, time, strength in loaded_save["effects"])
                    ],
                    "Abilities": {
                        "ghostMode": int(loaded_save["player"][0][4])
                    },
                    "rot": loaded_save["player"][0][3],
                    "pos": [
                        loaded_save["player"][0][2].x,
                        loaded_save["player"][0][2].y
                    ],
                    "score": loaded_save["player"][0][1],
                    "lives": loaded_save["player"][0][0]
                },
                "Map": {
                    "Bubbles": [
                        *({
                            "id": id_,
                            "size": size,
                            "speed": speed,
                            "pos": [
                                pos.x,
                                pos.y
                            ]
                        } for id_, size, speed, pos in loaded_save["bubbles"])
                    ]
                },
                "random": loaded_save["random"],
                "version": "0.2.0"
            }

            if "version" in nzt_data.keys():
                if nzt_data["version"] == "0.1.0":
                    for bubble in nzt_data["Map"]["Bubbles"]:
                        bubble["Multipliers"] = {"attack": g.NAME2BUBBLE[bubble["id"]].attackMultiplier,
                                                 "defence": g.NAME2BUBBLE[bubble["id"]].defenceMultiplier}
                        bubble["health"] = g.NAME2BUBBLE[bubble["id"]].health
                        bubble["maxHealth"] = g.NAME2BUBBLE[bubble["id"]].maxHealth
                    nzt_data["Player"]["health"] = 50 * loaded_save["player"][0][0] / 10 if \
                        loaded_save["player"][0][0] <= 10 else 50
                    nzt_data["Player"]["maxHealth"] = 50
            else:
                for bubble in nzt_data["Map"]["Bubbles"]:
                    bubble["Multipliers"] = {"attack": g.NAME2BUBBLE[bubble["id"]].attackMultiplier,
                                             "defence": g.NAME2BUBBLE[bubble["id"]].defenceMultiplier}
                    bubble["health"] = g.NAME2BUBBLE[bubble["id"]].health
                    bubble["maxHealth"] = g.NAME2BUBBLE[bubble["id"]].maxHealth
                nzt_data["Player"]["health"] = 50 * loaded_save["player"][0][0] / 10 if \
                    loaded_save["player"][0][0] <= 10 else 50
                nzt_data["Player"]["maxHealth"] = 50

            save_file2 = 'Save-{}.nzt'.format(self.save_name)
            save_file_path2 = os.path.join(self.savePath, save_file2)

            nzt_file = NZTFile(save_file_path2, "w")
            nzt_file.data = nzt_data
            nzt_file.save()

            # Bubbles
            for name, size, speed, position in loaded_save["bubbles"]:
                scene.game_objects.append(
                    scene.map.create_bubble(position.x, position.y, g.NAME2BUBBLE[name], scene.batch, size, speed,
                                            scene))

            # Player
            health = loaded_save["player"][0][0]
            score = loaded_save["player"][0][1]

            pos = loaded_save["player"][0][2]
            rot = loaded_save["player"][0][3]

            ghost_mode = loaded_save["player"][0][4]

            scene.player._Player__position = pos
            scene.player.rotation = rot
            scene.player.score = score
            scene.player.health = Integer(health)
            scene.player.ghostMode = ghost_mode

            scene.player.refresh()

            # Effects
            for effect, time, strength in loaded_save["effects"]:
                effect: str
                scene.player.add_effect(g.NAME2EFFECT[effect](time, strength, scene))

            # Random
            scene.random.setstate(loaded_save["rand"])

            # Completed
            self.timestamp_print('Loading completed.')
            return True

        else:
            # print("NZTData:", nzt_data)
            # Bubbles

            if "version" in nzt_data.keys():
                if nzt_data["version"] == "0.1.0":
                    for bubble in nzt_data["Map"]["Bubbles"]:
                        bubble["Multipliers"] = {"attack": g.NAME2BUBBLE[bubble["id"]].attackMultiplier,
                                                 "defence": g.NAME2BUBBLE[bubble["id"]].defenceMultiplier}
                        bubble["health"] = g.NAME2BUBBLE[bubble["id"]].health
                        bubble["maxHealth"] = g.NAME2BUBBLE[bubble["id"]].maxHealth
                    nzt_data["Player"]["health"] = 50 * nzt_data["Player"]["lives"] / 10 if \
                        nzt_data["Player"]["lives"] <= 10 else 50
                    nzt_data["Player"]["maxHealth"] = 50
            else:
                for bubble in nzt_data["Map"]["Bubbles"]:
                    bubble["Multipliers"] = {"attack": g.NAME2BUBBLE[bubble["id"]].attackMultiplier,
                                             "defence": g.NAME2BUBBLE[bubble["id"]].defenceMultiplier}
                    bubble["health"] = g.NAME2BUBBLE[bubble["id"]].health
                    bubble["maxHealth"] = g.NAME2BUBBLE[bubble["id"]].maxHealth
                nzt_data["Player"]["health"] = 50 * nzt_data["Player"]["lives"] / 10 if \
                    nzt_data["Player"]["lives"] <= 10 else 50.0
                nzt_data["Player"]["maxHealth"] = 50.0
            nzt_data["version"] = "0.2.0"

            for bubble in nzt_data["Map"]["Bubbles"]:
                scene.game_objects.append(
                    scene.map.create_bubble(bubble["pos"][0], bubble["pos"][1], g.NAME2BUBBLE[bubble["id"]], scene.batch, bubble["size"], bubble["speed"],
                                            scene))

            # Player
            health = nzt_data["Player"]["health"]
            score = nzt_data["Player"]["score"]

            pos = Position2D(nzt_data["Player"]["pos"])
            rot = nzt_data["Player"]["rot"]

            ghost_mode = nzt_data["Player"]["Abilities"]["ghostMode"]

            scene.player._Player__position = pos
            scene.player.rotation = rot
            scene.player.score = score
            scene.player.health = Float(health)
            scene.player.ghostMode = ghost_mode

            scene.player.refresh()

            # Effects
            for effect in nzt_data["Player"]["Effects"]:
                effect: Dict
                scene.player.add_effect(g.NAME2EFFECT[effect["id"]](effect["time"], effect["strength"], scene))

            # Random
            scene.random.setstate(nzt_data["random"])

            # Completed
            self.timestamp_print('Loading completed.')
            return True

    def delete_save(self):
        save_file = self.saveFile.format(self.save_name)
        save_file_path = os.path.join(self.savePath, save_file)

        if os.path.exists(save_file_path):
            os.remove(save_file_path)

    def save_save(self, event: AutoSaveEvent):
        # saveFileOLD = self.saveFileOLD.format(self.save_name)
        # save_file_path = os.path.join(self.savePath, saveFileOLD)
        self.timestamp_print('Start saving')

        nzt_data = {
            "Player": {
                "Effects": [
                    *({
                        "id": appliedeffect.baseEffectClass.get_unlocalized_name(),
                        "time": appliedeffect.timeRemaining,
                        "strength": appliedeffect.strengthMultiply
                    } for appliedeffect in event.player.activeEffects)
                ],
                "Abilities": {
                    "ghostMode": event.player.ghostMode
                },
                "rot": event.player.rotation,
                "pos": [
                    event.player.position.x,
                    event.player.position.y
                ],
                "score": event.player.score,
                "health": Float(event.player.get_max_health()),
                "maxHealth": Float(event.player.get_max_health())
            },
            "Map": {
                "Bubbles": [
                    *({
                        "id": bubbleobject.baseBubbleClass.get_unlocalized_name(),
                        "size": bubbleobject.size,
                        "speed": bubbleobject.speed,
                        "pos": [
                            bubbleobject.position.x,
                            bubbleobject.position.y
                        ],
                        "Multiplier": {
                            "attack": bubbleobject.attackMultiplier,
                            "defence": bubbleobject.defenceMultiplier
                        }
                    } for bubbleobject in event.map.bubbles)
                ]
            },
            "random": event.scene.random.getstate(),
            "version": "0.2.0"
        }

        # print(event.scene.rand.getstate())

        save_file = self.saveFile.format(self.save_name)
        save_file_path = os.path.join(self.savePath, save_file)

        nzt_file = NZTFile(save_file_path, "w+")
        nzt_file.data = nzt_data
        nzt_file.save()

        #
        # # If the save directory doesn't exist, create it
        # if not os.path.exists(self.savePath):
        #     self.timestamp_print(
        #         'Creating directory: {}'.format(self.savePath))
        #     os.makedirs(self.savePath)
        #
        # # Efficiently save the save to a binary file
        # with open(save_file_path, 'wb+') as file:
        #     # noinspection PyProtectedMember,SpellCheckingInspection
        #     pickle.dump({"player": [(event.player.lives, event.player.score, event.player._Player__position,
        #                              event.player.rotation, event.player.ghostMode)],
        #                  "bubbles": [(bubbleobject.name,
        #                               bubbleobject.size,
        #                               bubbleobject.speed,
        #                               bubbleobject.position
        #                               ) for bubbleobject in event.map.bubbles],
        #                  "rand": event.scene.rand.getstate(),
        #                  "effects": [(appliedeffect.baseEffectClass.get_unlocalized_name(),
        #                               appliedeffect._get_time_remaining(),
        #                               appliedeffect.strengthMultiply
        #                               ) for appliedeffect in event.player.activeEffects]
        #                  }, file)

        self.timestamp_print('Saving completed')

    def __getitem__(self, item):
        return self._data.get(item)

    def __setitem__(self, key, item):
        self._data[key] = item

    def get(self, item, default):
        return self._data.get(item, default)

    def keys(self):
        return self._data.keys()
