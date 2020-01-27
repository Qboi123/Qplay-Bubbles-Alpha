import os
import pickle
import zipfile
from typing import Optional, Union, Iterable

from utils import File

zipf = zipfile.ZipFile("File.zip", "w")


class ZipFormatFile(File):
    def __init__(self, path, password=None, mode="w"):
        super().__init__(path)
        import os

        self._currentDir = "/"
        self.zipfile = zipfile.ZipFile(path, mode)
        self.password = password

    def chdir(self, path):
        path = self.get_fp(path)
        self._currentDir = path

    def getcwd(self):
        return self._currentDir

    def split_path(self, path: str):
        # if path.count('/') >= 2:
        #     paths = self.os.path.split(path)
        #     s_paths = self.split_path(paths[0])
        #     return (s_paths[0], s_paths[1], paths[1])
        # elif path.count('/') == 1:
        #     return self.os.path.split(path)
        # else:
        #     return [path]
        return tuple(path.replace("\\", "/").split("/"))

    def get_fp(self, fp=None):
        if not fp:
            fp = self._currentDir
        else:
            if not self.os.path.isabs(fp):
                fp = self.os.path.join(self._currentDir, fp).replace("\\", "/")

        fp = fp.replace("\\", "/")

        if fp[-1] == "/" and fp != "/":
            fp = fp[:-1]

        return fp[1:]

    def listdir(self, fp=None):
        fp = self.get_fp(fp)
        list_ = []
        # print(self.zipFormatFile.infolist())
        for item in self.zipfile.infolist():
            if len(self.split_path(item.filename)) >= 2:
                # print(item.filename)
                # print(self.split_path(item.filename))
                # print(self.os.path.split(item.filename))
                s_path2 = self.split_path(item.filename)[:-1]
                s_path3 = "/"+self.os.path.join(
                    s_path2[0] if len(s_path2) >= 2 else "", *[s_path2[1]] if len(s_path2) >= 3 else []).\
                    replace("\\", "/")

                # print("SPath:", s_path2)
                # print("SPath 3:", s_path3)
                if s_path2:
                    if s_path3 == fp:
                        list_.append(self.split_path(item.filename)[-2])
            if "/"+self.os.path.join(*self.os.path.split(item.filename)[:-1]) == fp:
                list_.append(self.os.path.split(item.filename)[-1])
        return list_

    def listfiles(self, fp=None):
        fp = self.get_fp(fp)

        list_ = []
        # print(self.zipFormatFile.infolist())
        for item in self.zipfile.infolist():
            if "/"+self.os.path.join(*self.os.path.split(item.filename)[:-1]) == fp:
                if not item.is_dir():
                    list_.append(self.os.path.split(item.filename)[-1])
        return list_

    def listdirs(self, fp=None):
        fp = self.get_fp(fp)

        list_ = []
        # print(self.zipFormatFile.infolist())
        for item in self.zipfile.infolist():
            if len(self.split_path(item.filename)) >= 2:
                # print(item.filename)
                # print(self.split_path(item.filename))
                # print(self.os.path.split(item.filename))
                s_path2 = self.split_path(item.filename)[:-1]
                s_path3 = "/"+self.os.path.join(
                    s_path2[0] if len(s_path2) >= 2 else "", *[s_path2[1]] if len(s_path2) >= 3 else []).\
                    replace("\\", "/")

                # print("SPath:", s_path2)
                # print("SPath 3:", s_path3)
                if s_path2:
                    if s_path3 == fp:
                        list_.append(self.split_path(item.filename)[-2])
            if "/"+self.os.path.join(*self.os.path.split(item.filename)[:-1]) == fp:
                if item.is_dir():
                    list_.append(self.os.path.split(item.filename)[-1])
        return list_


# noinspection PyProtectedMember
class ZippedFile(object):
    def __init__(self, zip_file: ZipFormatFile, path: str, pwd=None):
        self.zipFormatFile = zip_file
        self.path = path
        self.password = pwd

        self.fileName = os.path.split(path)[-1]

        self._fd: Optional[zipfile.ZipExtFile] = None
        self._fileOpen = False

    def read(self):
        return self.zipFormatFile.zipfile.read(self.zipFormatFile.get_fp(self.path)[1:])

    def write(self, data: Union[bytes, bytearray]):
        with self.zipFormatFile.zipfile.open(self.path, "r+b", self.password, "w") as file:
            file.write(data)

    def __repr__(self):
        return f"<ZippedFile '{self.path}'>"


# noinspection PyProtectedMember
class ZippedDirectory(object):
    def __init__(self, zip_file: ZipFormatFile, path, pwd=None):
        import os
        self.zipFormatFile = zip_file
        self.path = path
        self.password = pwd
        self.dirName = os.path.split(path)[-1]

        self.os = os

    def create(self):
        pass

    def listdir(self):
        return self.index()

    def index(self):
        list_ = []
        for file in self.zipFormatFile.listdirs(self.path):
            list_.append(
                ZippedDirectory(self.zipFormatFile, self.os.path.join(self.path, file).replace("\\", "/"), self.password))

        for file in self.zipFormatFile.listfiles(self.path):
            list_.append(
                ZippedFile(self.zipFormatFile, self.os.path.join(self.path, file).replace("\\", "/"), self.password))
        return list_

    def listfiles(self):
        return [
            ZippedFile(self.zipFormatFile, self.os.path.join(self.path, file).replace("\\", "/"), self.password)
            for file in self.zipFormatFile.listfiles(self.path)]

    def listdirs(self):
        return [
            ZippedDirectory(self.zipFormatFile, self.os.path.join(self.path, dir_).replace("\\", "/"), self.password)
            for dir_ in self.zipFormatFile.listdirs(self.path)]

    def __repr__(self):
        return f"<ZippedDirectory '{self.path}'>"


class ZipFile(ZippedDirectory):
    def __init__(self, path):
        zip_file = ZipFormatFile(path)
        super().__init__(zip_file, "/")

        import os

        self.absPath: str = os.path.abspath(path)
        try:
            self.relPath: str = os.path.relpath(path)
        except ValueError:
            self.relPath: Optional[str] = None


class NZTFile(ZipFile):
    def __init__(self, filename):
        super().__init__(filename)
        self._contents = {}
        self.data: dict = {}

    def _save(self, fp: str, data: Union[dict, list]):
        if type(data) == dict:
            for key, value in data.items():
                if type(value) == int:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, "{key}.int")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == float:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.float")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == str:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.str")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == bytes:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.bytes")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == bytearray:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.bytearray")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == bool:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.bool")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == list:
                    self.zipFormatFile.zipfile.writestr(
                        zipfile.ZipInfo(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.list/"))), '')
                    self._save(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.list")), value)
                elif type(value) == dict:
                    self.zipFormatFile.zipfile.writestr(
                        zipfile.ZipInfo(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.dict/"))), '')
                    self._save(self.zipFormatFile.get_fp(os.path.join(fp, f"{key}.dict")), value)
        elif type(data) == list:
            for index in range(len(data)):
                value = data[index]
                if type(value) == int:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.int")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == float:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.float")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == str:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.str")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == bytes:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.bytes")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == bytearray:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.bytearray")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == bool:
                    with self.zipFormatFile.zipfile.open(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.bool")), "w") as file:
                        pickle.dump(value, file)
                        file.flush()
                        file.close()
                elif type(value) == list:
                    self.zipFormatFile.zipfile.writestr(
                        zipfile.ZipInfo(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.list/"))), '')
                    self._save(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.list")), value)
                elif type(value) == dict:
                    self.zipFormatFile.zipfile.writestr(
                        zipfile.ZipInfo(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.dict/"))), '')
                    self._save(self.zipFormatFile.get_fp(os.path.join(fp, f"{index}.dict")), value)

    def save(self):
        self.zipFormatFile.open("wb")
        for key, value in self.data.items():
            if type(value) == int:
                with self.zipFormatFile.zipfile.open(f"{key}.int", "w") as file:
                    pickle.dump(value, file)
                    file.flush()
                    file.close()
            elif type(value) == float:
                with self.zipFormatFile.zipfile.open(f"{key}.float", "w") as file:
                    pickle.dump(value, file)
                    file.flush()
                    file.close()
            elif type(value) == str:
                with self.zipFormatFile.zipfile.open(f"{key}.str", "w") as file:
                    pickle.dump(value, file)
                    file.flush()
                    file.close()
            elif type(value) == bytes:
                with self.zipFormatFile.zipfile.open(f"{key}.bytes", "w") as file:
                    pickle.dump(value, file)
                    file.flush()
                    file.close()
            elif type(value) == bytearray:
                with self.zipFormatFile.zipfile.open(f"{key}.bytearray", "w") as file:
                    pickle.dump(value, file)
                    file.flush()
                    file.close()
            elif type(value) == bool:
                with self.zipFormatFile.zipfile.open(f"{key}.bool", "w") as file:
                    pickle.dump(value, file)
                    file.flush()
                    file.close()
            elif type(value) == list:
                self.zipFormatFile.zipfile.writestr(
                    zipfile.ZipInfo(f"{key}.list/"), '')
                self._save(self.zipFormatFile.get_fp(f"{key}.list"), value)
            elif type(value) == dict:
                self.zipFormatFile.zipfile.writestr(
                    zipfile.ZipInfo(f"{key}.dict/"), '')
                self._save(self.zipFormatFile.get_fp(f"{key}.dict"), value)
        self.zipFormatFile.zipfile.close()

    def _load(self, zipped_dir: ZippedDirectory, data: Union[dict, list]):
        for item in zipped_dir.index()
            if type(item) == ZippedDirectory:
                if os.path.splitext(item.dirName) == ".dict":
                    self._load(zipped_dir, {})
                if os.path.splitext(item.dirName) == ".list":
                    self._load(zipped_dir, {})

    def load(self):
        for item in self.index():
            if type(item) == ZippedDirectory:
                if os.path.splitext(item.dirName) == ".dict":
                    self._load(zipped_dir, {})
                if os.path.splitext(item.dirName) == ".list":
                    self._load(zipped_dir, {})


if __name__ == '__main__':
    nzt_file = NZTFile("Test.nzt")
    nzt_file.data = {"string": "Hallo", "int": 39, "float": 43.6, "boolean": True, "object": lambda: print("Hallo"),
                     "dict": {"Hoi": 3, "Hallo": False}, "list": [485.4, False, 95, "Hoi", 40]}
    nzt_file.save()
