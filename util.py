import sounds

def getIntInput(self, player):

    while True:
        
            try:
                itemChoice = int(input())
            except ValueError:#Catch exception if input isn't int
                print("\nInvalid item choice")
                sounds.no()
                continue#Restart loop
            return itemChoice



