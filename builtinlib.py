Print = print
Input = input
Set = set
setAttr = setattr
getAttr = getattr
hasAttr = hasattr
setAttribute = setattr
getAttribute = getattr
hasAttribute = hasattr

NULL = None
NONE = None
TRUE = True
FALSE = False

String = lambda o="": str(o)
Integer = lambda o=0: int(o)
Float = lambda o=0.0: float(o)
List = lambda o=[]: list(o)
Dictionary = lambda o={}: dict(o)
Bytes = lambda o=b'': bytes(o)
ByteArray = bytearray
Object = object
Type = type
Complex = complex

# Array = EditableClass


if __name__ == '__main__':
    a: String = String("Hallo")
