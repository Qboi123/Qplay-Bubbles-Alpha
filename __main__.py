VERSION = ("indev", 0, 0, 1)


def main(args):
    window = pyglet.window.Window(1200, 700, "Qplay Bubbles %s" % version2name(VERSION))
    scene_manager = SceneManager(window, init)
    init.post_init()
    pyglet.clock.schedule_interval(scene_manager.update, 1.0 / UPDATE_INTERVAL)
    pyglet.clock.schedule_interval(scene_manager.tick_update, 1.0 / TICKS_PER_SEC)
    pyglet.clock.schedule_interval(scene_manager.auto_save_update, AUTO_SAVE_INTERVAL)
    graphics.setup()


if __name__ == '__main__':
    import os
    import time

    from log import Log
    import sys

    startup = time.time()
    startup2 = time.ctime(startup).replace(" ", "-").replace(":", ".")

    # if not os.path.exists("../../logs"):
    #     os.makedirs("../../logs")
    #
    # if not os.path.exists("../../logs"):
    #     os.makedirs("../../logs")

    log_file = time.strftime(f"%d-%m-%Y %H_%M_%S.log", time.gmtime(startup))

    stderr = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stderr__, "ERROR")
    stdwrn = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stderr__, "WARN")
    stdout = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__, "Info")
    stdbug = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__, "Debug")
    stdin = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__, "Input")

    sys.stdbug = stdbug
    sys.stdwrn = stdwrn
    sys.stderr = stderr
    sys.stdout = stdout
    sys.stdin = stdin

    import pyglet

    from init import Init

    init = Init()
    init.pre_init()

    import graphics
    from scenemanager import SceneManager
    from utils import version2name, UPDATE_INTERVAL, TICKS_PER_SEC, AUTO_SAVE_INTERVAL

    main(sys.argv)
    pyglet.app.run()
