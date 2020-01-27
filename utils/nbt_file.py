from typing import Union, List, Dict

from nbt.nbt import *
import nbt

nbt_file = NBTFile()

nbt_file["hallo"] = nbt.nbt.TAG_Int(3)
nbt_file["dict"] = nbt.nbt.TAG_Compound()
nbt_file["dict"]["string"] = nbt.nbt.TAG_String("Hallo")
nbt_file.write_file("hallo.nbt")


def get_nbt_tag(value):
    if type(value) == float:
        return nbt.nbt.TAG_Float(value)
    elif type(value) == int:
        return nbt.nbt.TAG_Long(value)
    elif type(value) == str:
        return nbt.nbt.TAG_String(value)
    # if type(value) == bytes:
    #     return nbt.nbt.TAG_Byte(eval("0x"+value.hex()))
    elif type(value) == list:
        return get_nbt_list(value[0], value[1:])
    elif type(value) == dict:
        return get_nbt_compound(value)
    else:
        raise TypeError(f"Type {repr(value)} is not an integer, string, float, list or dictionary")


def get_nbt_list(type_: type, list_: list):
    if type_ == int:
        tag_type = nbt.nbt.TAG_Long
    elif type_ == str:
        tag_type = nbt.nbt.TAG_String
    elif type_ == float:
        tag_type = nbt.nbt.TAG_Float
    elif type_ == list:
        tag_type = nbt.nbt.TAG_List
    elif type_ == dict:
        tag_type = nbt.nbt.TAG_Compound
    else:
        raise TypeError(f"Type {type_.__name__} is not integer, string, float, list or dictionary")

    tag_list = nbt.nbt.TAG_List(tag_type, [])
    for item in list_:
        if type(item) == type_:
            tag_list.append(get_nbt_tag(item))
        else:
            raise TypeError(f"{repr(item)} is not a(n) {type_.__name__}")
    return tag_list


def get_nbt_compound(dict_: dict):
    tag_compound = nbt.nbt.TAG_Compound()
    for key, value in dict_.items():
        tag_compound[key] = get_nbt_tag(value)
    return tag_compound


def get_nbt(dict_: dict):
    nbt_file_ = NBTFile()
    for key, value in dict_.items():
        nbt_file_[key] = get_nbt_tag(value)
    return nbt_file_


if __name__ == '__main__':
    a = {"string": "value",
         "int": 39,
         "float": 39.74,
         "compound": {"string2": "value2",
                      "int2": 75,
                      "float2": 75.23
                      },
         "list": [float, 39.54, 93.48, 61.45]
         }
    nbt_file = get_nbt(a)
    nbt_file.write_file("test2.nbt")


def get(tag: TAG) -> Union[str, int, float, list, dict]:
    if type(tag) == TAG_Long:
        tag: TAG_Long
        return get_long(tag)
    elif type(tag) == TAG_Int:
        tag: TAG_Int
        return get_int(tag)
    elif type(tag) == TAG_Short:
        tag: TAG_Short
        return get_short(tag)
    elif type(tag) == TAG_Float:
        tag: TAG_Float
        return get_float(tag)
    elif type(tag) == TAG_String:
        tag: TAG_String
        return get_string(tag)
    elif type(tag) == TAG_Double:
        tag: TAG_Double
        return get_double(tag)
    elif type(tag) == TAG_List:
        tag: TAG_List
        return get_list(tag)
    elif type(tag) == TAG_Compound:
        tag: TAG_Compound
        return get_compound(tag)


def get_string(tag: TAG_String) -> str:
    return tag.value


def get_int(tag: TAG_Int) -> int:
    return tag.value


def get_long(tag: TAG_Long) -> int:
    return tag.value


def get_short(tag: TAG_Short) -> int:
    return tag.value


def get_double(tag: TAG_Double) -> Union[int, float]:
    return tag.value


def get_float(tag: TAG_Float) -> float:
    return tag.value


def get_byte(tag: TAG_Byte) -> int:
    return tag.value


def get_compound(tag: TAG_Compound) -> Dict[str, Union[str, int, float, list, dict]]:
    dict_ = {}
    for key, value in tag.items():
        dict_[key] = get(value)
    return dict_


def get_file(nbt_: NBTFile) -> Dict[str, Union[str, int, float, list, dict]]:
    dict_ = {}
    for key, value in nbt_.items():
        dict_[key] = get(value)
    return dict_


def get_list(tag: TAG_List) -> List[Union[str, int, float, list, dict]]:
    list_ = []
    for item in tag:
        list_.append(get(item))
    return list_
