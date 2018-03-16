import items, enemies, actions, world, random, sounds, util
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
        moves.append(actions.Status())
        moves.append(actions.Heal())
        return moves

class StartingRoom(MapTile):

    # override the intro_text method in the superclass
    def intro_text(self, player):


        return """
        The Year is 2045, the world has entered the second ice age for over
        200 years. Forced to retreat into the underground, humanity has lived
        on scrapping by. Recently a plague has swept through humanity from 
        the poor conditions of living underground. Lately, scientist has 
        discovered something interesting…. Rats have evolved to being able 
        to live in the world’s harsh conditions and are immune to the plague. 
        In a secret government base, Dr. Beaumont Liston has been testing for
        years to make the perfect humanoid, performing test on live humans and
        animals mixing their DNA and forcing them to live in the cold and how 
        they survive. You are the next test subject to be the perfect rat 
        humanoid which is believed to be able to live in the world and immune
        to the disease. Tests have also been able to enhance the body and mind
        once perfected to create the ultimate being……  until something happened
        and all the subjects are released in the compound. You wake up to 
        monsters running all around the place, your only task… survive.


        Woman: Hello….? please wake up!!! It’s not safe to lay here. We must 
                leave this place
        You: Wh-where am I? Who are you?
        Woman: My name is Amelia, I am here trying to find my Daughter, 
                Elizabeth…. She’s only 13 years old and there are monsters 
                running rampant in this place. Please you have to help me 
                find her!
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

class PortalRoom(MapTile):
    def __init__(self, x, y, xChange, yChange, wentThrough = False):
        self.xChange = xChange
        self.yChange = yChange
        super().__init__(x, y)
 
    def modify_player(self, player):
        player.location_x += xChange
        player.location_y += yChange

def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.Equip())
        moves.append(actions.Status())
        moves.append(actions.Heal())
        return moves



class PortalOne(PortalRoom):
    def __init__(self, x, y):
       #self.beenThere = False
        super().__init__(x, y, xChange = 2, yChange = 0, wentThrough = False)
    def intro_text(self, player):
        if self.wentThrough:
            return """
            The portal took you to a different room with another portal.
            """
        else:
            return """
            There is a portal.
            """

            return """
            Your notice something shiny in the corner.
            It's a dagger! You pick it up.
            """

class HealthRoom(MapTile):#Super to PotionRoom, ... maybe fountain room
    def __init__(self, x, y, health, beenThere = False):
        self.health = health
        self.beenThere = False
        super().__init__(x, y)
 
    def add_hp(self, player):
        if not self.beenThere:
            self.beenThere = True
            #Add room's health to player health.
            player.hp += self.health
            #hp can't be higher than max hp.
            if player.hp > player.maxHp:
                player.hp = player.maxHp
            util.printGameText("HP is {}\n".format(player.hp))
            util.pause()
 
    def modify_player(self, player):
        self.add_hp(player)

class AmeliaRoom(HealthRoom):
    def __init__(self, x, y):
        super().__init__(x, y, 50, beenThere = False)

    def intro_text(self, player):
        util.printGameText("\nYou see a nurse. She uses her nursing skills to heal you.\n")
              
        util.ameliaGraphic()

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

class PotionRoom(HealthRoom):
    def __init__(self, x, y):
        super().__init__(x, y, 25, beenThere = False)#25 hp potion

    def intro_text(self, player):
        if self.beenThere:
            return "\nBroken glass crunches under your feet.\
                    \nThis is the room you found the potion.\n"
              
        else:
            util.potionGraphics()

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
                
class SmallPotionRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.SmallPotion(), beenThere = False)

    def intro_text(self, player):
        if self.beenThere:
            return """
            your in the room where you found the small potion
            """
        else:
            return"""
            You find a small potion                           
            You put it in your bag
            """
                    


class VendorRoom(LootRoom):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y, item, beenThere = False)
 
    def add_loot(self, player):
        player.inventory.append(self.item)

    def give_loot(self, player, itemIndex):
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
                itemChoice = util.getIntInput("\nSelect the item you would like to sell: ")
        
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
                self.give_loot(player, itemChoice)

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
        super().__init__(x, y, items.Slingshot())
 
    def intro_text(self, player):
        return """
        You find an old man looking to purchase some items.
        """

#class LootRoom(MapTile):
#    def __init__(self, x, y, item, beenThere):
#        self.item = item
#        self.beenThere = False
#        super().__init__(x, y)
 
#    def add_loot(self, player):
#        if(self.beenThere == False):#If you have not been here...  
#            sounds.good()
#            player.inventory.append(self.item)#Add item to player inventory
#            self.beenThere = True
 
#    def modify_player(self, player):
#        self.add_loot(player)

class SellerRoom(MapTile):
    def __init__(self, x, y, item):
        self.item =[items.Moltov(),  items.Crossbow(), items.SmallPotion()]
        super().__init__(x, y)
 
    def add_loot(self, player, item):
        player.inventory.append(item)

    def give_money(self, player, value):
        player.money -= value
 
    def modify_player(self, player):

        sell = input("\nCan I interest you in purchasing any items?(y/n): ")
        print("")

        if sell == "y" or sell == "Y":
            for item in self.item: 
                print(self.item.index(item),".", item.name + " - $" + str(item.value));
            print(len(self.item),".", "Nevermind")
      

            while True:
                itemChoice = util.getIntInput("\nSelect the item you would like to buy: ")
                

                if itemChoice not in range(0,len(self.item)+1):#+1 for nevermind choice
                    print("\nInvalid item choice")
                    sounds.no()
                    continue#Restart loop

                if itemChoice == len(self.item):
                    break#needed to skip index out of range in next if.

                #Not enough money
                if self.item[itemChoice].value > player.money:
                    print("\nNot enough money, sorry")
                    sounds.no()
                    continue#Restart loop
                break#Passed validation break infinite loop

            if itemChoice == len(self.item):
                print("\nThanks anyway\n")
                return#Nevermind was selected
            else:
                print("\nYou bought {} for {} moneys\n".format(self.item[itemChoice].name\
                    , self.item[itemChoice].value))
                
                self.add_loot(player, self.item[itemChoice])
                self.give_money(player, self.item[itemChoice].value)
                # if item is a potion
                if isinstance(itemChoice, items.Potions):#If item is a potion...
                    itemChoice.amt = itemChoice.amt + 1 #Add one to the amount 
                del self.item[itemChoice]#Seller won't have this anymore

                print("\nYou have {} moneys\n".format(player.money))
        else:
            print("\nThanks anyway\n")

class LadySellerRoom(SellerRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Slingshot())
 
    def intro_text(self, player):
        return """
        An attractive woman with some items for sale.
        """


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            #r makes enemy take off between 75% and 125% of damage.
            r=random.randint(int(self.enemy.damage *.75), int(self.enemy.damage*1.25))
            #If player has armor, cut damage in half.
            if the_player.armor:
                r = int(r / 2)
                the_player.armorHits += 1
                if(the_player.armorHits > 15):
                    the_player.armorHits = 0
                    the_player.armor = False
                    print("Your armor is toast\n")
                    
            the_player.hp = the_player.hp - r

            if the_player.hp < 0:#No negative hp
                the_player.hp = 0

            print("Enemy does {} damage. You have {} HP remaining\n"
                  .format(r, the_player.hp))
 
    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), 
                    actions.Attack(enemy=self.enemy), 
                    actions.Equip(),
                    actions.Heal()]
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

class ArmorRoom(MapTile):
    def intro_text(self, player):
        return """
        You find armor made of mythril, you put it on.\n\
        Damage you take will be halved for 15 hits
        """

    def modify_player(self, player):
        player.armor = True
 
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
            
            return """
        **You walk into the lab and notice Elizabeth strapped up to a machine. 
        There are needles in her and are draining her body of her blood**

        You: Amelia!!! Stop this now!!!
        Amelia: I’ve worked too long and too hard to be pulled down by anyone 
        who does not believe in my methods. This is the way of life! One must 
        sacrifice to save the lives of millions! I only need a sample of her 
        blood to perfect my experiment! Elizabeth’s body is born immune of the 
        disease and in her DNA is the genes used to allow for the rat DNA to 
        be accepted into the body and work properly. 

        You: No one wants to be turned into a rat! This isn’t the way!

        Amelia: Then those who deny me will die. Our bodies will be able to
        withstand the cold, immune to disease. I will open up a new chapter 
        in human history!

        **Amelia pulls a sample of the perfected formula 
                     and injects it into her body**

        Amelia: The formula only works if the body is under extreme conditions. 
        Here, I can expose myself to the harsh cold and my body will react.

        **She presses a button and the roof opens up and lets in the extreme 
        cold. You feel it chilling your very bones. Her body begins to react, 
        growing more and more hair. Her face begins to grow a long snout and 
        her teeth grow razor sharp. Her eyes glow red as she hunches over on 
        all fours. Her Muscles seem abnormally large and she is ready to fight**

        Amelia: This is what the new face of humanity will look like and you 
        will experience first hand what I can do.
        """

            sounds.ratHumanoid()
        else:
            return """
            
            """

class BatRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Bats())
 
    def intro_text(self, player):
        if self.enemy.is_alive():
            #sounds.bats();
            return """
            In the dark cave, you hear small clicks. Before long, you somehow found yourself surrounded by many small bats, all of them looking towards you. 
			The many years of pollution and evolution have made them more aggressive to the new inhabitants it now has to share their habitats with 
			and now they seek to vent their frustration on you! 
			You ready your weapon to intercept any bats coming towards you.
            """
        else:
            return """
            The bats that were in this area have now dispersed. The bats that were too slow or unlucky litter the floor.
            """


class ZombieRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Zombie())
 
    def intro_text(self, player):
        if self.enemy.is_alive():
            #sounds.zombie()
            return """
            As you continue to walk in this direction, you slow down as you hear a dragging 
			noise across the ground. Soon, a shambling corpse can be seen around the corner, 
			and it starts groaning as it continues to shamble and turns toward you with its 
			lifeless eyes. This must have been another failed experiment. You ready your weapon. 
            """
        else:
            return """
            As you walk over the corpse and try not to notice it still twitching, it white eyes still stare blankly at the ceiling.
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

class CrawlerRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Crawler())
 
    def intro_text(self, player):
        if self.enemy.is_alive():
            return """
            Walking along this path, you suddenly feel a chill creep up your spine. 
            You then notice a crawling figure's shadow before you see a horrendously 
            mutated figure with many appendages with sharp claws on its back propped 
            on the ceiling. It defly lands on  the ground on its four muscular limbs 
            it used to prop itself on the celing..  
            """
        else:
            return """
            The dead abomination that could scale walls...
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
            util.dagRoomGraphic()

            return """
            You notice something shiny in the corner.
            It's a dagger! You pick it up.
            """

class FindTundrasEndRoom(LootRoom):
    def __init__(self, x, y):
       #self.beenThere = False
        super().__init__(x, y, items.TundrasEnd(), beenThere = False)


 
    def intro_text(self, player):
        if self.beenThere:
            return """
            You have been here before...
            This is where you found that massive sword!
            """
        else:
            

            return """
            In the center of the room is a massive sword on a pedestal..
            As you pick it up, it feels almost as if the sword has been
            waiting for you.....
            """

class FindLargeHammer(LootRoom):
    def __init__(self, x, y):
       #self.beenThere = False
        super().__init__(x, y, items.LargeHammer(), beenThere = False)


 
    def intro_text(self, player):
        if self.beenThere:
            return """
            You have been here before...
            This is where you found that hammer!
            """
        else:
            

            return """
            Over in the corner of the room you spot a massive mallet..
            Probably a good idea to hit things with this.
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
        You’ve beaten Amelia and as her body lays still on the ground, you walk over to 
        Elizabeth to free her from the machine. She is still breathing and wakes up to 
        her in your arms. She hugs you and thanks you for saving her. You carry her out 
        of the laboratory but hear something move. You look over at Amelia’s body and 
        its not there. You turn around and see her standing in front of you. You reach 
        for your small dagger and thrust it into her heart…… but not before she drives 
        her claws into your chest. As death creeps up on you and you can feel your 
        last breath being drawn, you give Elizabeth a map and prompt her to go to your 
        family’s place where you lived. You tell her she will be safe there and to 
        leave you here. As she runs away crying, you have a smile on your face. 
        “I guess Amelia was right” you say. “It takes the sacrifice of one to 
        save millions.” 
        
        You close your eyes and embrace your frozen grave.
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

class StoryRoom1(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.blank(), beenThere = False)

    #override the intro_text method in the superclass
    def intro_text(self, player):

        if self.beenThere:
            return """
            This room looks familiar...
            """
        
        else:
            return """
            You: What are you doing here? In a place like this? 
            Amelia: My daughter and I were bought here unwillingly by the government. 
            Dr. Beaumont Liston wanted to preform experiments on my daughter, 
            saying she was special. That she was the key to saving humanity. 
            But I saw what he’s done, He only creates monsters and I wasn’t having it.
            """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class StoryRoom2(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.blank(), beenThere = False)

    #override the intro_text method in the superclass
    def intro_text(self, player):

        if self.beenThere:
            return """
            This room looks familiar...
            """

        else:
            return """
            You: What are these creatures?
            Amelia: These are Dr. Liston’s creations. 
            For years he tested the genetics of humans and animals, trying to create 
            the ultimate being for the new world by mixing DNA.  These are all his failures. 
            He takes them and locks them away to die.
            You: I guess they are pretty pissed about it huh?
            """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class StoryRoom3(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.blank(), beenThere = False)

    # override the intro_text method in the superclass
    def intro_text(self, player):

        if self.beenThere:
            return """
            This room looks familiar...
            """

        else:
            return """
            You: Do you know where Elizabeth could be?
            Amelia: Dr. Liston was planning to do an operation on her. 
            She was so scared but when the place went downhill, 
            she ran away and locked herself in the North-West corridor. She must be there.
            """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class StoryRoom4(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.blank(), beenThere = False)

    # override the intro_text method in the superclass
    def intro_text(self, player):

        if self.beenThere:
            return """
            This room looks familiar...
            """

        else:
            return """
            You: Why do you know so much about this place?
            Amelia: I used to work here as a nurse, tending to the patients when 
            Dr. Liston finished working on them.
            """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class StoryRoom5(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.blank(), beenThere = False)

    # override the intro_text method in the superclass
    def intro_text(self, player):

        if self.beenThere:
            return """
            This room looks familiar...
            """

        else:
            return """
            **Doctor Liston’s body lays on the ground**
            You: He’s…. Dead? But how?
            Amelia: He was probably attacked by something he created. Serves him right.
            You: I don’t think so……He was shot.
            Amelia: Shot….. he was a monster anyways. Leave him, we must press onwards...
            **Amelia walks away**
            Voice:                          wait…..
            You: Dr. Liston? 
            Liston: She is Lying to you….. She’s the reason you’re here… don’t let her… get….. Elizabeth…..
            **Listion Dies (again)**
            You start to wonder if you should be helping her….
            """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class StoryRoom6(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.blank(), beenThere = False)

    # override the intro_text method in the superclass
    def intro_text(self, player):

        if self.beenThere:
            return """
            This room looks familiar...
            """
        else:
            return """
            Amelia: Just up ahead is my daughter. She must be so scared, but I will take care of her.
            You: I hope you are ensuring her safety.
            Amelia: She’s my Daughter, I only want what’s best for her.
            You: ………
            """
 
    def modify_player(self, player):
        #Room has no action on player
        pass


class StoryRoom7(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.blank(), beenThere = False)

    # override the intro_text method in the superclass
    def intro_text(self, player):

        if self.beenThere:
            return """
            This room looks familiar...
            """

        else:
            self.beenThere = True
            return """
            Amelia: Elizabeth! Come here, my child.
            Elizabeth stands there shaking...
            Amelia: Did you not hear me? Come here!
            Elizabeth: NO! You killed my father and now you want to kill me for your stupid experiments!
            You: What? Who is her father?
            Amelia: Don’t listen to this child, she knows nothing!
            Elizabeth: Dr. Liston! He was my dad and she shot him for wanting to save me from this woman! 
                       She wants to take my heart out to complete and mass produce her rat formula.
            You: I thought she was your daughter! You lied about everything!
            Amelia: ... You know, I thought you would be smart enough to see who’s in the right here. 
                        But obviously you want to share a similar fate as that man.
            **Amelia draws a gun and fires at you, you barely dodge it as the bullet grazes your arm. 
            Amelia then pulls out a taser and hits Elizabeth. She grabs her and runs away. 
            You can hear Elizabeth’s screams coming from the far north end of the compound.**
            I have to go save Elizabeth!
            """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class StoryRoomFinal(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.blank(), beenThere = False)

    # override the intro_text method in the superclass
    def intro_text(self, player):

        if self.beenThere:
            return """
            This room looks familiar...
            """

        else:
            return """
            **You walk into the lab and notice Elizabeth strapped up to a machine. 
            There are needles in her and are draining her body of her blood**

            You: Amelia!!! Stop this now!!!
            Amelia: I’ve worked too long and too hard to be pulled down by anyone 
            who does not believe in my methods. This is the way of life! One must 
            sacrifice to save the lives of millions! I only need a sample of her 
            blood to perfect my experiment! Elizabeth’s body is born immune of the 
            disease and in her DNA is the genes used to allow for the rat DNA to 
            be accepted into the body and work properly. 

            You: No one wants to be turned into a rat! This isn’t the way!

            Amelia: Then those who deny me will die. Our bodies will be able to
            withstand the cold, immune to disease. I will open up a new chapter 
            in human history!

            **Amelia pulls a sample of the perfected formula 
                         and injects it into her body**

            Amelia: The formula only works if the body is under extreme conditions. 
            Here, I can expose myself to the harsh cold and my body will react.

            **She presses a button and the roof opens up and lets in the extreme 
            cold. You feel it chilling your very bones. Her body begins to react, 
            growing more and more hair. Her face begins to grow a long snout and 
            her teeth grow razor sharp. Her eyes glow red as she hunches over on 
            all fours. Her Muscles seem abnormally large and she is ready to fight**

            Amelia: This is what the new face of humanity will look like and you will experience first hand what I can do.
            """
 
    def modify_player(self, player):
        #Room has no action on player
        pass