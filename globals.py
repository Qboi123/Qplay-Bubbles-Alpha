from typing import Dict, List

# from bubble import Bubble

NAME2BUBBLE: Dict[str, object] = dict()
BUBBLE2NAME: Dict[object, str] = dict()
NAME2EFFECT: Dict[str, type] = dict()
EFFECT2NAME: Dict[type, str] = dict()
GAME_OBJECTS: List[object] = list()

del Dict, List
