# PAUSESCREEN

# importy
import pygame


# klasa główna
class pauseScreen():
    '''
        Służy do utworzenia obiektu obsługującego stopowanie gry
    '''
    def toggle(self, **kwargs) -> None:
        '''Służy do zmieniania stanu zastopowania gry\n
        Argumenty:\n
            - forceState (opcjonalne, służy do zmiany stanu okna)\n
        zwraca:\n
            - None\n
        '''
        if 'forceState' in kwargs:
            if not isinstance(kwargs['forceState'], bool):
                raise Exception("Boolean musisz podać")
            self.__state = kwargs['forceState']
        else:
            self.__state = not self.__state
          
    def getState(self) -> bool:
        '''Służy do pozyskania stanu zastopowania gry\n
        Argumenty:\n
            Brak\n
        zwraca:\n
            - Bool (stan stopowania)\n
        '''  
        return self.__state
            
            
    def draw(self, screen: pygame.display = pygame.display.get_surface()) -> None:
        '''Służy do rysowania stanu zastopowania gry\n
        Argumenty:\n
            Screen (pygame.display), gdzie będzie to rysowane\n
        zwraca:\n
            - None\n
        '''  
        if not self.__state: return

        screen.blit(self.__image, (0,0))
        screen.blit(
            self.__mainText.render("Gra zatrzymana", False, (255,255,255,77)),
            (pygame.display.get_window_size()[0] * 0.32, pygame.display.get_window_size()[1] * 0.07)
        )

        
        
    def __init__(self, screen: pygame.display = pygame.display.get_surface()) -> None:
        '''Służy do rysowania stanu zastopowania gry\n
        Argumenty:\n
            Screen (pygame.display), pobierze z tego rozmiar okna\n
        zwraca:\n
            - None\n
        '''
        self.__state = False
        
        self.__image = pygame.Surface(screen.get_size()).convert_alpha()
        self.__image.fill((0,0,0,77))
        
        self.__mainText = pygame.font.SysFont('Comic Sans MS', 70)
        
        
        