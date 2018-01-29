class Enemy:
    def __init__(self, name, hp, damage, experience):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.experience = experience
 
    def is_alive(self):
        return self.hp > 0

class GiantSpider(Enemy):
    def __init__(self):
        super().__init__(name="Giant Spider", hp=10, damage=2, experience=10)
 
 
class Ogre(Enemy):
    def __init__(self):
        super().__init__(name="Ogre", hp=30, damage=15, experience=30)

class Hellhound(Enemy):
    def __init__(self):
        super().__init__(name="Hellhound", hp=20, damage=10, experience=20)