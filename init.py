import resources


class Init(object):
    allBubbles = []
    def __init__(self):
        pass

    @staticmethod
    def pre_init():
        res = resources.Resources()
        res.reindex()
        res.load()

        import sprites.bubbles

        Init.allBubbles = sprites.BUBBLES

    @staticmethod
    def init():
        import bubble as b

        for bubble in Init.allBubbles:
            bubble: b.Bubble
            bubble.check_unlocalized_name()

    @staticmethod
    def post_init():
        pass
