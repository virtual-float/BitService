#################################
# fonts.py      
#
# Cel: szybki dostęp do czcionek po nazwie (z pygama)  
#################################


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
    "SMALLER_COMICSANS": pygame.font.SysFont('Comic Sans MS', 25),
    "VERYSMALLLANG_COMICSANS": pygame.font.SysFont('Comic Sans MS', 21),
    "VERYSMALL_COMICSANS": pygame.font.SysFont('Comic Sans MS', 20),
    "TINY_COMICSANS": pygame.font.SysFont('Comic Sans MS', 18),
    "TINER_COMICSANS": pygame.font.SysFont('Comic Sans MS', 16),
    "MORETINER_COMICSANS": pygame.font.SysFont('Comic Sans MS', 14),
    "TINYTINY_COMICSANS": pygame.font.SysFont('Comic Sans MS', 12),
    "KINDATINY_COMICSANS": pygame.font.SysFont('Comic Sans MS', 10),
    "ULTRATINY_COMICSANS": pygame.font.SysFont('Comic Sans MS', 8),

    # THOMA
    "MEDIUM_TAHOMA": pygame.font.SysFont('Tahoma', 40),
    "VERYSMALL_TAHOMA": pygame.font.SysFont('Comic Sans MS', 20),

    # CONSOLAS
    "BIG_CONSOLAS": pygame.font.SysFont("consolas", 70),
    "MEDIUM_CONSOLAS": pygame.font.SysFont("consolas", 40), 
    "SMALL_CONSOLAS": pygame.font.SysFont("consolas", 30),
    "VERYSMALL_CONSOLAS": pygame.font.SysFont("consolas", 20)
    }