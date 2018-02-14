import winsound, os

dirname = os.path.dirname(__file__)#For relative file path for sounds

filename = os.path.join(dirname, '/sounds')
dirname = filename

def good():
    winsound.PlaySound(os.path.join(dirname, 'good.WAV') , winsound.SND_FILENAME)

def die():
    winsound.PlaySound(os.path.join(dirname, 'die.WAV') , winsound.SND_FILENAME)

def breakGlass():
    winsound.PlaySound(os.path.join(dirname, 'break_glass.WAV') , winsound.SND_FILENAME)

def drink():
    winsound.PlaySound(os.path.join(dirname, 'drink_sound.WAV') , winsound.SND_FILENAME)

def ogre():
    winsound.PlaySound(os.path.join(dirname, 'ogre1.WAV') , winsound.SND_FILENAME)

def chestOpen():
    winsound.PlaySound(os.path.join(dirname, 'chest_open.WAV') , winsound.SND_FILENAME)

def levelUp():
    winsound.PlaySound(os.path.join(dirname, 'level_up.WAV') , winsound.SND_FILENAME)

def gun():
    winsound.PlaySound(os.path.join(dirname, 'revolver.wav') , winsound.SND_FILENAME)

def no():
    winsound.PlaySound(os.path.join(dirname, 'no_dear.wav') , winsound.SND_FILENAME)

def hellhound():
    winsound.PlaySound(os.path.join(dirname, 'hellhound.wav') , winsound.SND_FILENAME)

def bear():
    winsound.PlaySound(os.path.join(dirname, 'bear.wav') , winsound.SND_FILENAME)

def arrow():
    winsound.PlaySound(os.path.join(dirname, 'arrow.wav') , winsound.SND_FILENAME)

def moltov():
    winsound.PlaySound(os.path.join(dirname, 'moltov.wav') , winsound.SND_FILENAME)

def ratHumanoid():
    winsound.PlaySound(os.path.join(dirname, 'rat_humanoid.wav') , winsound.SND_FILENAME)