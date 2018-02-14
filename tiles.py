import items, enemies, actions, world, random, sounds, module1
from player import Player
import time
 
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #Added player because player inventory affects some entry text
    def intro_text(self, player):
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
        moves.append(actions.Equip())
        return moves

class StartingRoom(MapTile):
    # override the intro_text method in the superclass
    def intro_text(self, player):

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
            sounds.good()
            player.inventory.append(self.item)#Add item to player inventory
            self.beenThere = True
 
    def modify_player(self, player):
        self.add_loot(player)

class HealthRoom(MapTile):#Super to PotionRoom, ... maybe fountain room
    def __init__(self, x, y, health, beenThere):
        self.health = health
        self.beenThere = False
        super().__init__(x, y)
 
    def add_hp(self, player):
        #Add room's health to player health.
        player.hp += self.health
        #hp can't be higher than max hp.
        if player.hp > player.maxHp:
            player.hp = player.maxHp
        time.sleep(1)
        print("HP is {}\n".format(player.hp))
        time.sleep(1)
 
    def modify_player(self, player):
        self.add_hp(player)

class PotionRoom(HealthRoom):
    def __init__(self, x, y):
        super().__init__(x, y, 25, beenThere = False)#25 hp potion

    def intro_text(self, player):
        if self.beenThere:
            return "\nBroken glass crunches under your feet.\
                    \nThis is the room you found the potion.\n"
              
        else:
            self.beenThere = True
            print( """\n   /***\\""")
            time.sleep(.5)
            print( """  /^^^^^\\""") 
            time.sleep(.5)
            print( """ /       \\""")
            time.sleep(.5)
            print( """< POTION  >""")
            time.sleep(.5)
            print( """ \       /""")
            time.sleep(.5)
            print( """  \     /""")
            time.sleep(.5)
            print( """   \___/\n""")
            time.sleep(1)
            print('You found a bottle and you drink the purple potion.\n')
            sounds.drink()
            time.sleep(1)
            print('You smash the bottle.')
            sounds.breakGlass()
            time.sleep(1)

            if (self.health + player.hp) > player.maxHp:
                if (player.hp) >= player.maxHp:
                    return """
                    HP already full!
                    """
                return """
                    You gained {} HP!
                    """.format(player.maxHp - (player.hp) )

            return """
                You gained 25 HP!
                """
                

                    


class VendorRoom(LootRoom):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y, item, beenThere = False)
 
    def add_loot(self, player):
        player.inventory.append(self.item)

    def take_loot(self, player, itemIndex):
        del player.inventory[itemIndex]

    def take_money(self, player):
        player.money -= self.item.value

    def add_money(self, player, itemIndex):
        player.money += player.inventory[itemIndex].value
 
    def modify_player(self, player):

        sell = input("\nDo you have any items you would like to sell?(y/n): ")
        print("")

        if sell == "y" or sell == "Y":
            for item in player.inventory: 
                print(player.inventory.index(item),".", item.name + " - $" + str(item.value));
            print(len(player.inventory),".", "Nevermind")
      
            while True:
                try:
                    itemChoice = int(input("\nSelect the item you would like to sell: "))
                except ValueError:#Catch exception if input isn't int
                    print("\nInvalid item choice")
                    sounds.no()
                    module1.getIntInput()
                    continue#Restart loop
                if itemChoice not in range(0,len(player.inventory)+1):#+1 for nevermind choice
                    print("\nInvalid item choice")
                    sounds.no()
                    continue#Restart loop
                break#Passed validation break infinite loop

            if itemChoice == len(player.inventory):
                print("\nThanks anyway\n")
                return#Nevermind was selected
            else:
                print("\nYou sold {} for {} moneys\n".format(player.inventory[itemChoice].name\
                    , player.inventory[itemChoice].value))

                self.add_money(player, itemChoice)
                self.take_loot(player, itemChoice)

                print("\nYou have {} moneys\n".format(player.money))
        else:
            print("\nThanks anyway\n")

        #if player.money >= self.item.value:
        #    print("Would you like to buy the {}?".format(self.item))
        #    self.add_loot(player)
        #    player.money -= self.item.value
        #else:
        #    print("You don't have enough money to buy the {}?".format(self.item))

class OldManVendorRoom(VendorRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Slingshot)
 
    def intro_text(self, player):
        return """
        You find an old man looking to purchase some items.
        """



class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            #r makes enemy take off between 75% and 125% of damage.
            r=random.randint(int(self.enemy.damage *.75), int(self.enemy.damage*1.25))
            the_player.hp = the_player.hp - r

            if the_player.hp < 0:#No negative hp
                the_player.hp = 0

            print("Enemy does {} damage. You have {} HP remaining\n"
                  .format(r, the_player.hp))
 
    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()

class EmptyCavePath(MapTile):
    def intro_text(self, player):
        #Random intro text for each empty cave room.
        text = []
        text.append( "\nAnother unremarkable part of the cave. You must forge onwards.\n")
        text.append("\nThis room is dark and empty.\n")
        text.append("\nThere isn't much going on in this room.\n")
        r = random.randint(0, len(text)-1)
        return text[r]
 
    def modify_player(self, player):
        #Room has no action on player
        pass
 
class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())
 
    def intro_text(self, player):
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
 
    def intro_text(self, player):
        if self.enemy.is_alive():
            sounds.hellhound()
            return """
            A massive flaming dog growls angrily as you enter his lair.  
            """
        else:
            return """
            A Hellhound corpse.  How did I ever manage to kill that thing?
            """

class BearRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Bear())
 
    def intro_text(self, player):
        if self.enemy.is_alive():
            sounds.bear()
            return """
            A gigantic grizzly bear wants to eat you for lunch.  
            """
        else:
            return """
            Here's that dead grizzly.
            """

class RatHumanoidRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.RatHumanoid())
 
    def intro_text(self, player):
        if self.enemy.is_alive():
            sounds.ratHumanoid()
            return """
            A Rat Humanoid, oh my!.  
            """
        else:
            return """
            Here's the slain rat man.
            """

class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ogre())
 
    def intro_text(self, player):
        if self.enemy.is_alive():
            sounds.ogre()
            return """
            Oh shit an ogre.  
            """
        else:
            return """
            Here's that dead ogre.
            """
 
class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
       #self.beenThere = False
        super().__init__(x, y, items.Dagger(), beenThere = False)


 
    def intro_text(self, player):
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

class ChestRoom(LootRoom):
    def __init__(self, x, y, item, key, gotKey, beenThere, gotBox):
        self.item = item
        self.key = key;
        self.gotKey = False
        self.beenThere = False#Whether player has been in this room
        self.gotBox = False
        super().__init__(x, y, item, beenThere)
 
    def add_loot(self, player):
        if(player.checkInventory(self.key)):
            self.gotKey = True
            player.inventory.append(self.item)#Add item to player inventory
            self.gotBox = True;
            self.beenThere = True
 
    def modify_player(self, player):
        self.add_loot(player)

class SkullChestRoom(ChestRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Crossbow(), beenThere = False,\
               key = items.SkullKey(), gotBox = False, gotKey = False)

    def intro_text(self, player):
        self.gotKey = player.checkInventory(self.key)
        if self.beenThere and not self.gotBox:
            return """
            The chest with the skull shaped key is still locked.
            """
        elif self.beenThere and self.gotBox:
            return """
            You see the empty chest where you found the {}
            """.format(self.item)
        elif self.gotKey and not self.gotBox:
            sounds.chestOpen()
            self.gotBox = True
            return """
                    You see a chest with a skull keyhole.
                    You use the skull key and open the chest.
                    You obtained a {}.
                    """.format(self.item) 
        else: 
            return"""
            You find an old chest, the keyhole is shaped like a skull.
            It's locked.
            """

class BlueChestRoom(ChestRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Moltov(), beenThere = False,\
               key = items.BlueKey(), gotBox = False, gotKey = False)

    def intro_text(self, player):
        self.gotKey = player.checkInventory(self.key)
        if self.beenThere and not self.gotBox:
            return """
            The blue chest is still locked.
            """
        elif self.beenThere and self.gotBox:
            return """
            You see the empty blue chest where you found the {}
            """.format(self.item)
        elif self.gotKey and not self.gotBox:
            sounds.chestOpen()
            self.gotBox = True
            return """
                    You see a blue chest.
                    You use the blue key and open the chest.
                    You obtained a {}.
                    """.format(self.item) 
        else: 
            return"""
            You find a blue chest, the keyhole is shaped like a skull.
            It's locked, maybe you need a blue key.
            """

#class KeyRoom(LootRoom):
#    def __init__(self, x, y, item, key, beenThere):
#        self.item = item
#        self.key = key;
#        self.beenThere = False
#        super().__init__(x, y)
 
#    def add_loot(self, player):
#        if(self.beenThere):#If you have not been here...  
#            player.inventory.append(self.item)#Add item to player inventory
#            self.beenThere = True
 
#    def modify_player(self, player):
#        self.add_loot(player)

class SkullKeyRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.SkullKey(), beenThere = False)

    def intro_text(self, player):
        if self.beenThere:
            return """
            your in the room where you found the skull key
            """
        else:
            return"""
            You find a key shaped like a skull
            """

class BlueKeyRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.BlueKey(), beenThere = False)

    def intro_text(self, player):
        if self.beenThere:
            return """
            your in the room where you found the blue key
            """
        else:
            return"""
            You find a blue key
            """

           
class LeaveCaveRoom(MapTile):
    def intro_text(self, player):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        player.victory = True

class LeaveCaveRoomEntrance(ChestRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Crossbow(), beenThere = False,\
               key = items.FinalKey(), gotBox = False, gotKey = False)

    def available_actions(self):
        """Returns all of the available actions in this room."""
        
        moves = [actions.MoveSouth()]#Can always go back south
        if self.gotBox: # Door unlocked
            moves.append(actions.MoveNorth())#North to boss

        moves.append(actions.ViewInventory())
        moves.append(actions.Equip())
        

        return moves

    def modify_player(self, player):
        self.beenThere = True
        self.gotKey = player.checkInventory(self.key)
        if self.gotKey:
            self.gotBox = True#Door unlocked

    def intro_text(self, player):
        self.gotBox = player.checkInventory(self.key)
        if self.gotBox:
            if self.beenThere:
                return """
                        Do you dare enter the unlocked door?
                        """
            sounds.chestOpen()#Will be door open
            self.gotBox = True#Door unlocked
            return """
                    You unlocked the metal door to travel northward.
                    Something seems off.
                    Continue at your own risk.

                    """
        else: 
            return"""
                There is a thick metal door, must be guarding something.
                There is a keyhole.
                """
