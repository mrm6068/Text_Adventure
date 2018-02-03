import items, world, random, time
 
class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Pillow()]
        self.hp = 100
        self.maxHp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False
        self.experience = 0
        self.level = 1
        self.money = 0
        self.nextLevelUp = 10
 
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
        print('\n')
        for item in self.inventory:
            print(item, '\n')
            time.sleep(2)#Show 1 at a time.
    
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
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:#Loops through inventory to find best weapon.
         if isinstance(i, items.Weapon):
            if i.minDamage > max_dmg:
                #r=random.randint(i.minDamage, i.maxDamage)
                max_dmg = i.minDamage
                best_weapon = i

        print("\nYou use {} against {}\n".format(best_weapon.name, enemy.name))
        #rolls a random int between min and max damage of weapon (in items class)
        r=random.randint(i.minDamage, i.maxDamage)
        time.sleep(1)
        print("{} lost {} HP\n".format(enemy.name, r)) #prints out how much damage it rolled
        time.sleep(1)
        enemy.hp -= r #takes away the rolled integer between damage range

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
            print("Total XP is {}\n".format(self.maxHp))
            time.sleep(2)
            print("Next level up at {} XP\n".format(self.nextLevelUp))
            time.sleep(2)

    def do_action(self, action, **kwargs):
     action_method = getattr(self, action.method.__name__)
     if action_method:
                action_method(**kwargs)

    def flee(self, tile):
        """Moves the player randomly"""
        available_moves = tile.adjacent_moves()
        r=random.randint(0, len(available_moves)-1)#Added -1 which i think fixed fleeing crash index out of range
        self.do_action(available_moves[r])

    #Needed to check for key when chestRoom reached
    def checkInventory(self, item):
        for _item in self.inventory:
            #check inventory for instance of passed item(key)
            if isinstance(_item, item.__class__):
                return True
        return False


