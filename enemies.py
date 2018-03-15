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

class Bear(Enemy):
    def __init__(self):
        super().__init__(name="Bear", hp=25, damage=12, experience=30)

class RatHumanoid(Enemy):
    def __init__(self):
        super().__init__(name="Rat Humanoid", hp=200, damage=35, experience=1000)

class Bats(Enemy):
    def __init__(self):
        super().__init__(name="Bats", hp=15, damage=10, experience=30)

class Zombie(Enemy):
    def __init__(self):
        super().__init__(name="Zombie", hp=25, damage=20, experience=20)

class Crawler(Enemy):
    def __init__(self):
        super().__init__(name="Crawler", hp=50, damage=20, experience=35)