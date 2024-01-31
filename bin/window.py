# importy podstawowe
from typing import Any, Iterable, Union
import pygame
import asyncio
import abc

# importy pygama
from pygame.sprite import AbstractGroup

# importy lokalne
import bin.savemanager as saveManager
import bin.fonts as fn
import bin.pausescreen as psc



class windowElement(pygame.sprite.Sprite):
    '''Podstawowy obiekt w oknie'''
    
    def focusLoop(self, me: 'windowElement', events, window: 'window'): 
        '''
            Funkcja wykonuje się za każdym razem gdy może (max co 0.05s)\n
            UWAGA: wymaga uzycia listenera na obiekcie by to działało\n
            window.addObjectToListen(tenObiekt)\n
            ------------------------\n
            Funkcje należy zaimplementować w obiekcie który dziedziczy lub ustawić ją za pomocą
            tenObiekt.setFocusLoop(Funkcja)\n
            \n
            Funkcja musi przyjmować:\n\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setFocusLoop to tracisz selfa\n
            * events <- Dostaniesz tutaj aktualne eventy\n
            * window <- dostaniesz tutaj okno\n
            \n
            ------------------------------\n
            Funkcji nie powinieneś wywoływać samemu!
        '''
        pass
    
    
    def setFocusLoop(self, function: object) -> 'windowElement':
        '''
            Służy do ustawiania focus Loopa na obiekcie.\n
            Uwaga obiekty takie jak textbox już mają zaimplementowanego focus Loopa!\n
            --------------------------\n
            Argumenty:\n
                * Funkcja (Object Function)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)
            --------------------------\n
            Funkcja musi przyjmować:\n\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setFocusLoop to tracisz selfa\n
            * events <- Dostaniesz tutaj aktualne eventy\n
            * window <- dostaniesz tutaj okno\n            
        '''
        self.focusloop = function
        return self
    
    
    def focusEnd(self, me: 'windowElement', events, window: 'window'):
        '''
            Funkcja wywołuje się z odznaczeniem obiektu\n
            Funkcje należy zaimplementować w obiekcie który dziedziczy lub ustawić ją za pomocą
            tenObiekt.setFocusEnd(Funkcja)\n
            \n
            Funkcja musi przyjmować:\n\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setFocusLoop to tracisz selfa\n
            * events <- Dostaniesz tutaj aktualne eventy\n
            * window <- dostaniesz tutaj okno\n
            \n
            ------------------------------\n
            Funkcji nie powinieneś wywoływać samemu!
        '''
        pass

    def setFocusEnd(self, function: object) -> 'windowElement':
        '''
            Służy do ustawiania focus Enda na obiekcie.\n
            Uwaga obiekty takie jak textbox już mają zaimplementowanego focus Enda!\n
            --------------------------\n
            Argumenty:\n
                * Funkcja (Object Function)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)
            --------------------------\n
            Funkcja musi przyjmować:\n\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setFocusEnd to tracisz selfa\n
            * events <- Dostaniesz tutaj aktualne eventy\n
            * window <- dostaniesz tutaj okno\n            
        '''
        self.focusEnd = function
        return self    

    
    def focusStart(self, me, events, window: 'window'):
        '''
            Funkcja wywołuje się z zaznaczeniem obiektu\n
            Funkcje należy zaimplementować w obiekcie który dziedziczy lub ustawić ją za pomocą
            tenObiekt.setFocusStart(Funkcja)\n
            \n
            Funkcja musi przyjmować:\n\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setFocusLoop to tracisz selfa\n
            * events <- Dostaniesz tutaj aktualne eventy\n
            * window <- dostaniesz tutaj okno\n
            \n
            ------------------------------\n
            Funkcji nie powinieneś wywoływać samemu!
        '''
        pass
    
    def setFocusStart(self, function: object) -> 'windowElement':
        '''
            Służy do ustawiania focus Starta na obiekcie.\n
            Uwaga obiekty takie jak (aktualnie takie nie istnieją) już mają zaimplementowanego focus Starta!\n
            --------------------------\n
            Argumenty:\n
                * Funkcja (Object Function)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)
            --------------------------\n
            Funkcja musi przyjmować:\n\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setFocusStart to tracisz selfa\n
            * events <- Dostaniesz tutaj aktualne eventy\n
            * window <- dostaniesz tutaj okno\n            
        '''
        self.focusStart = function
        return self 
    
    
    def setPosition(self, cords: list[int,int] | tuple[int,int] = [0,0]) -> 'windowElement':
        '''
            Służy do ustawiania pozycji okna\n
            ---------------------\n
            Argumenty:\n
                * cords (poprostu kordynaty x i y wyrażone za pomocą tupla bądź listy)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)
        '''
        self.rect.topleft = [cords[0], cords[1]]
        return self
        
        
    def getPosition(self) -> list[int,int]:
        '''Służy do pozyskiwania pozycji okna\n
            Argumenty:\n
                * Brak\n
            Zwraca:\n
                * cords (kordynaty okna, lista z dwoma intami)'''
        return self.rect.topleft
    
    
    def setImage(self, image: pygame.surface.Surface) -> 'windowElement':
        '''
            Służy do ustawiania grafiki obiektu\n
            ---------------------\n
            Argumenty:\n
                * grafika (pygame.surface.Surface)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)
        '''
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        return self
    
        
    def getImage(self) -> pygame.surface.SurfaceType:
        '''Służy do pozyskiwania grafiki obiektu\n
            Argumenty:\n
                * Brak\n
            Zwraca:\n
                * grafika (pygame.surface.Surface)'''
        return self.image
    
    
    def click(self, me: 'windowElement', pressed:tuple[bool], pos:tuple[int], posRelative:tuple[int], events, window: 'window') -> bool:
        '''
            Funkcja wywołuje się z nacisnieciem obiektu\n
            Funkcje należy zaimplementować w obiekcie który dziedziczy lub ustawić ją za pomocą
            tenObiekt.setClickListener(Funkcja)\n
            \n
            Funkcja musi przyjmować:\n\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setClickListener to tracisz selfa\n
            * pressed (tuple trzech booli, jakie przyciski są naciśnięte (lewy, scroll, prawy))\n
            * pos (tuple dwóch intów, bewzględna pozycja myszki)\n
            * pos (tuple dwóch intów, względna względem okna pozycja myszki)\n
            * events <- Dostaniesz tutaj aktualne eventy\n
            * window <- dostaniesz tutaj okno\n
            \n
            ------------------------------\n
            Funkcji nie powinieneś wywoływać samemu!
        '''
        pass
        
        
    def addClickListener(self, function:object=lambda me, pressed, pos, posRelative, events, window: False) -> 'windowElement':
        '''
            Służy do ustawiania event Clicka na obiekcie.\n
            Uwaga obiekty takie jak (aktualnie takie nie istnieją) już mają zaimplementowanego focus Starta!\n
            --------------------------\n
            Argumenty:\n
                * Funkcja (Object Function)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)
            --------------------------\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setClickListener to tracisz selfa\n
            * pressed (tuple trzech booli, jakie przyciski są naciśnięte (lewy, scroll, prawy))\n
            * pos (tuple dwóch intów, bewzględna pozycja myszki)\n
            * pos (tuple dwóch intów, względna względem okna pozycja myszki)\n
            * events <- Dostaniesz tutaj aktualne eventy\n
            * window <- dostaniesz tutaj okno\n
            \n     
        '''
        self.click = function
        return self
    
    def __init__(self, image: pygame.surface.Surface, cords: list[int, int] | tuple[int, int] = [0,0], clickListener:None|object = None):
        '''Tworzenie obiektu\n
            Argumenty:\n
                * image (jak będzie wyglądać obiekt, pygame.surface.Surface)\n
                * cords (lista dwóch intów, relatywne kordynaty do okna; opcjonalne, lecz zalecane)\n
                \n
                * clickListener (opcjonalny, funkcja), pozwala na łatwe ustawienie clickListenera odrazu bez wywoływania
                dodatkowej metody\n
            Zwraca:\n
                * Obiekt
        '''
        
        # inicjalizacja klasy nadrzędnej od pygama
        super().__init__()
        
        # podstawowe atrybuty
        self.pos = cords
        self.image = image.convert_alpha()
        self.rect = image.get_rect()
        self.rect.topleft = [cords[0], cords[1]]
        self.focused = False
        self.autoListen = False
        
        # opcjonalny listener
        if clickListener != None:
            self.click = clickListener

    
class windowText(windowElement):
    '''Obiekt reprezentujący tekst w oknie, pochodna windowElement'''
    
    def setText(self, text: str) -> 'windowText':
        '''Służy do ustawiania tekstu\n
            Argumenty:\n
                * tekst (string)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)'''
        self.__text = text
                
        # renderowanie fonta
        self.image = self.__font.render(text, False, self.__color).convert_alpha()
        self.rect = self.image.get_rect()
        return self


    def getText(self) -> str:
        '''Służy do pozyskiwania tekstu\n
            Argumenty:\n
                * Brak \n
            Zwraca:\n
                * tekst (string)'''        
        
        return self.__text
  
  
    def setColor(self, color: tuple[int,int,int]) -> 'windowText':
        '''Służy do ustawiania koloru\n
            Argumenty:\n
                * kolor (tuple[int,int,int], kolor w RGB)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)'''
        self.__color = color
                
        # renderowanie fonta
        self.image = self.__font.render(self.__text, False, color).convert_alpha()
        self.rect = self.image.get_rect()
        return self

    def getColor(self) -> tuple[int,int,int]:
        '''Służy do pozyskiwania tekstu\n
            Argumenty:\n
                * Brak \n
            Zwraca:\n
                * kolor (tuple[int,int,int], kolor w RGB)\n'''        
        
        return self.__color     
    
    def __init__(self, fontName:str, text:str, cords: list[int, int] | tuple[int, int] | pygame.Vector2 = [0, 0], color:tuple[int] = (0,0,0), clickListener:None|object = None):
        '''Tworzenie obiektu\n
            Argumenty:\n
                * fontName (string, nazwa fonta, aktualnie obiekt obsługuje tylko i wyłącznie stringi z fonts.py)\n
                * text (string, poprostu tekst)\n
                * cords (lista dwóch intów, relatywne kordynaty do okna; opcjonalne lecz zalecane)\n
                \n
                * color (tuple trzech intów, opcjonalny kolor)\n
                * clickListener (opcjonalny, funkcja), pozwala na łatwe ustawienie clickListenera odrazu bez wywoływania
                dodatkowej metody\n
            Zwraca:\n
                * Obiekt
        '''
        # podstawowe argumenty
        self.__fontName, self.__color, self.__text = fontName, color, text
        
        # ustawienie fonta
        _fn = fn.getfonts()
        self.__font = _fn[fontName]
        
        # renderowanie fonta
        _img = self.__font.render(text, False, color).convert_alpha()
        
        # inicjalizacja klasy nadrzędnej
        super().__init__(_img, cords, clickListener=clickListener)    


class windowTextBox(windowElement):
    '''Łatwy, prosty, jednoliniowy textbox'''
    
    # podstawowe grafiki
    textboxLeftImg = pygame.image.load("bin/images/textbox_left.png")
    textboxMidImg = pygame.image.load("bin/images/textbox_mid.png")
    textboxRightImg = pygame.image.load("bin/images/textbox_right.png")
    textboxOneImg = pygame.image.load("bin/images/textbox_one.png")
    
    
    def focusLoop(self, me, events, window):
        '''Funkcja zaimplementowana, nie dotykać jej, nawet jej nie wywoływać'''
        
        # miganie kursora
        if len(self.__displayText) == len(self.text):
            self.__displayText = self.text + "|"
        else:
            self.__displayText = self.text
        
        # obsługa zdarzeń
        for event in events:
            if event.type == pygame.KEYDOWN:
                # backspace
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # enter
                elif event.key == pygame.K_RETURN:
                    if not self.__returnText(self.text):
                        self.text = ''
                # wpisywanie znaków
                elif event.key != pygame.K_ESCAPE:
                    if not len(self.text) >= self.maxlength:
                        self.text += event.unicode
        
        # wyrenderowanie nowego obrazu obiektu
        self.image = self.__imageTemplate.copy()
        self.__renderText()
        self.image.blit(self.__background, (0,0))
        self.image.blit(self.__textImg, (self.__marginLeft,0))
    
    
    def focusEnd(self, me, events, window):
        '''Funkcja zaimplementowana, nie dotykać jej, nawet jej nie wywoływać'''
        # usunięcie migania
        self.__displayText = self.text
        
        # wyrenderowanie nowego obrazu obiektu
        self.image = self.__imageTemplate.copy()
        self.__renderText()
        self.image.blit(self.__background, (0,0))
        self.image.blit(self.__textImg, (self.__marginLeft,0))
        
        
    def setReturnListener(self, function: object = lambda text: 0):
        '''
            Służy do ustawiania returna na obiekcie.\n
            --------------------------\n
            Argumenty:\n
                * Funkcja (Object Function)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)
            --------------------------\n
            Funkcja musi przyjmować:\n\n
            * Self <- Dostaniesz tutaj obiekt\n
            * me <- Kopia self, jest poprostu zabezpieczeniem bo gdy ustawiasz za pomocą\n
            setFocusStart to tracisz selfa\n
            * text <- (string, dostaniesz tutaj tekst)\n            
        '''
        self.__returnText = function
        return self
        
        
    def __returnText(self, me: 'windowTextBox', text:str): 
        '''Funcja prywatna, wypadać stąd, ustawia się ją za pomocą setReturnListener a nie tak!'''
        self.text = text
    
    
    def __renderText(self):
        '''Funkcja prywatna, służąca do renderingu tekstu'''
        self.__textImg = self.__font.render(self.__displayText, False, self.__color).convert_alpha()
        
        
    def __generateBackground(self) -> None:
        '''Funkcja prywatna, służąca do renderingu tła'''
        
        # paleta by mieć gdzie renderować
        _tempSurf = pygame.surface.Surface((self.__xsize * 10, 45))
        
        # rendering tła
        if self.__xsize == 1:
             _tempSurf.blit(windowTextBox.textboxOneImg, (0,0))
        else:    
            for i in range(0,self.__xsize):
                if i == 0:
                    _tempSurf.blit(windowTextBox.textboxLeftImg, (0,0))
                elif i == self.__xsize -1:
                    _tempSurf.blit(windowTextBox.textboxRightImg, (i * 10,0))
                else:
                    _tempSurf.blit(windowTextBox.textboxMidImg, (i * 10,0))
        
        # ustawienie tła
        self.__background = _tempSurf.convert_alpha()
        
        
    def __generateApperance(self) -> None:
        '''Funkcja prywatna, służąca do finalnego renderingu'''
        
        # wywołanie pozostałych renderingów przed
        self.__renderText()
        self.__generateBackground()
        
        # wyrenderowanie wszystko do nowej palety
        self.__imageTemplate = pygame.surface.Surface((self.__xsize * 10, 45))
        self.image = self.__imageTemplate.copy()
        self.image.blit(self.__background, (0,0))
        self.image.blit(self.__textImg, (5,0))
        
        # ustawienie recta
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos[0], self.pos[1]]
        
    
    def __init__(self, cords: list[int, int] | tuple[int, int] | pygame.Vector2 = [0, 0], startingText:str="", maxlength:int = 5, xsize:int=10, fontName:str="SMALL_COMICSANS", color:tuple[int,int,int] = (0,0,0),
                 marginleft:int=5, clickListener:None|object = None):
        '''Tworzenie obiektu\n
            Argumenty:\n
                * cords (lista dwóch intów, relatywne kordynaty do okna; opcjonalne lecz zalecane)\n
                * startingText (string, poprostu startowy tekst; opcjonalne)\n
                \n
                * maxlength (int, opcjonalne, maksymalna ilość wprowadzonych znaków)\n
                * xsize (int, opcjonalne, ilość kafelków (kwestia graficzna))\n
                * fontName (string, opcjonalny nazwa fonta, aktualnie obiekt obsługuje tylko i wyłącznie stringi z fonts.py)\n
                * color (tuple trzech intów, opcjonalny kolor)
                * marginleft (int, podstawowo 5, opcjonalne, ilość marginu dla tekstu z lewej strony)\n
                * clickListener (opcjonalny, funkcja), pozwala na łatwe ustawienie clickListenera odrazu bez wywoływania
                dodatkowej metody\n
            Zwraca:\n
                * Obiekt
        '''
        
        # ustawienie podstawowych argumentów
        self.__fontName, self.__color = fontName, color
        self.__xsize, self.text = xsize, startingText
        self.__displayText = startingText
        self.maxlength = maxlength
        self.__marginLeft = marginleft
        
        # stworzenie fonta
        _fn = fn.getfonts()
        self.__font = _fn[fontName]
        
        # wywołanie klasy nadrzędnej
        super().__init__(windowTextBox.textboxLeftImg, cords, clickListener=clickListener)
        
        # wygenerowanie początkowego wyglądu
        self.__generateApperance()
        

# Tylko po to by mieć fajną nazwę, nie trzeba tego używać, działa identycznie jak Groupa z pygama
class windowBody(pygame.sprite.Group):
    '''Tylko po to by mieć fajną nazwę, nie trzeba tego używać, działa identycznie jak Groupa z pygama'''
    def __init__(self, *sprites: Any | AbstractGroup | Iterable):
        super().__init__(*sprites)
        

class window():
    '''Obiekt okna'''
    
    # ikona zamykania
    closeImg = pygame.image.load('bin/images/close.png')
    
    # aktualnie nie pełni żadnego celu, w przyszłości moze będzie pokazywał czy jest włączona wymagana pętla
    isconfigured = False
    
    # lista okien poindeksowana po id
    __windowList = {
        
    }
    
    # kolejność renderowania oraz ważności okien (aktualnie działa tylko częsciowo bo nie było implementacji poruszania nimi) (nie zmienia ważności okien pod wpływem kliknięcia)
    __windowOrder = []
    
    # aktualny element na którym jest focus
    __focusedElement = None
    
    # aktualne okno
    lastFocusedWindow = None
    
    # eventy gracza
    events = None
    
    
    @classmethod
    def removeFocus(cls):
        '''Usunięcie wszystkich focusów'''
        # usunięcie z pamięci obiektu
        if cls.__focusedElement != None:
            cls.__focusedElement.focused = None
            cls.__focusedElement.focusEnd(cls.lastFocusedWindow,cls.events,cls)
            
        # usunięcie z naszej pamięci
        cls.__focusedElement = None
    
    @classmethod
    def sendEvents(cls, events) -> None:
        '''Wysłanie eventów poprostu'''
        cls.events = events
        
    
    @classmethod
    def startTask(cls) -> None:
        '''Włączenie tasku, powinien być maksymalnie 1 i zawsze minimum 1!'''
        asyncio.create_task(cls.__globalLoop(), name=f"windowManager")
    
    @classmethod
    async def __globalLoop(cls) -> None:
        '''Pętla do taska'''
        while True:
            # nie działanie gdy jest włączony ekran pauzy
            if psc.pauseScreen.object.getState(): 
                await asyncio.sleep(0.02)
                continue
            
            # próba pozyskania wciśniętych klawiszy myszy
            try:
                _pres = pygame.mouse.get_pressed()
            except: 
                return
            
            # obsługa naciśniecia
            if any(_pres):
                _pos = pygame.mouse.get_pos()
                _foundWindow = False
                
                # wyszukanie okna które mogłoby być nacisnięte
                for name in cls.__windowOrder:
                    window = cls.__windowList[name]
                    
                    # jeśli miejsce naciśnienia koliduje z pozycją
                    if window.windowRect.collidepoint(_pos):
                        
                        # usunięcie focusa gdy obiektu nie ma w oknie tym
                        if cls.__focusedElement != None and not cls.__focusedElement in window.getBody().sprites():
                            cls.__focusedElement.focused = False
                            cls.__focusedElement.focusEnd(cls.__focusedElement, cls.events, cls)
                            cls.__focusedElement = None
                   
                        # obsluga focusa i kliknięcia
                        cls.__focusedElement = window.handleClick(_pres,_pos, cls.__focusedElement)
                        _foundWindow = True
                        
                        # koniec pętli
                        break     
                    
                # obsługa kliknięcia poza okna (usunięcie focusu)
                if not _foundWindow and cls.__focusedElement != None: 
                    cls.__focusedElement.focused = False
                    cls.__focusedElement.focusEnd(cls.__focusedElement, cls.events, cls)
                    cls.__focusedElement = None
            
            # klasyczne spanko
            await asyncio.sleep(0.02)
            
    
    @classmethod
    def eraseWindows(cls) -> None:
        '''Usuwa wszystkie okna'''
        for name,window in cls.windowList().items():
            cls.removeWindow(name)
            
            
    @classmethod
    def removeWindow(cls, name:str) -> None:
        '''Usunięcie danego okna\n
            ----------------\n
            Argumenty:\n
                * name (string, nazwa okna)\n
            Zwraca:\n
                * None'''
        
        # usunięcia focusu jeżeli byłw tym oknie
        if cls.__focusedElement in cls.__windowList[name].getBody().sprites():
            cls.__focusedElement.focused = False
            cls.__focusedElement = None
        
        # usunięcia okna z listy głównej
        cls.__windowList.pop(name)
        
        # usunięcie tasku okna
        for task in asyncio.all_tasks():
            if task.get_name() == f"windowLoop_{name}": task.cancel()
        
        # usunięcie z orderu
        cls.__windowOrder.remove(name)
        
        # zapis do sava
        cls.__save()    
        
        
    @classmethod
    def getWindow(cls, name:str) -> 'window': 
        '''pozyskanie danego okna\n
            ----------------\n
            Argumenty:\n
                * name (string, nazwa okna)\n
            Zwraca:\n
                * okno (window)'''
        return cls.__windowList[name]
    
    
    @classmethod
    def checkWindow(cls, name:str) -> bool:
        '''sprawdzanie czy dane okno istnieje\n
            ----------------\n
            Argumenty:\n
                * name (string, nazwa okna)\n
            Zwraca:\n
                * bool (czy istnieje)'''
        return True if name in cls.__windowList else False
    
    
    @classmethod
    def windowList(cls) -> dict:
        '''Bezpieczna skopiowana lista okien, edycje nie zostają zapisane, do edycji\n
            użyj dedykowanych metod\n
            ----------------\n
            Argumenty:\n
                * Brak\n
            Zwraca:\n
                * dict'''
        return cls.__windowList.copy()
    
    
    @classmethod
    def addWindowToList(cls, name:str, window:'window', loop:asyncio.coroutines) -> None:
        '''
            To nie powinno być używane\n
            ------------\n
            Użyj window() zamiast tego
        '''
        cls.__windowList[name] = window
        cls.__windowOrder.insert(0, name)
        asyncio.create_task(loop, name=f"windowLoop_{name}")
        
        cls.__save()
        
        
    @classmethod
    def __save(cls):
        '''Zapisywanie do sava aktualnego stanu'''
        # pozyskanie menadżera savów
        _s = saveManager.get(alwaysNew=False)
        
        # lista okien
        _s.set('gameState.windows',
                {
                name:{
                    'position': window.getPosition(),
                    'size': window.getSize(),
                    'visible': window.visible,
                    'closable': window.closable,
                    'body': {
                        
                    }
                }
                for name, window in cls.__windowList.items()
                })
            
        # pozostałe
        _s.set("gameState.windowOrder", cls.__windowOrder)
        _s.set("gameState.windowNumber", len(cls.__windowList))
    
    
    @classmethod
    def draw(cls, destination:pygame.surface.Surface) -> None:
        '''
            Renderuje wszystkie okna\n
            Argumenty:\n
                * destination (pygame.surface.Surface) -> Gdzie renderować\n
            Zwraca:\n
                * None\n
            
        '''
        # no tego chyba nie musze wyjasniać :(
        for window in cls.__windowList.values():
            if window.visible:
                window.drawSelf(destination)
                
                
    
    def drawSelf(self, destination:pygame.surface.Surface) -> None:
        '''
            Renderuje pojedyncze okno\n
            Argumenty:\n
                * destination (pygame.surface.Surface) -> Gdzie renderować\n
            Zwraca:\n
                * None\n
        '''
        # rysuje podstawe na tymczasowych wartościach (body)
        self.__tempSurfaceBody.fill(self.__backgroundColor)
        self.__body.draw(surface=self.__tempSurfaceBody)
        
        # rysuje stałe tło
        destination.blit(self.__tempSurfaceBackground, (self.__position[0],self.__position[1]))
        
        # rysuje x jeżeli ma być narysowany
        if self.closable:
            destination.blit(window.closeImg, (self.__size[0] + self.__position[0] - 30,5 + self.__position[1]))
            
        # rysuje reszte (body)
        destination.blit(self.__tempSurfaceBody, (self.__position[0],40+self.__position[1]))
        
        
    
    async def __loop(self):
        '''Nie wywołuj tej funkcji naprawdę... To jest funckja dla taska okna'''
        while True:
            # nie działaj jeżeli jest włączone menu pauzy
            if psc.pauseScreen.object.getState(): 
                await asyncio.sleep(0.02)
                continue
            
            # keys = pygame.key.get_pressed()
            
            # obiekty do nasłuchiwania
            for element in self.__objectsToListen:
                if element.focused:
                    element.focusLoop(element, window.events, self)
                    break
                
            await asyncio.sleep(0.05)
        
        
    def handleClick(self, pressed: tuple[bool], pos: tuple[int], previousFocused) -> None | pygame.sprite.Sprite:
        '''
            Służy do obsługi kliknięcia na pojedynczym oknie\n
            funkcja jest wywoływana sama, nie musisz jej wywoływać (o ile jest task menadżera okien)\n
            ---------------------\n
            Argumenty:\n
                * pressed (tuple z 3 boolami, z tym defacto jakie przyciski nacisnięte)\n
                * pos (tuple z 3 intami, bezwględna pozycja myszki)\n
                * ostatni focus (przed tym)\n
            Zwraca:\n
                * None lub nowy focus\n
        '''
        # ta zmienna niewiem czy nie zostanie usunięta, bo jej sens jest aktualnie nie istniejący przez to że
        # returna się używa, ale zostawiam by jakby co można było łatwo przerobić kod
        # dodane przy okazji dodawania focusu na dany element
        _beenclicked = False
        
        # by zapamiętac jakie okno kliknęło ostatnio
        window.lastFocusedWindow = self
        
        # po wszystkich spritach
        for sprite in self.__body.sprites():
            # skopiuj recta i przesuń go tam gdzie powinno być okno (pozycja względna z bezwzględnej)
            _temp_rect = sprite.rect.copy()
            _temp_rect.topleft = (
                _temp_rect.topleft[0] + self.__position[0],
                _temp_rect.topleft[1] + self.__position[1] + 40
            )
            
            # jeśli myszka jest w tym spricie
            if _temp_rect.collidepoint(pos):
                
                # wywołaj metodę na spricie wtedy
                sprite.click(sprite, pressed, pos, (pos[0] + self.__position[0], self.__position[1] + self.__position[1]), window.events, self)
                
                # zmienna że zostało coś kliknięte
                _beenclicked = True
                
                # usuń starego focusa
                if previousFocused != None:
                    previousFocused.focused = False
                    previousFocused.focusEnd(sprite, window.events, self)
                
                # ustaw nowego
                sprite.focused = True
                sprite.focusStart(sprite, window.events, self)
                return sprite

        # gdy nie został żaden sprite kliknięty      
        if not _beenclicked:
            # wyłączanie okna (ten x)
            if self.closable and pressed[0] and self.closableRect.collidepoint(pos):
                window.removeWindow(self.__name)
                return None
            
            # usunięcie focusa gdy się kliknęło na np tło
            if previousFocused != None:
                    previousFocused.focused = False
                    previousFocused.focusEnd(sprite, window.events, self)
                
            #TODO: tu opcjonalnie można by zaimplementować poruszanie oknami
            
            return None


    def __regenerateRect(self):
        '''Służy do wygenerowania nowego recta okna (np po zmianie pozycji bądź wielkości)'''
        # sam rect okna
        self.windowRect = self.__tempSurfaceBackground.get_rect()
        self.windowRect.topleft = (self.windowRect.topleft[0] + self.__position[0],
                                     self.windowRect.topleft[1] + self.__position[1])
        
        # rect x
        self.closableRect = window.closeImg.get_rect()
        self.closableRect.topleft = (self.__size[0] + self.__position[0] - self.closableRect.size[0], 
                                      self.closableRect.topleft[1] + self.__position[1])
        
        
    def setPosition(self, position:tuple[int, int]) -> 'window':
        '''Ustawianie pozycji okna\n
            ----------------------\n
             Argumenty:\n
                * position (tuple dwóch intów) -> nowa pozycja\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)\n
        '''
        # ustaw pozycja
        self.__position = position
        # napraw recty
        self.__regenerateRect()
        # zwróc siebie
        return self
   
        
    def getPosition(self) -> tuple[int,int]:
        '''pozyskiwanie pozycji okna\n
            ----------------------\n
             Argumenty:\n
                * Brak\n
            Zwraca:\n
                * position (tuple dwóch intów, nowa pozycja)\n       
        
        '''
        return self.__position 
 
 
    def setSize(self, size:tuple[int, int]) -> 'window':
        '''Ustawianie pozycji okna\n
            ----------------------\n
             Argumenty:\n
                * position (tuple dwóch intów) -> nowa pozycja\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)\n
        '''
        # ustaw pozycja
        self.__size = size
        
        # nowy background
        self.__tempSurfaceBackground = pygame.surface.Surface(size=(size[0], size[1] + 40))
        self.__tempSurfaceBackground.fill(self.__backgroundColor)
        self.__tempSurfaceBackground = self.__tempSurfaceBackground.convert()
        
        # nowe płótno dla okna
        self.__tempSurfaceBody = pygame.surface.Surface(size=size)
        self.__tempSurfaceBody.set_colorkey(self.__backgroundColor)
        self.__tempSurfaceBody.fill(self.__backgroundColor)
        
        # napraw recty
        self.__regenerateRect()
        # zwróc siebie
        return self
    
    
    def getSize(self) -> tuple[int,int]:
        '''pozyskiwanie rozmiaru okna\n
            ----------------------\n
             Argumenty:\n
                * Brak\n
            Zwraca:\n
                * size (tuple dwóch intów, nowa pozycja)\n       
        '''
        return self.__size
    
    
    def getBody(self) -> pygame.sprite.Group | windowBody:
        '''pozyskiwanie listy spritów okna\n
            ----------------------\n
             Argumenty:\n
                * Brak\n
            Zwraca:\n
                * spriteList (pygame.sprite.Group lub windowBody)\n       
        '''
        return self.__body
    
    def addObjectToListen(self, object: windowElement):
        '''Dodawanie obiektów do nasłuchiwania\n
            ----------------------\n
             Argumenty:\n
                * object (windowELement, jaki objekt)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)\n       
        '''
        if not object in self.__objectsToListen:
            self.__objectsToListen.append(object)

        return self

    def removeObjectFromListening(self, object: windowElement):
        '''Usuwanie obiektów z nasłuchiwania\n
            ----------------------\n
             Argumenty:\n
                * object (windowELement, jaki objekt)\n
            Zwraca:\n
                * self (ten sam obiekt na którym to wywołałeś)\n       
        '''
        if object in self.__objectsToListen:
            self.__objectsToListen.remove(object)

        return self

    def __init__(self, name:str, size:tuple[int,int], body:windowBody | pygame.sprite.Group, closable:bool=False,
                 backgroundColor: tuple[int,int,int] = (195,195,195), cords: list[int, int] | tuple[int, int] | pygame.Vector2 = [0, 0]):
        '''Tworzenie nowego okna\n
            NIE PRZYPISUJ TEGO DO ŻADNEJ ZMIENNEJ\n
            by pozyskiwać okno wcześniejsze użyj window.getWindow(nazwaOkna)\n
            ---------------------------------\n
            Argumenty:\n
                * name (string, nazwa/identyfikator okna)\n
                * size (rozmiar okna, tuple dwóch intów)\n
                * body (windowBody, pygame.sprite.Group; grupa z windowElement'ami)\n
                \n
                * closable (bool, opcjonalne, czy można zamknać okno i czy wyświetlać krzyżyk do tego zamknięcia, domyślnie nie można)\n
                * backgroundColor (tuple trzech intów, rgb; opcjonalne; poprostu kolor tła, podstawowo (195,195,195))\n
                * position (tuple dwóch intów, pozycja; opcjonalne; domyślnie (0,0))
            Zwraca:\n
                * Obiekt\n       
        '''
        # sprawdzanie błędów danych
        if window.checkWindow(name):
            raise Exception(f"Okno o id {name} juz istnieje!")
        
        if size[0] <= 40 or size[1] <= 40:
            raise Exception(f"Okno {name} ma {size[0]}x{size[1]} a powinno mieć co najmniej 40x40")
        
        # podstawowe atrybuty
        self.__name = name
        self.__body = body
        self.__size = size
        self.visible = True
        self.__position = cords
        self.closable = closable
        self.__backgroundColor = backgroundColor
        
        # tło
        self.__tempSurfaceBackground = pygame.surface.Surface(size=(size[0], size[1] + 40))
        self.__tempSurfaceBackground.fill(self.__backgroundColor)
        self.__tempSurfaceBackground = self.__tempSurfaceBackground.convert()
        
        # rect
        self.__regenerateRect()
        
        # płótno dla spritów
        self.__tempSurfaceBody = pygame.surface.Surface(size=size)
        self.__tempSurfaceBody.set_colorkey(self.__backgroundColor)
        self.__tempSurfaceBody.fill(self.__backgroundColor)
        
        # lista nasłuchiwanych obiektów
        self.__objectsToListen = []
        
        # finalne dodanie okna do listy okien
        window.addWindowToList(name, self, self.__loop())