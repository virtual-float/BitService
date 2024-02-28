#################################
# fonts.py      
#
# Cel: szybki dostęp do czcionek po nazwie (z pygama)  
#################################


# stałe do obsługi łatwiej czcionek

# importy i inicjacje
import pygame

from os import getcwd

FONT_FAMILY : str = 'Comic Sans MS'

# COMIC SANS
def getfonts():
    pygame.font.init()
    return {
    # comic sans
    "BIG_COMICSANS" : pygame.font.SysFont(FONT_FAMILY, 70),
    "MEDIUM_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 40),
    "SMALL_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 30),
    "SMALLER_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 25),
    "VERYSMALLLANG_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 21),
    "VERYSMALL_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 20),
    "TINY_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 18),
    "TINER_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 16),
    "MORETINER_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 14),
    "TINYTINY_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 12),
    "KINDATINY_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 10),
    "ULTRATINY_COMICSANS": pygame.font.SysFont(FONT_FAMILY, 8),

    # THOMA
    "MEDIUM_TAHOMA": pygame.font.SysFont('Tahoma', 40),
    "VERYSMALL_TAHOMA": pygame.font.SysFont('Tahoma', 20),

    # CONSOLAS
    "BIG_CONSOLAS": pygame.font.SysFont("consolas", 70),
    "MEDIUM_CONSOLAS": pygame.font.SysFont("consolas", 40), 
    "SMALL_CONSOLAS": pygame.font.SysFont("consolas", 30),
    "VERYSMALL_CONSOLAS": pygame.font.SysFont("consolas", 20)
    }