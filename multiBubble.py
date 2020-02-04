from typing import List


class MultiBubbleRegistry(object):
    def __init__(self):
        self.registry = []

    def add(self, item):
        if type(item) != tuple:
            tuple(item)

        self.registry.append(item)


class MultiBubble(object):
    def __init__(self, curr_bubble=None, on_complete=lambda multi_bubble: None, on_mismatch=lambda multi_bubble: None):
        self.currBubble = curr_bubble

        self.repeatAfterEnd: bool = False

        self.bubbleList: List = []
        self.__historyList: List = []
        self.historyList = property(lambda: self.__historyList)

        self.dead = False

        self.__index = -1
        self.currentIndex = property(lambda: self.__index)

        self.onComplete = on_complete
        self.onMismatch = on_mismatch

        if curr_bubble:
            self.new(curr_bubble)

    def new(self, bubble):
        if self.bubbleList[self.__index + 1] == bubble.baseBubbleClass and not self.dead:
            self.__index += 1
            self.currBubble = bubble
            self.__historyList.append(bubble)
            if self.__index == len(self.bubbleList):
                self.onComplete(self)
        else:
            self.dead = True
            self.currBubble = bubble
            self.onMismatch(self)
