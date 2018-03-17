import items, sounds, world, random, time, tiles, actions, util
from world import tile_exists
from util import printGameText

class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Pillow(), items.SmallPotion(), items.SmallPotion(), items.SmallPotion()]
        self.hp = 100
        self.maxHp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False
        self.experience = 0
        self.level = 1
        self.money = 30
        self.attackPower = 100
        self.nextLevelUp = 10
        self.chosenWpn = None
        self.armor = False
        self.armorHits = 0
        self.currentWpn = self.inventory[1]
 
    def hasVisited(self):
        if ([self.location_x, self.location_y]) in player.visitList:
            return True
            print("True" + self.visitList)
        else:
            return False
            print("false" + self.visitList)



    def is_alive(self):
            return self.hp > 0
        
 

    def print_inventory(self):
         print("This is what you have so far from your travels.\n")
         for item in self.inventory:
             print(item, '\n\n')
             #if not isinstance(item, items.Weapon):
             #   print(item, '\n')
         print("\nCurrently you brandish your trusty", self.currentWpn.name, "in your hands.\n")
         print("\nYou currently have {} gold coin\n".format(self.money))
                
    def status(self):
        util.printGameText("You are level {}\n".format(self.level))
        print(" * Current HP: {} /".format(self.hp), "{}\n".format(self.maxHp))
        print(" * Attack Power: {}\n".format(self.attackPower))
        print(" * Total XP: {}\n".format(self.experience))
        print(" * XP until next level up: {} XP\n".format(self.nextLevelUp - self.experience))
        util.pause()

    def item_choose(self, item_class):
        self.item_class = item_class
        item_list = []
        for item in self.inventory: 
            if isinstance(item, items.item_class):#If item is this class...
                item_list.append(item)#Add it to item_list
        for item in item_list:
            print(item_list.index(item) ,".", item_class.name, sep='')

    def heal(self):
        print("\nThese are the potions you currently possess.\n")
        potion_list = []
        #item_choose(self, items.Potions)
        for potion in self.inventory: 
            if isinstance(potion, items.Potions):#If item is this class...
                if potion.amt <= 0:
                    self.inventory.remove(potion)
                    continue #skips this potion which you have none of
                else:
                    potion_list.append(potion)#Add it to item_list
        i=1
        for potion in potion_list:
            print(i,". ", potion.name, sep='')
            i+=1
        while True:
            if len(potion_list) == 0:
                print("You have no potions.")
                util.pause()
                return None #no potions, get out of method

            itemChoice = util.getIntInput("""\nSelect a potion: """) - 1

            if itemChoice not in range(0,len(potion_list)):
                print("\nInvalid choice")
                sounds.no()
                continue#Restart loop
            break#Passed validation break infinite loop

        self.healToPlayer(itemChoice, potion_list)


    def healToPlayer(self, itemChoice, potionList): #logic for healing player
        chosenPotion = potionList[itemChoice]
        util.printGameText("\nYou were healed for {} ".format(chosenPotion.health))
        util.printGameText("hp. \n")
        self.hp = self.hp + chosenPotion.health
        chosenPotion.amt = chosenPotion.amt - 1
        if chosenPotion.amt == 0:
            self.inventory.remove(chosenPotion)
        sounds.drink()
        util.pause()
        if self.maxHp < self.hp:
            self.hp = self.maxHp


    def equip(self):
        print("\nThese are the weapons you currently possess.\n")

        weapon_list = []
        for item in self.inventory: 
            if isinstance(item, items.Weapon):#If item is weapon...
                weapon_list.append(item)#Add it to weapon_list
        i = 1
        for weapon in weapon_list:
            print(i,". ", weapon.name, sep='')
            i+=1
        #input validation to get int from user in proper range
        while True:

            itemChoice = util.getIntInput("""\nSelect the weapon you want to equip: """) - 1

            if itemChoice not in range(0,len(weapon_list)):
                print("\nInvalid weapon choice")
                sounds.no()
                continue#Restart loop
            break#Passed validation break infinite loop

        print('\n')
        print(weapon_list[itemChoice].name, "equipped.\n")
        self.currentWpn = weapon_list[itemChoice]

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        util.printGameText(world.tile_exists(self.location_x, self.location_y).intro_text(self))
        print()
 
    def move_north(self):
        self.move(dx=0, dy=-1)
 
    def move_south(self):
        self.move(dx=0, dy=1)
 
    def move_east(self):
        self.move(dx=1, dy=0)
 
    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
    
        self.currentWpn.sound()

        print("\nYou use {} against {}\n".format(self.currentWpn.name, enemy.name))
        r=random.randint(self.currentWpn.minDamage, self.currentWpn.maxDamage)
        time.sleep(1)

        print("{} lost {} HP\n".format(enemy.name, r))
        time.sleep(1)
        #player attackPower starts at 100, gets stronger when level up
        enemy.hp -= int((r*(self.attackPower/100)))

        #Check if weapon is projectile to subtract 1 ammo each attack
        if isinstance(self.currentWpn, items.Projectile):
            self.currentWpn.ammo -= 1
            if self.currentWpn.ammo > 0:
                print("\n{} has {} shots left\n".format\
                    (self.currentWpn.name, self.currentWpn.ammo))
            else:
                #Don't print out of ammo for Moltov
                if not isinstance(self.currentWpn, items.Moltov):
                    print("\n{} is out of ammo, you toss it away.\n".format(self.currentWpn.name))
                print("\nSelect a new weapon.\n")
                self.inventory.remove(self.currentWpn)
                self.equip()
                
        if not enemy.is_alive():
            print("You killed {}!\n".format(enemy.name))
            time.sleep(.5)
            self.experience += enemy.experience
            print("You gained {} XP\n".format(enemy.experience))
            time.sleep(.5)
            print("Total XP = {} \n".format(self.experience))
            time.sleep(.5)

            #Check for level up
            Player.checkLevelUp(self)

        else:
            time.sleep(.5)
            util.printGameText("{} HP is {}\n".format(enemy.name, enemy.hp))
            time.sleep(.5)

    def checkLevelUp(self):
        if self.experience >= self.nextLevelUp:
                self.level += 1#Level up
                self.nextLevelUp *= 2 #Will get harder to level up each level.
                self.maxHp = int(self.maxHp * 1.20)#Max HP increases 20% per level
                self.attackPower = int(self.maxHp * 1.10)
                util.printGameText("\n\n* * * * * * * * * * *\n")
                util.printGameText("You've reached level {}!".format(self.level))
                util.printGameText("\n* * * * * * * * * * *\n\n")
                sounds.levelUp()
                time.sleep(1)
                print(" * Max HP increased to {}\n".format(self.maxHp))
                time.sleep(.5)
                print(" * Attack Power increased to {}\n".format(self.attackPower))
                time.sleep(.5)
                print(" * Total XP is {}\n".format(self.experience))
                time.sleep(.5)
                print(" * Next level up at {} XP\n".format(self.nextLevelUp))
                time.sleep(.5)
                self.checkLevelUp()#Recursively check for multiple level ups

    def do_action(self, action, **kwargs):
     action_method = getattr(self, action.method.__name__)
     if action_method:
                action_method(**kwargs)


    def flee(self, tile):
        """Moves the player randomly"""
        available_moves = tile.adjacent_moves()
        if isinstance(tile, tiles.RatHumanoidRoom):
            del available_moves[0]#Can't flee north from final boss

        r = random.randint(0, len(available_moves)-1)#Added -1 which i think fixed fleeing crash index out of range
        self.do_action(available_moves[r])

    #Needed to check for key when chestRoom reached
    def checkInventory(self, item):
        for _item in self.inventory:
            #check inventory for instance of passed item(key)
            if isinstance(_item, item.__class__):
                return True
        return False


