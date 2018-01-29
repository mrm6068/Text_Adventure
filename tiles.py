import items, enemies, actions, world
from player import Player
 
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.beenThere = False

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
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)
 
    def add_loot(self, player):
        if(self.beenThere == False):#If you have not been here...
            player.inventory.append(self.item)#Add item to player inventory
            #player.visitList.append([set(player.location_x, player.location_y.y)])
 
    def modify_player(self, player):
        self.add_loot(player)
        #self.visitList += [player.location_x, player.location_y]

    #def addVisited(self, player):
        #self.visitList += [player.location_x, player.location_y]


class HealthRoom(MapTile):#Super to PotionRoom, ...
    def __init__(self, x, y, health):
        self.health = health
        super().__init__(x, y)
 
    def add_hp(self, player):
        player.hp += self.health
        print("HP is {}".format(player.hp))
 
    def modify_player(self, player):
        self.add_hp(player)

class PotionRoom(HealthRoom):
    def __init__(self, x, y):
        super().__init__(x, y, 25)#25 hp potion

    def intro_text(self):
        return """
        You find a bottle and drink the purple potion.
        You gained 25 HP!

    /***\ 
   /^^^^^\ 
  /       \ 
 < POTION  > 
  \       / 
   \     /
    \___/
   

        """



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

            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))
 
    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()

class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
 
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
        super().__init__(x, y, items.Dagger())

 
    def intro_text(self):
        if self.beenThere:
            return """
            You have been here before...
            This is where you found a dagger!
            """
        else:
            self.beenThere = True
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