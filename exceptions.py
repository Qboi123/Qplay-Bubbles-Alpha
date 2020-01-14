import sys
import traceback


class UnlocalizedNameError(Exception):
    def __init__(self, *args):
        super(UnlocalizedNameError, self).__init__(*args)


class UnresolvedValueError(Exception):
    def __init__(self, *args):
        super(UnresolvedValueError, self).__init__(*args)


class Warning(Warning):
    def __init__(self, *args):
        super(Warning, self).__init__(*args)
        print("\nWarning traceback (most recent call last):", file=sys.stdwrn)
        traceback.print_stack(self.__traceback__, file=sys.stdwrn)
        traceback.print_exception(self, self, self.__traceback__, file=sys.stdwrn)


class TextureWarning(Warning):
    def __init__(self, *args):
        super(TextureWarning, self).__init__(*args)


class ModelWarning(Warning):
    def __init__(self, *args):
        super(ModelWarning, self).__init__(*args)
