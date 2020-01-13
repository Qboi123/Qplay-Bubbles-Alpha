from pyglet.sprite import Sprite
from typing import List, Union, Type

from bubble import Bubble
from sprites.bubbles import *
from sprites.player import Player

BUBBLES: List[Bubble] = list()
BUBBLES.append(NormalBubble())
BUBBLES.append(SpeedyBubble())
BUBBLES.append(DoubleBubble())
BUBBLES.append(TripleBubble())
BUBBLES.append(DeadlyBubble())
BUBBLES.append(LifeBubble())
BUBBLES.append(TeleporterBubble())
BUBBLES.append(SpeedBoostBubble())

ALL: List[Union[Bubble, Type[Player]]] = list()
ALL.extend(BUBBLES)
ALL.append(Player)
