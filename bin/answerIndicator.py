#################################
# answerIndicator.py      
#
# Cel: wiadomość o poprawnej lub niepoprawnej odpowiedzi      
#################################

# ogólne importy
import pygame
import asyncio

from os import getcwd

# importy wewnętrzne
from bin.function import scaleImage

class answerIndicator(pygame.sprite.Sprite):
    indicatorGroup = pygame.sprite.Group()
    async def __disappearance(self):
        # pojawianie 
        for i in range(1, 15):
            self.image.set_alpha(i*17)
            await asyncio.sleep(0.05)
        await asyncio.sleep(2)
        
        # znikanie
        for i in range(1, 15):
            self.image.set_alpha(255-i*17)
            await asyncio.sleep(0.05)
        await asyncio.sleep(0.1)
            
        # niszczenie    
        self.kill()

        
    
    def __init__(self, status:bool=True):
        super().__init__(self.indicatorGroup)
        
        # podstawy
        self.image = pygame.surface.Surface((320, 74))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (20,520)
        self.image.set_alpha(0)
        
        _s = scaleImage('./bin/images/information.png', 3)
            
        self.image.blit(_s, (0,0))
        
        self.image.convert_alpha()

        COMMON_X : int = 20
        COMMON_FONT_SZ : int = 29
        
        self.image.blit(
            pygame.font.SysFont(getcwd() + '\\bin\\franklin_gothic.TTF', COMMON_FONT_SZ, bold=True).render("POPRAWNA" if status else "NIEPOPRAWNA", True, 
                (250,250,250)),
            (COMMON_X, 2)
        )
        self.image.blit(
            pygame.font.SysFont(getcwd() + '\\bin\\franklin_gothic.TTF', COMMON_FONT_SZ, bold=True).render("ODPOWIEDŹ", True, 
                (250, 250, 250)), 
            (COMMON_X, 24)
        )
        
        
        # task
        asyncio.create_task(self.__disappearance(), name="answerIndicator")