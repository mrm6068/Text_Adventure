import sounds

def getIntInput(sInput):

    while True:
        
        try:
            itemChoice = int(input(sInput))
        except ValueError:#Catch exception if input isn't int
            print("\nInvalid item choice")
            sounds.no()
            continue#Restart loop
        return itemChoice



