# stałe do obsługi łatwiej czcionek

# importy i inicjacje
import pygame


# COMIC SANS
def getfonts():
    pygame.font.init()
    return {
    # comic sans
    "BIG_COMICSANS" : pygame.font.SysFont('Comic Sans MS', 70),
    "MEDIUM_COMICSANS": pygame.font.SysFont('Comic Sans MS', 40),
    "SMALL_COMICSANS": pygame.font.SysFont('Comic Sans MS', 30),
    "VERYSMALL_COMICSANS": pygame.font.SysFont('Comic Sans MS', 20),
    "TINY_COMICSANS": pygame.font.SysFont('Comic Sans MS', 18),

    "BIG_CONSOLAS": pygame.font.SysFont("consolas", 70),
    "MEDIUM_CONSOLAS": pygame.font.SysFont("consolas", 40), 
    "SMALL_CONSOLAS": pygame.font.SysFont("consolas", 30),
    "VERYSMALL_CONSOLAS": pygame.font.SysFont("consolas", 20)
    }