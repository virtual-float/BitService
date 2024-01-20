import pygame
import json
import asyncio

import bin.fonts as fn
class achievement:
    
    screen = None
    achievementShown = []
    __doExist = False
    
    @classmethod
    def configure(cls, screen: pygame.surface.Surface) -> None:
        '''
            skonfiguruj managera osiągnieć\n
            ----------------------------\n
            Argumenty:\n
                screen (pygame.surface.Surface), screen gry\n
            zwraca:\n
                Brak        
        '''
        cls.screen = screen
        cls.achievementShown = []
        
        loop = asyncio.get_event_loop()
        loop.create_task(achievement.__loop(), name="achievementManager")
        
    @classmethod
    def loopDraw(cls) -> None:
        '''
            renderuj\n
            ----------------------------\n
            Argumenty:\n
                Brak\n
            zwraca:\n
                Brak        
        '''
        for element in cls.achievementShown:
            if not element.deleted: element.selfDraw()  
        
    @classmethod
    async def __loop(cls) -> None:
        '''
            obliczaj osiągniecia\n
            ----------------------------\n
            Argumenty:\n
                Brak\n
            zwraca:\n
                Brak        
        '''
        while True:
            for element in cls.achievementShown:
                if element.deleted:
                    cls.achievementShown.remove(element)
                else:
                    element.selfLoop()
            await asyncio.sleep(0.02)
        
          
    def selfLoop(self) -> None:
        '''
            Self loop poprostu
        '''
        self.__cords[0] += 7
        if self.__cords[0] > achievement.screen.get_size()[0] + 105:
            self.deleted = True

    def selfDraw(self) -> None:
        '''
            Self draw poprostu
        '''
        achievement.screen.blit(
            self.__surface,
            self.__cords            
        )
        
    def __init__(self, achievementName: str, *args, **kwargs):
        '''
            Tworzy nowe osiągniecie\n
            ----------------------------\n
            Argumenty:\n
                achievementName (str) -> wyświetlana nazwa\n
                image (pygame.surface.Surface {64x64}, opcjonalne) -> ikona osiągniecia\n
                color (TUPLE/LIST: (R,G B), opcjonalne) -> kolor nazwy\n
            zwraca:\n
                achievement (opcjonalne)     
        '''
        
        # sprawdź czy skonfigurowano wcześniej manager
        if achievement.screen == None:
            raise Exception("Nie skonfigurowano managera achievementów")
        
        # obsługa kwargs
        
        # image
        if 'image' in kwargs:
            if not isinstance(kwargs['image'], pygame.surface.Surface):
                raise Exception("Zły typ podany w osiągnieciu jako obraz (WYMAGANY: pygame.surface.Surface)")
            
            image = pygame.transform.scale(kwargs['image'], (64,64))
        else:
            image = pygame.surface.Surface((64,64))
            image.fill((0,0,0))
            
        # color
        if 'color' in kwargs:
            self.__color = kwargs['color']
        else:
            self.__color = (0,255,0)
        
        
        # ustawienie podstawowych parametrów
        self.deleted = False
        
        self.__name = achievementName
        self.__image = image
        
        # surface
        self.__surface = pygame.surface.Surface((250,64))
        self.__surface.fill((153, 153, 102))
        self.__surface.blit(self.__image, (0, 0))
        
        _fonts = fn.getfonts()
        self.__surface.blit(
             _fonts['VERYSMALL_COMICSANS'].render(self.__name, False, self.__color),
            (66, 5)
        )
        self.__surface = self.__surface.convert_alpha()
        self.__surface.set_alpha(170)
        
        
        
        # kordy
        self.__cords = [achievement.screen.get_size()[0] - 350, achievement.screen.get_size()[1] - ((len(achievement.achievementShown) +1) * 120)]
        
        # dodanie do listy na koniec
        achievement.achievementShown.append(self)
        
        