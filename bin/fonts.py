# stałe do obsługi łatwiej czcionek

# importy i inicjacje
import pygame


# COMIC SANS
def getfonts():
    pygame.font.init()
    return {
    "BIG_COMICSANS" : pygame.font.SysFont('Comic Sans MS', 70),
    "MEDIUM_COMICSANS": pygame.font.SysFont('Comic Sans MS', 40),
    "SMALL_COMICSANS": pygame.font.SysFont('Comic Sans MS', 30),
    "VERYSMALL_COMICSANS": pygame.font.SysFont('Comic Sans MS', 20)
    }