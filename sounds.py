import winsound, os

dirname = os.path.dirname(__file__)#For relative file path for sounds

def good():
    winsound.PlaySound(os.path.join(dirname, 'good.WAV') , winsound.SND_FILENAME)

def die():
    winsound.PlaySound(os.path.join(dirname, 'die.WAV') , winsound.SND_FILENAME)

def breakGlass():
    winsound.PlaySound(os.path.join(dirname, 'break_glass.WAV') , winsound.SND_FILENAME)

def drink():
    winsound.PlaySound(os.path.join(dirname, 'drink_sound.WAV') , winsound.SND_FILENAME)

def drink():
    winsound.PlaySound(os.path.join(dirname, 'ogre.WAV') , winsound.SND_FILENAME)

def chestOpen():
    winsound.PlaySound(os.path.join(dirname, 'chest_open.WAV') , winsound.SND_FILENAME)

def levelUp():
    winsound.PlaySound(os.path.join(dirname, 'level_up.WAV') , winsound.SND_FILENAME)

