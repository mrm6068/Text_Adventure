import items
import world
import random
import time
 
class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Pillow(), items.Dagger(), items.Crossbow()]
        self.hp = 100
        self.maxHp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False
        self.experience = 0
        self.level = 1
        self.money = 30
        self.nextLevelUp = 10
        self.chosenWpn = None
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
        
 
    #def print_inventory(self):
    #    print('\n')
    #    for item in self.inventory:
    #        print(item, '\n')
    #        time.sleep(2)#Show 1 at a time.

    #def inventory_choice(self):
    #    while True:
    #            print("i: Inventory")
    #            print("e: Equip item")
    #            inventory_option = input()

    #            if inventory_option in ['i', 'e']:
    #                # will exit loop when choice is made
    #                break
    #            if inventory_option == 'i':
    #               return 'i'

    #            elif inventory_option == 'e':
    #                return 'e'
                              

    def print_inventory(self):
         print("This is what you have so far from your travels.")
         for item in self.inventory:
             print(item, '\n\n')
             #if not isinstance(item, items.Weapon):
             #   print(item, '\n')
         print("\nCurrently you brandish your trusty", self.currentWpn.name, "in your hands.\n")
                
    def equip(self):
        print("\nThese are the weapons you currently possess.\n")

        weapon_list = []
        for item in self.inventory: 
            if isinstance(item, items.Weapon):
                #n+=1
                #print(n, ".", item, '\n')
                weapon_list.append(item)
        for weapon in weapon_list:
            print(weapon_list.index(weapon),".", weapon.name)
        #print(len(weapon_list))
        self.chosenWpn = int(input("\nSelect the weapon you want to equip: "))
        #while self.chosenWpn < 0 or self.chosenWpn > len(weapon_list):
        #    self.chosenWpn = int(input("Select the weapon you want to
        #    equip."))
        if self.chosenWpn >= 0 and self.chosenWpn < len(weapon_list):
                print('\n')
                print(weapon_list[self.chosenWpn].name, "equipped.\n")
                self.currentWpn = weapon_list[self.chosenWpn]
        else:
            print("\nInvalid weapon chosen.\n")

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text(self))
 
    def move_north(self):
        self.move(dx=0, dy=-1)
 
    def move_south(self):
        self.move(dx=0, dy=1)
 
    def move_east(self):
        self.move(dx=1, dy=0)
 
    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        #best_weapon = None
        #max_dmg = 0
        #for i in self.inventory:#Loops through inventory to find best weapon.
        # if isinstance(i, items.Weapon):
        #    if i.damage > max_dmg:
        #        max_dmg = i.damage
        #        best_weapon = i
        #if self.currentWpn.minDamage > self.currentWpn.dmg:
        #       self.currentWpn.dmg = i.minDamage
        #       #best_weapon = i
        #       self.currentWpn = i
        
        print("\nYou use {} against {}\n".format(self.currentWpn.name, enemy.name))
        r=random.randint(self.currentWpn.minDamage, self.currentWpn.maxDamage)
        time.sleep(1)

        print("{} lost {} HP\n".format(enemy.name, r))
        time.sleep(1)
        enemy.hp -= r

        #Check if weapon is projectile to subtract 1 ammo each attack
        if isinstance(self.currentWpn, items.Projectile):
            self.currentWpn.ammo -= 1
            if self.currentWpn.ammo > 0:
                print("\n{} has {} shots left\n".format\
                    (self.currentWpn.name, self.currentWpn.ammo))
            else:
                print("\n{} is out of ammo, you toss it away.\n".format(self.currentWpn.name))
                print("\nSelect a new weapon.\n")
                self.inventory.remove(self.currentWpn)
                self.equip()
                



        if not enemy.is_alive():
            print("You killed {}!\n".format(enemy.name))
            time.sleep(2)
            self.experience += enemy.experience
            print("You gained {} XP\n".format(enemy.experience))
            time.sleep(2)
            print("Total XP = {} \n".format(self.experience))
            time.sleep(2)

            #Check for level up
            Player.checkLevelUp(self)

        else:
            time.sleep(2)
            print("{} HP is {}\n".format(enemy.name, enemy.hp))
            time.sleep(2)

    def checkLevelUp(self):
        if self.experience >= self.nextLevelUp:
                self.level += 1#Level up
                self.nextLevelUp *= 2 #Will get harder to level up each level.
                self.maxHp = int(self.maxHp * 1.10)#Max HP increases 10% per level
                print("You've reached level {}!\n".format(self.level))
                time.sleep(2)
                print("Max HP increased to {}\n".format(self.maxHp))
                time.sleep(2)
                print("Total XP is {}\n".format(self.experience))
                time.sleep(2)
                print("Next level up at {} XP\n".format(self.nextLevelUp))
                time.sleep(2)
                self.checkLevelUp()#Recursively check for multiple level ups

    def do_action(self, action, **kwargs):
     action_method = getattr(self, action.method.__name__)
     if action_method:
                action_method(**kwargs)


    def flee(self, tile):
        """Moves the player randomly"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)#Added -1 which i think fixed fleeing crash index out of range
        self.do_action(available_moves[r])

    #Needed to check for key when chestRoom reached
    def checkInventory(self, item):
        for _item in self.inventory:
            #check inventory for instance of passed item(key)
            if isinstance(_item, item.__class__):
                return True
        return False


