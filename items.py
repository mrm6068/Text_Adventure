import sounds
# Base class for all items
class Item():
    # __init__ is the contructor method
    def __init__(self, name, description, value):
        self.name = name   # attribute of the Item class and any subclasses
        self.description = description # attribute of the Item class and any subclasses
        self.value = value # attribute of the Item class and any subclasses
    
    # __str__ method is used to print the object
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)

# Extend the Items class
# Gold class will be a child or subclass of the superclass Item
class Gold(Item):
    # __init__ is the contructor method
    def __init__(self, amt): 
        self.amt = amt # attribute of the Gold class
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt)

class Weapon(Item):
    def __init__(self, name, description, value, minDamage, maxDamage):
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        
        super().__init__(name, description, value)
 
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}-{}"\
            .format(self.name, self.description, self.value, self.minDamage, self.maxDamage)

    def sound(self):#Each weapon CAN have it's own sound.
        pass
        
 
class Rock(Weapon):
    def __init__(self):
        super().__init__(name="Rock",
                         description="A fist-sized rock, suitable for bludgeoning.",
                         value=0,
                         minDamage=3,
                         maxDamage=5)
 
class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dagger",
                         description="A small dagger with some rust. Somewhat more dangerous than a rock.",
                         value=10,
                         minDamage=3,
                         maxDamage=5)

class Projectile(Weapon):
    def __init__(self, name, description, value, minDamage, maxDamage, ammo):
        self.ammo = ammo
        
        super().__init__(name, description, value, minDamage, maxDamage)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}-{}\nAmmo: {}"\
            .format(self.name, self.description, self.value, self.minDamage,\
           self.maxDamage, self.ammo)

class Crossbow(Projectile):
    def __init__(self):
        super().__init__(name="Crossbow",
                         description="A wooden crossbow",
                         value=30,
                         minDamage=7,
                         maxDamage=13,
                         ammo = 2)
    def sound(self):
        sounds.arrow()

class Moltov(Projectile):
    def __init__(self):
        super().__init__(name="Moltov cocktail",
                         description="One moltov cocktail, use it wisely",
                         value=20,
                         minDamage=25,
                         maxDamage=40,
                         ammo = 1)
    def sound(self):
        sounds.moltov()

class Revolver(Projectile):
    def __init__(self):
        super().__init__(name="Revolver",
                         description="A 5-shot revolver",
                         value=30,
                         minDamage=14,
                         maxDamage=21,
                         ammo = 5)
    def sound(self):
        sounds.gun()

class Slingshot(Projectile):
    def __init__(self):
        super().__init__(name="Slingshot",
                         description="A slingshot",
                         value=20,
                         minDamage=5,
                         maxDamage=11,
                         ammo = 4)

class Pillow(Weapon):
    def __init__(self):
        super().__init__(name="Pillow",
                         description="A pillow for handling my soft work",
                         value=1,
                         minDamage=1,
                         maxDamage=3)

class SkullKey(Item):
    # __init__ is the contructor method
    def __init__(self): 
        super().__init__(name="Skull Key",
                         description="An old key shaped like a skull",
                         value=5)

class FinalKey(Item):
    # __init__ is the contructor method
    def __init__(self): 
        super().__init__(name="Final Key",
                         description="The last key you will ever need",
                         value=5)