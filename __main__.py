import pyglet

import graphics
from scenemanager import SceneManager
from utils import version2name, UPDATE_INTERVAL, TICKS_PER_SEC, AUTO_SAVE_INTERVAL
import resources

VERSION = ("indev", 0, 0, 1)


def main(args):
    res = resources.Resources()
    res.reindex()
    res.load()
    window = pyglet.window.Window(1200, 700, "Qplay Bubbles %s" % version2name(VERSION))
    scene_manager = SceneManager(window)
    pyglet.clock.schedule_interval(scene_manager.update, 1.0 / UPDATE_INTERVAL)
    pyglet.clock.schedule_interval(scene_manager.tick_update, 1.0 / TICKS_PER_SEC)
    pyglet.clock.schedule_interval(scene_manager.tick_update, AUTO_SAVE_INTERVAL)
    graphics.setup()


if __name__ == '__main__':
    import sys
    main(sys.argv)
    pyglet.app.run()
