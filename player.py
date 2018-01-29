import items, world, random
 
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
        for item in self.inventory:
            print(item, '\n')
    
    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())
 
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
            if i.damage > max_dmg:
                max_dmg = i.damage
                best_weapon = i
 
        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        print("\n")
        enemy.hp -= best_weapon.damage

        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
            self.experience += enemy.experience
            print("You gained {} XP".format(enemy.experience))
            print("Total XP = {} ".format(self.experience))

            #Check for level up
            Player.checkLevelUp(self)

        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def checkLevelUp(self):
        if self.experience >= self.nextLevelUp:
                self.level += 1#Level up
                self.nextLevelUp *= 2 #Will get harder to level up each level.
                print("You've reached level {}!".format(self.level))
                print("Next level up at {} XP\n".format(self.nextLevelUp))


    def do_action(self, action, **kwargs):
     action_method = getattr(self, action.method.__name__)
     if action_method:
                action_method(**kwargs)


    def flee(self, tile):
        """Moves the player randomly"""
        available_moves = tile.adjacent_moves()
        r=random.randint(0, len(available_moves))
        self.do_action(available_moves[r])
