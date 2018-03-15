import sounds, time, sys


def printGameText(x):
    #print(x)
    for character in x:
        sys.stdout.write(character)
        sys.stdout.flush()
        #print(character, end = '')
        #time.sleep(.035)
        time.sleep(.005)

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
    time.sleep(.2)
    print( """   |  |""") 
    time.sleep(.2)
    print( """   |  |""")
    time.sleep(.2)
    print( """   |  |""")
    time.sleep(.2)
    print( """ __|  |__""")
    time.sleep(.2)
    print( """|___   __|""")
    time.sleep(.2)
    print( """    | |""")
    time.sleep(.2)
    print( """    ---""")
    time.sleep(.2)

  
def potionGraphics():
    print( """\n   /***\\""")
    time.sleep(.2)
    print( """  /^^^^^\\""") 
    time.sleep(.2)
    print( """ /       \\""")
    time.sleep(.2)
    print( """< POTION  >""")
    time.sleep(.2)
    print( """ \       /""")
    time.sleep(.2)
    print( """  \     /""")
    time.sleep(.2)
    print( """   \___/\n""")
    time.sleep(.5)
    print('You found a bottle and you drink the purple potion.\n')
    sounds.drink()
    time.sleep(.5)
    print('You smash the bottle.')
    sounds.breakGlass()
    time.sleep(.5)

def ameliaGraphic():
    print("   ____________________")
    time.sleep(.2)
    print("/////////////////////||\\")
    time.sleep(.2)
    print("////////////////////||||")
    time.sleep(.2)
    print("|||||||||||          |||")
    time.sleep(.2)
    print("|||||||||  O       O ||")
    time.sleep(.2)
    print("|||||||        /    /|")
    time.sleep(.2)
    print("||||||\       __  /|||")
    time.sleep(.2)
    print("||||||||\_______/||||")
    time.sleep(.2)
    print("|||||||||||||____|||||||||")
    time.sleep(.2)
    print("||||||||||                   \\")
    time.sleep(.2)
    print("||||||| |  (       (    |     |")
    time.sleep(.2)
    print("||||||| |               |     |")
    time.sleep(.2)
    print("||||||  |               \     \\")
    time.sleep(.2)
    print("/    //                 \\    \\")
    time.sleep(.2)
    print("    //                    \\    \\")
    time.sleep(.2)
    print("  //                        \\    \\")
    time.sleep(.2)
    print(")/______________\( ,,,)")
    time.sleep(.2)
    print("{ >o﹤ }{ >o﹤ }{ >o﹤ }")
    time.sleep(.2)
    print("        |     |      |     |")
    time.sleep(.2)
    print("        |     |      |     |")
    time.sleep(.2)
    print("      (___ |      | ___)\n")
    time.sleep(.58)
