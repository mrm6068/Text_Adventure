import items, enemies, actions, world, random
from player import Player
import time
 
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()
 
    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves
 
    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        return moves


class StartingRoom(MapTile):
    # override the intro_text method in the superclass
    def intro_text(self):

        
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class LootRoom(MapTile):
    def __init__(self, x, y, item, beenThere):
        self.item = item
        self.beenThere = False
        super().__init__(x, y)
 
    def add_loot(self, player):
        if(self.beenThere == False):#If you have not been here...  
            player.inventory.append(self.item)#Add item to player inventory
            self.beenThere = True
 
    def modify_player(self, player):
        self.add_loot(player)

  


class HealthRoom(MapTile):#Super to PotionRoom, ...
    def __init__(self, x, y, health, beenThere):
        self.health = health
        self.beenThere = False
        super().__init__(x, y)
 
    def add_hp(self, player):
        player.hp += self.health
        if player.hp > player.maxHp:
            player.hp = player.maxHp

        print("HP is {}\n".format(player.hp))
 
    def modify_player(self, player):
        self.add_hp(player)

class PotionRoom(HealthRoom):
    def __init__(self, x, y):
        super().__init__(x, y, 25, beenThere = False)#25 hp potion

    def intro_text(self):
        if self.beenThere:
            return """
                \nThis is the room you found the potion.\n"""

        else:
            self.beenThere = True
            print( """\n   /***\\""")
            time.sleep(1)
            print( """  /^^^^^\\""") 
            time.sleep(1)
            print( """ /       \\""")
            time.sleep(1)
            print( """< POTION  >""")
            time.sleep(1)
            print( """ \       /""")
            time.sleep(1)
            print( """  \     /""")
            time.sleep(1)
            print( """   \___/\n""")
            time.sleep(1)

            return """
                \nYou found a bottle and you drink the purple potion.
                You gained 25 HP!\n"""


'''class VendorRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)
 
    def add_loot(self, player):
        player.inventory.append(self.item)
 
    def modify_player(self, player):
        self.add_loot(player)'''


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage

            if the_player.hp < 0:#No negative hp
                the_player.hp = 0

            print("Enemy does {} damage. You have {} HP remaining\n".format(self.enemy.damage, the_player.hp))
 
    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()

class EmptyCavePath(MapTile):
    def intro_text(self):
        #Random intro text for each cave room.
        text = []
        text.append( "\nAnother unremarkable part of the cave. You must forge onwards.")
        text.append("\nThis room is dark and empty.")
        text.append("\nThere isn't much going on in this room.")
        r = random.randint(0, len(text)-1)
        return text[r]
 
    def modify_player(self, player):
        #Room has no action on player
        pass
 
class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())
 
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """

class HellhoundRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Hellhound())
 
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A massive flaming dog growls angrily as you enter his lair.  
            """
        else:
            return """
            A Hellhound corpse.  How did I ever manage to kill that thing?
            """
 
class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
       #self.beenThere = False
        super().__init__(x, y, items.Dagger(), beenThere = False)


 
    def intro_text(self):
        if self.beenThere:
            return """
            You have been here before...
            This is where you found a dagger!
            """
        else:
            print( """\n    /\\""")
            time.sleep(.7)
            print( """   |  |""") 
            time.sleep(.7)
            print( """   |  |""")
            time.sleep(.7)
            print( """   |  |""")
            time.sleep(.7)
            print( """ __|  |__""")
            time.sleep(.7)
            print( """|___   __|""")
            time.sleep(.7)
            print( """    | |""")
            time.sleep(.7)
            print( """    ---""")
            time.sleep(.7)

            return """
            Your notice something shiny in the corner.
            It's a dagger! You pick it up.
            """



           
class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        player.victory = True