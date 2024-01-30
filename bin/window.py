from typing import Any, Iterable, Union
import pygame
import asyncio
import abc

from pygame.sprite import AbstractGroup

import bin.savemanager as saveManager
import bin.fonts as fn
import bin.pausescreen as psc


# helloWorld = print
# print = 'Hello World'

# helloWorld(print)

        

class windowElement(pygame.sprite.Sprite):
    def focusLoop(self, keys): 
        pass
    
    def focusEnd(self):
        pass
    
    def focusStart(self):
        pass
    
    def setPosition(self, cords: list[int,int] | tuple[int,int] = [0,0]) -> None:
        self.rect.topleft = [cords[0], cords[1]]
        
    def getPosition(self) -> list[int,int]:
        return self.rect.topleft
    
    
    def setImage(self, image: pygame.surface.Surface):
        self.image = image.convert_alpha()
        
    def getImage(self) -> pygame.surface.SurfaceType:
        return self.image
    
    def click(self, pressed:tuple[bool], pos:tuple[int]) -> bool:
        pass
        
    def addClickListener(self, function:object=lambda pressed, pos: False):
        self.click = function
        return self
    
    def __init__(self, image: pygame.surface.Surface, cords: list[int,int] | tuple[int,int] = [0,0]):
        super().__init__()
        
        self.image = image.convert_alpha()
        self.rect = image.get_rect()
        self.rect.topleft = [cords[0], cords[1]]
        self.focused = False
        self.autoListen = False

    
class windowText(windowElement):
    def __init__(self, fontName:str, text:str, cords: list[int,int] | tuple[int,int], color:tuple[int] = (0,0,0)):
        self.__fontName, self.__color = fontName, color
        _fn = fn.getfonts()
        self.__font = _fn[fontName]
        _img = self.__font.render(text, False, color).convert_alpha()
        super().__init__(_img, cords)    


class windowTextBox(windowElement):
    def focusLoop(self, events):
        if len(self.__displayText) == len(self.text):
            self.__displayText = self.text + "|"
        else:
            self.__displayText = self.text
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.__returnText(self.text)
                    self.text = ""
                elif event.key != pygame.K_ESCAPE:
                    self.text += event.unicode
        
        self.__renderText()
    
    def focusEnd(self):
        self.__displayText = self.text
        self.__renderText()
        
    def setReturnListener(self, function: object = lambda text: 0):
        self.__returnText = function
        return self
        
    def __returnText(self, text:str): 
        self.text = text
    
    def __renderText(self):
        self.__textImg = self.__font.render(self.__displayText, False, self.__color).convert_alpha()
        self.image = self.__textImg
        
    def __init__(self, cords: list[int] | tuple[int, int] = [0, 0], startingText:str="", xsize:int=10, fontName:str="SMALL_COMICSANS", color:tuple[int,int,int] = (0,0,0)):
        self.__fontName, self.__color = fontName, color
        self.__xsize, self.text = xsize, startingText
        self.__displayText = startingText
        
        _fn = fn.getfonts()
        self.__font = _fn[fontName]
        
        self.__renderText()
        
        super().__init__(self.__textImg, cords)

# Tylko po to by mieć fajną nazwę, nie trzeba tego używać, działa identycznie jak Groupa z pygama
class windowBody(pygame.sprite.Group):
    def __init__(self, *sprites: Any | AbstractGroup | Iterable):
        super().__init__(*sprites)
        

class window():
    closeImg = pygame.image.load('bin/images/close.png')
    
    isconfigured = False
    
    __windowList = {
        
    }
    
    __windowOrder = []
    
    __focusedElement = None
    
    events = None
    
    
    @classmethod
    def removeFocus(cls):
        if cls.__focusedElement != None:
            cls.__focusedElement.focused = None
            cls.__focusedElement.focusEnd()
        cls.__focusedElement = None
    
    @classmethod
    def sendEvents(cls, events):
        cls.events = events
        
    
    @classmethod
    def startTask(cls) -> None:
        asyncio.create_task(cls.__globalLoop(), name=f"windowManager")
    
    @classmethod
    async def __globalLoop(cls) -> None:
        while True:
            if psc.pauseScreen.object.getState(): 
                await asyncio.sleep(0.02)
                continue
            
            try:
                _pres = pygame.mouse.get_pressed()
            except: 
                return
            if any(_pres):
                _pos = pygame.mouse.get_pos()
                _foundWindow = False
                
                for name in cls.__windowOrder:
                    window = cls.__windowList[name]
                    
                    if window.windowRect.collidepoint(_pos):
                        if cls.__focusedElement != None and not cls.__focusedElement in window.getBody().sprites():
                            cls.__focusedElement.focused = False
                            cls.__focusedElement.focusEnd()
                            cls.__focusedElement = None
                   
                        
                        cls.__focusedElement = window.handleClick(_pres,_pos, cls.__focusedElement)
                        _foundWindow = True
                        break     
                    
                if not _foundWindow and cls.__focusedElement != None: 
                    cls.__focusedElement.focused = False
                    cls.__focusedElement.focusEnd()
                    cls.__focusedElement = None
            await asyncio.sleep(0.02)
            
    
    @classmethod
    def eraseWindows(cls) -> None:
        for name,window in cls.windowList().items():
            cls.removeWindow(name)
            
            
    @classmethod
    def removeWindow(cls, name:str) -> None:
        if cls.__focusedElement in cls.__windowList[name].getBody().sprites():
            cls.__focusedElement.focused = False
            cls.__focusedElement = None
        
        cls.__windowList.pop(name)
        
        for task in asyncio.all_tasks():
            if task.get_name() == f"windowLoop_{name}": task.cancel()
        
        cls.__windowOrder.remove(name)
        cls.__save()    
        
    @classmethod
    def getWindow(cls, name:str) -> 'window': 
        return cls.__windowList[name]
    
    @classmethod
    def checkWindow(cls, name:str) -> bool:
        return True if name in cls.__windowList else False
    
    @classmethod
    def windowList(cls) -> dict:
        return cls.__windowList.copy()
    
    @classmethod
    def addWindowToList(cls, name:str, window:'window', loop:asyncio.coroutine) -> None:
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
        _s = saveManager.get(alwaysNew=False)
        
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
        for window in cls.__windowList.values():
            if window.visible:
                window.drawSelf(destination)
                
                
    
    def drawSelf(self, destination:pygame.surface.Surface) -> None:
        self.__tempSurfaceBody.fill((60,54,51))
        self.__body.draw(surface=self.__tempSurfaceBody)
        
        destination.blit(self.__tempSurfaceBackground, (self.__position[0],self.__position[1]))
        if self.closable:
            destination.blit(window.closeImg, (self.__size[0] + self.__position[0] - 30,5 + self.__position[1]))
        destination.blit(self.__tempSurfaceBody, (self.__position[0],40+self.__position[1]))
        
        
    
    async def __loop(self):
        while True:
            if psc.pauseScreen.object.getState(): 
                await asyncio.sleep(0.02)
                continue
            
            keys = pygame.key.get_pressed()
            
            for element in self.__objectsToListen:
                if element.focused:
                    element.focusLoop(window.events)
                    break
                
            await asyncio.sleep(0.05)
        
    def handleClick(self, pressed: tuple[bool], pos: tuple[int], previousFocused) -> None | pygame.sprite.Sprite:
        # ta zmienna niewiem czy nie zostanie usunięta, bo jej sens jest aktualnie nie istniejący przez to że
        # returna się używa, ale zostawiam by jakby co można było łatwo przerobić kod
        # dodane przy okazji dodawania focusu na dany element
        _beenclicked = False
        
        for sprite in self.__body.sprites():
            _temp_rect = sprite.rect.copy()
            _temp_rect.topleft = (
                _temp_rect.topleft[0] + self.__position[0],
                _temp_rect.topleft[1] + self.__position[1] + 40
            )
            
            if _temp_rect.collidepoint(pos):
                sprite.click(pressed, pos)
                _beenclicked = True
                
                if previousFocused != None:
                    previousFocused.focused = False
                    previousFocused.focusEnd()
                
                sprite.focused = True
                sprite.focusStart()
                
                return sprite

                
        if not _beenclicked:
            # wyłączanie okna
            if self.closable and pressed[0] and self.closableRect.collidepoint(pos):
                window.removeWindow(self.__name)
                return None
            
            if previousFocused != None:
                    previousFocused.focused = False
                    previousFocused.focusEnd()
            return None
                
            #TODO: tu opcjonalnie można by zaimplementować poruszanie oknami

    def __regenerateRect(self):
        self.windowRect = self.__tempSurfaceBackground.get_rect()
        self.windowRect.topleft = (self.windowRect.topleft[0] + self.__position[0],
                                     self.windowRect.topleft[1] + self.__position[1])
        
        self.closableRect = window.closeImg.get_rect()
        self.closableRect.topleft = (self.__size[0] + self.__position[0] - self.closableRect.size[0], 
                                      self.closableRect.topleft[1] + self.__position[1])
        
    def setPosition(self, position:tuple[int, int]) -> None:
        self.__position = position
        
        self.__regenerateRect()
        
    def getPosition(self) -> tuple[int,int]:
        return self.__position 
    
    def getSize(self) -> tuple[int,int]:
        return self.__size
    
    def getBody(self) -> pygame.sprite.Group | windowBody:
        return self.__body
    
    def addObjectToListen(self, object: windowElement):
        if not object in self.__objectsToListen:
            self.__objectsToListen.append(object)

        return self

    def removeObjectFromListening(self, object: windowElement):
        if object in self.__objectsToListen:
            self.__objectsToListen.remove(object)

        return self

    def __init__(self, name:str, size:tuple[int,int], body:windowBody | pygame.sprite.Group, closable:bool=False):
        
        # sprawdzanie błędów danych
        if window.checkWindow(name):
            raise Exception(f"Okno o id {name} juz istnieje!")
        
        if size[0] <= 40 or size[1] <= 40:
            raise Exception(f"Okno {name} ma {size[0]}x{size[1]} a powinno mieć co najmniej 40x40")
        
        self.__name = name
        self.__body = body
        self.__size = size
        self.visible = True
        self.__position = [0,0]
        self.closable = closable
        
        self.__tempSurfaceBackground = pygame.surface.Surface(size=(size[0], size[1] + 40))
        self.__tempSurfaceBackground.fill((60,54,51))
        self.__tempSurfaceBackground = self.__tempSurfaceBackground.convert()
        
        self.__regenerateRect()
        
        self.__tempSurfaceBody = pygame.surface.Surface(size=size)
        self.__tempSurfaceBody.set_colorkey((60,54,51))
        self.__tempSurfaceBody.fill((60,54,51))
        
        self.__objectsToListen = []
        
        window.addWindowToList(name, self, self.__loop())
        
        
        
    
    
# window()