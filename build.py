import os

# noinspection PyCompatibility
from compiler import Compiler

"""
Default:        |            | pyinstaller -y 
First args:     | first_args | -F -w          -F = one file | -w = hides the console
Icon:           | icon       | -i ICON
Additional Data | add_data   | --add-data "<FILE_PATH>";"<EXPORT_FP>" --add-data "<FILE_PATH>";"<EXPORT_FP>" ...
UPX Directory   | upx_dir    | --upx-dir UPX_DIR
No Unicode Su...| no_unicode | -a
Clean PyInsta...| clean      | --clean
Log Level       | log_level  | --log-level DEBUG|INFO|WARN|ERROR|CRITICAL
App Name        | app_name   | -n NAME

"""

if __name__ == '__main__':
    # Main variables
    # exclude_ = [".idea", ".gitattributes", ".gitignore", "build_config.json", "dll", "build.py", "README.md", "venv",
    #             "output", "obj", "icon.png", ]
    #
    # icon_ = "./icon.ico"

    main_folder_ = os.getcwd()
    compiler = Compiler(
        exclude=[".idea", ".gitattributes", ".gitignore", "build_config.json", "dll", "build.py", "README.md",
                 "venv", "output", "obj", "icon.png", ".git", "assets/temp", "assets/sfx/GitHubDesktopSetup.exe",
                 "assets/sfx/pyglet-master.zip", "assets/sfx/source-archive.zip", "compiler.py", "dll"],
        icon="icon.ico", main_folder=os.getcwd(), main_file="__main__.py",
        hidden_imports=["pyglet", "PIL", "sys", "os", "pyglet.gui", "pyglet.gl", "pyglet.graphics", "pyglet.window",
                        "pyglet.image", "pyglet.resource", "collections", "typing", "tempfile", "io", "win32ctypes"],
        log_level="INFO", app_name="Qplay Bubbles", clean=True,
        dlls=["dll/avcodec.dll", "dll/avcodec-58.dll", "dll/avutil-56.dll"])
    compiler.reindex()

    args = compiler.get_args()
    command = compiler.get_command(args)
    compiler.compile(command)
