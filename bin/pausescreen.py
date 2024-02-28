#################################
# pausescreen.py      
#
# Cel: zarządzanie pausescrenem który się pojawia po naciśnięciu np. ESC i stopuje grę       
#################################

# Tak, jest to klasa która musi mieć obiekt, ale mi sie wydaje to najłatwiejszy pomysł
# z przyszłości: Nie, nie był, ale nie chce mi się tego pisać od nowa

# importy
import pygame
from pygame import Vector2

# importy lokalne
import bin.savemanager as sm
import bin.achievements as ach
import bin.devmode as devmode
import bin.fonts as fn
import bin.window as wn

# klasa główna
class pauseScreen():
    object = None
    
    '''
        Służy do utworzenia obiektu obsługującego stopowanie gry
    '''
    def toggle(self, **kwargs) -> None:
        '''Służy do zmieniania stanu zastopowania gry\n
        Argumenty:\n
            - forceState (opcjonalne, służy do zmiany stanu okna)\n
            - checkFocus (opcjonalne choć domyślnie True, wymaga by focus był wyłączony gdy próbuję się wyjść do menu)\n
        zwraca:\n
            - None\n
        '''
        if not 'checkFocus' in kwargs or kwargs.get('checkFocus') == True:
            if wn.window.getFocusElement() != None:
                return
        
        if 'forceState' in kwargs:
            if not isinstance(kwargs['forceState'], bool):
                raise Exception("Boolean musisz podać")
            self.__state = kwargs['forceState']
        else:
            self.__state = not self.__state
            
        if self.__state == True:
            wn.window.removeFocus()
          
    def getState(self) -> bool:
        '''Służy do pozyskania stanu zastopowania gry\n
        Argumenty:\n
            Brak\n
        zwraca:\n
            - Bool (stan stopowania)\n
        '''  
        return self.__state
    
            
                    
    def draw(self, screen: pygame.surface.Surface, DEVMODE: bool) -> None:
        '''Służy do rysowania stanu zastopowania gry\n
        Argumenty:\n
            Screen (pygame.display), gdzie będzie to rysowane\n
        zwraca:\n
            - None\n
        '''  
        if not self.__state: return
        
        screen.blit(self.__image, (0,0))
        screen.blit(
            self.__fonts['BIG_COMICSANS'].render("Gra zatrzymana", False, (255,255,255,77)),
            (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.07)
        )        
        screen.blit(
            self.__fonts['VERYSMALL_COMICSANS'].render("użyj strzałek/wsadu i enteru; q/esc by powrócić do gry", False, (255,255,255,77)),
            (20, screen.get_size()[1] - 35)
        )
        
        screen.blit(
            self.__fonts['SMALL_COMICSANS'].render(f"Powróć do gry {'<-- ' if self.__cursorPosition == 0 else ''}", False, (255,255,255,77)),
            (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30)
        )
        
        screen.blit(
            self.__fonts['SMALL_COMICSANS'].render(f"Zapisz grę {'<-- ' if self.__cursorPosition == 1 else ''}", False, (255,255,255,77)),
            (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30 + 40)
        )
        
        screen.blit(
            self.__fonts['SMALL_COMICSANS'].render(f"Wyjdź do menu {'<-- ' if self.__cursorPosition == 2 else ''}", False, (255,255,255,77)),
            (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30 + 80)
        )
        
        screen.blit(
            self.__fonts['SMALL_COMICSANS'].render(f"Wyjdź z gry {'<-- ' if self.__cursorPosition == 3 else ''}", False, (255,255,255,77)),
            (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30 + 120)
        )
        
        
        if DEVMODE:
            screen.blit(
                self.__fonts['SMALL_COMICSANS'].render(f"Tryb dewelopera {'<-- ' if self.__cursorPosition == 4 else ''}", False, (255,255,255,77)),
                (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30 + 160)
            )
         

    def eventHandler(self, DEVMODE: bool, EVENTS: list, save: dict) -> bool:
        for E in EVENTS:
            if not (E.type == pygame.KEYDOWN or E.type == pygame.MOUSEBUTTONDOWN): continue
            
            if E.type == pygame.MOUSEBUTTONDOWN:
            # obsługa myszki
                # obsługiwanie tylko lewego przycisku
                if E.button == 1:
                    
                    _pos = (
                        E.pos[0] * (self.__screenSize[0] / pygame.display.get_surface().get_size()[0]),
                        E.pos[1] * (self.__screenSize[1] / pygame.display.get_surface().get_size()[1])
                        )
                    
                    # print(self.__returnRect.collidepoint(E.pos), E.pos)
                    
                    # wyjście z menu pauzy
                    if self.__returnRect.collidepoint(_pos):
                        self.__state = 0
                    # zapis gry
                    elif self.__saveRect.collidepoint(_pos):
                        save.save()
                    # wyjście do menu
                    elif self.__menuExitRect.collidepoint(_pos):
                        return 1
                    # wyjście z gry
                    elif self.__gameExitRect.collidepoint(_pos):
                        return 2
                    # devmode
                    elif devmode and self.__devmodeRect.collidepoint(_pos):
                        _s = sm.get(alwaysNew=False)
                        _s.set("everdevmode", True)
                        _s.set("devmode", not _s.get("devmode", default=False))
                        
                        if _s.get("devmode", default=False):
                            ach.achievement("devmode ON")
                            devmode.runDevMode()
                        else:
                            ach.achievement("devmode OFF")
                    
            # obsługa klawiszy
            elif E.type == pygame.KEYDOWN:
                match E.key:
                    # góra
                    case pygame.K_w | pygame.K_UP:
                        self.__cursorPosition -= 1
                        
                        if DEVMODE and self.__cursorPosition < 0:
                            self.__cursorPosition = 4
                        elif self.__cursorPosition < 0:
                            self.__cursorPosition = 3   
                            
                    # dół     
                    case pygame.K_s | pygame.K_DOWN:
                        self.__cursorPosition += 1
                        
                        if not DEVMODE and self.__cursorPosition > 3:
                            self.__cursorPosition = 0
                        elif DEVMODE and self.__cursorPosition > 4:
                            self.__cursorPosition = 0
                            
                    # zatwierdzanie enterem 
                    case pygame.K_RETURN:
                        match self.__cursorPosition:
                            # wyjście z menu pauzy
                            case 0:
                                self.__state = False
                            
                            # zapis gry
                            case 1: save.save()
                            # wyjście do menu gry
                            case 2: return 1
                            # wyjście z gry
                            case 3: return 2
                            # devmode
                            case 4:
                                _s = sm.get(alwaysNew=False)
                                _s.set("everdevmode", True)
                                _s.set("devmode", not _s.get("devmode", default=False))
                                
                                if _s.get("devmode", default=False):
                                    ach.achievement("devmode ON")
                                    devmode.runDevMode()
                                else:
                                    ach.achievement("devmode OFF")
                            
                            case _: 
                                return 0

                        
                    case _: 
                        return 0
        
    def __init__(self, screen: pygame.surface.Surface = pygame.display.get_surface()) -> None:
        '''Służy do rysowania stanu zastopowania gry\n
        Argumenty:\n
            Screen (pygame.display), pobierze z tego rozmiar okna\n
        zwraca:\n
            - None\n
        '''
        self.__screenSize = screen.get_size()
        
        self.__state = False
        
        self.__image = pygame.Surface(screen.get_size()).convert_alpha()
        self.__image.fill((0,0,0, 120))
        
        
        self.__cursorPosition = 0
        
        self.__fonts = fn.getfonts()
        
        pauseScreen.object = self
        
        # recty
        
        # return Rect
        self.__returnRect = self.__fonts['SMALL_COMICSANS'].render(f"Powróć do gry <-- ", False, (255,255,255,77)).get_rect()
        self.__returnRect.topleft = (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30)
 
        # save Rect
        self.__saveRect = self.__fonts['SMALL_COMICSANS'].render(f"Zapisz grę <-- ", False, (255,255,255,77)).get_rect()
        self.__saveRect.topleft = (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30 + 40)   
        
        # menu exit Rect
        self.__menuExitRect = self.__fonts['SMALL_COMICSANS'].render(f"Wyjdź do menu <-- ", False, (255,255,255,77)).get_rect()
        self.__menuExitRect.topleft = (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30 + 80)        
        
        # game exit Rect
        self.__gameExitRect = self.__fonts['SMALL_COMICSANS'].render(f"Wyjdź z gry <-- ", False, (255,255,255,77)).get_rect()
        self.__gameExitRect.topleft = (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30 + 120)        
        
         # game exit Rect
        self.__devmodeRect = self.__fonts['SMALL_COMICSANS'].render(f"Tryb dewelopera <-- ", False, (255,255,255,77)).get_rect()
        self.__devmodeRect.topleft = (screen.get_size()[0] * 0.32, screen.get_size()[1] * 0.30 + 160)        
        
