#################################
# answerIndicator.py      
#
# Cel: wiadomość o poprawnej lub niepoprawnej odpowiedzi      
#################################

# ogólne importy
import pygame
import asyncio

# importy wewnętrzne
from bin.function import scaleImage

class answerIndicator(pygame.sprite.Sprite):
    indicatorGroup = pygame.sprite.Group()
    async def __disappearance(self):
        # pojawianie 
        for i in range(1, 15):
            self.image.set_alpha(i*17)
            await asyncio.sleep(0.2)
        await asyncio.sleep(0.1)
        
        # znikanie
        for i in range(1, 15):
            self.image.set_alpha(255-i*17)
            await asyncio.sleep(0.2)
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
        
        # strzałka
        if status:
            _s = scaleImage("./bin/images/progress_up.png", 2)
        else:
            _s = scaleImage("./bin/images/progress_down.png", 2)
            
        self.image.blit(_s, (0,0))
        
        self.image.convert_alpha()
        
        self.image.blit(
            pygame.font.SysFont("Ink Free", 22).render("POPRAWNA ODPOWIEDŹ" if status else "NIEPOPRAWNA ODPOWIEDŹ",True, (
                (20,240,20) if status else (240,20,20)
            )),
            (60, 15)
        )
        
        
        # task
        asyncio.create_task(self.__disappearance(), name="answerIndicator")