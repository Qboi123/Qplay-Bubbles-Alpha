from pyglet.sprite import Sprite

from typinglib import Float, Integer, Union


class Entity(Sprite):
    def __init__(self, defence_mp: Float, attack_mp: Float, regen_mp: Float, health: Float, max_health: Float,
                 image, x=0, y=0, batch=None, group=None, subpixel=False):
        self.defenceMultiplier = defence_mp
        self.attackMultiplier = attack_mp
        self.regenMultiplier = regen_mp
        self.maxHealth = max_health
        self.health = health

        self.damageHook = lambda: None
        self.regenHook = lambda: None

        self.invulnerable = False

        self.dead = False

        super(Entity, self).__init__(image, x, y, batch=batch, group=group, subpixel=subpixel)

    def _check_dead(self):
        if float(self.health) <= 0:
            self.dead = True
            # print("DEAD:", self.dead)
            # self.delete()

    def damage(self, atk: Union[Float, Integer]):
        if (not self.dead) and not self.invulnerable:
            if float(atk) == 0.0:
                return
            elif float(atk) < 0.0:
                raise ValueError(f"Damage value can't be under zero, value is '{atk}'")
            elif float(self.defenceMultiplier) == 0.0:
                self.health = 0.0
            else:
                # print("Attacked")
                # print(atk)
                new_value = self.health - float(atk / self.defenceMultiplier)
                if float(new_value) < 1.0:
                    new_value = 0.0
                self.health = new_value
            self._check_dead()

    def regen(self, value: Union[Float, Integer]):
        if not self.dead:
            if value == 0.0:
                return
            if value < 0.0:
                raise ValueError(f"Regeneration can't be under zero, value is '{value}'")
            new_value = self.health + int(value * self.regenMultiplier)
            if new_value > self.maxHealth:
                new_value = self.maxHealth
            self.health = new_value
