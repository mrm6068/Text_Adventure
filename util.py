import sounds, time, sys


def printGameText(x):
    for character in x:
        sys.stdout.write(character)
        sys.stdout.flush()
        #print(character, end = '')
        time.sleep(.02)

def pause():
    input("Press any key to continue...")

def getIntInput(sInput):

    while True:
        
        try:
            itemChoice = int(input(sInput))
        except ValueError:#Catch exception if input isn't int
            print("\nInvalid item choice")
            sounds.no()
            continue#Restart loop
        return itemChoice

def dagRoomGraphic():

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

  
def potionGraphics():
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
