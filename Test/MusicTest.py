#from pydub import AudioSegment
#from pydub.playback import play

#song = AudioSegment.from_wav("Pigstep.wav")
 #play(song)

import pygame
pygame.mixer.init()
pygame.mixer.music.load("Pigstep.ogg")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
quit()