class UnlocalizedNameError(Exception):
    def __init__(self, *args):
        super(UnlocalizedNameError, self).__init__(*args)


class UnresolvedValueError(Exception):
    def __init__(self, *args):
        super(UnresolvedValueError, self).__init__(*args)


class TextureWarning(Warning):
    def __init__(self, *args):
        super(TextureWarning, self).__init__(*args)
