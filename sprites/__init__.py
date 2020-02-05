from pyglet.sprite import Sprite
from typing import List, Union, Type

from bubble import Bubble
from sprites.bubbles import *
from sprites.player import Player

BUBBLES: List[Bubble] = list()
BUBBLES.append(NormalBubble())
BUBBLES.append(SpeedyBubble())
BUBBLES.append(KeyBubble())
BUBBLES.append(DoubleBubble())
BUBBLES.append(TripleBubble())
BUBBLES.append(DecupleBubble())
BUBBLES.append(DoubleScoreStatBubble())
BUBBLES.append(TripleScoreStatBubble())
BUBBLES.append(DecupleScoreStatBubble())
BUBBLES.append(DeadlyBubble())
BUBBLES.append(LifeBubble())
BUBBLES.append(TeleporterBubble())
BUBBLES.append(SpeedBoostBubble())
BUBBLES.append(SlownessBubble())
BUBBLES.append(UltraBubble())
BUBBLES.append(GhostBubble())
# BUBBLES.append(ConfusionBubble())
BUBBLES.append(ParalyseBubble())
BUBBLES.append(ProtectionBubble())

ALL: List[Union[Bubble, Type[Player]]] = list()
ALL.extend(BUBBLES)
ALL.append(Player)
