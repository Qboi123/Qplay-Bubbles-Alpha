import resources


class Init(object):
    def __init__(self):
        pass

    @staticmethod
    def pre_init():
        res = resources.Resources()
        res.reindex()
        res.load()

    def init(self):
        pass

    def post_init(self):
        pass
