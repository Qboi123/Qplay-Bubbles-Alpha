from pyglet.sprite import Sprite
from typing import List

from bubble import Bubble
from sprites.bubbles import NormalBubble, TripleBubble, SpeedyBubble, DoubleBubble, DeadlyBubble, LifeBubble
from sprites.player import Player

BUBBLES: List[Bubble] = list()
BUBBLES.append(NormalBubble())
BUBBLES.append(SpeedyBubble())
BUBBLES.append(DoubleBubble())
BUBBLES.append(TripleBubble())
BUBBLES.append(DeadlyBubble())
BUBBLES.append(LifeBubble())

ALL: List[Sprite] = list()
ALL.extend(BUBBLES)
ALL.append(Player)
