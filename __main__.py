from typinglib import Boolean, String, Float, Tuple

VERSION: Tuple = ("indev", 0, 1, 0)


def main(args):
    display = pyglet.canvas.get_display()
    # display = platform.get_default_display()
    screen = display.get_default_screen()
    # screen_width = screen.width
    # screen_height = screen.height

    screen_width = 1280
    screen_height = 800

    init.init()
    window = pyglet.window.Window(screen_width, screen_height, caption="Qplay Bubbles %s" % version2name(VERSION), resizable=False, fullscreen=True, display=display, screen=screen)
    window.set_minimum_size(800, 600)
    scene_manager = SceneManager(window, init)
    init.post_init()
    pyglet.clock.schedule_interval(scene_manager.update, UPDATE_INTERVAL)
    pyglet.clock.schedule_interval(scene_manager.tick_update, TICKS_PER_SEC)
    pyglet.clock.schedule_interval(scene_manager.auto_save_update, AUTO_SAVE_INTERVAL)
    graphics.setup()


if __name__ == '__main__':
    import os
    import time

    from log import Log
    import sys

    startup: Float = time.time()
    startup2: String = time.ctime(startup).replace(" ", "-").replace(":", ".")

    # if not os.path.exists("../../logs"):
    #     os.makedirs("../../logs")
    #
    # if not os.path.exists("../../logs"):
    #     os.makedirs("../../logs")

    if "--debug" in sys.argv:
        write_std: Boolean = True
    else:
        write_std: Boolean = False

    log_file: String = time.strftime(f"%d-%m-%Y %H_%M_%S.log", time.gmtime(startup))

    stderr = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stderr__, "ERROR", write_std)
    stdwrn = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stderr__, "WARN", write_std)
    stdout = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__, "Info", write_std)
    stdbug = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__, "Debug", write_std)
    stdin = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__, "Input", write_std)

    sys.stdbug = stdbug
    sys.stdwrn = stdwrn
    sys.stderr = stderr
    sys.stdout = stdout
    sys.stdin = stdin

    import pyglet

    from init import Init

    init: Init = Init()
    init.pre_init()

    import graphics
    from scenemanager import SceneManager
    from utils import version2name, UPDATE_INTERVAL, TICKS_PER_SEC, AUTO_SAVE_INTERVAL

    main(sys.argv)
    pyglet.app.run()
