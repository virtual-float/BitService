from typing import Any, Iterable, Union
import pygame
import asyncio

from pygame.sprite import AbstractGroup

import bin.savemanager as saveManager


class windowElement(pygame.sprite.Sprite):
    def setPosition(self, cords: list[int,int] | tuple[int,int] = [0,0]) -> None:
        self.rect.topleft = [cords[0], cords[1]]
        
    def getPosition(self) -> list[int,int]:
        return self.rect.topleft
    
    
    def setImage(self, image: pygame.surface.Surface):
        self.image = image
        
    def getImage(self) -> pygame.surface.SurfaceType:
        return self.image
    
    def __init__(self, image: pygame.surface.Surface, cords: list[int,int] | tuple[int,int] = [0,0]):
        super().__init__()
        
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = [cords[0], cords[1]]
    

# Tylko po to by mieć fajną nazwę, nie trzeba tego używać, działa identycznie jak Groupa z pygama
class windowBody(pygame.sprite.Group):
    def __init__(self, *sprites: Any | AbstractGroup | Iterable):
        super().__init__(*sprites)
        

class window():
    __windowList = {
        
    }
    
    
    @classmethod
    def removeWindow(cls, name:str) -> None:
        cls.__windowList.pop(name)
        
        for task in asyncio.all_tasks():
            if task.get_name() == f"windowLoop_{name}": task.cancel()
        
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
        asyncio.create_task(loop, name=f"windowLoop_{name}")
        
        cls.__save()
        
        
    @classmethod
    def __save(cls):
        saveManager.get(alwaysNew=False).set('gameState.windows',
                                        {
                                        name:{
                                            'position': window.getPosition(),
                                            'size': window.getSize(),
                                            'visible': window.visible,
                                            'body': {
                                                
                                            }
                                        }
                                        for name, window in cls.__windowList.items()
                                        })
    
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
        destination.blit(self.__tempSurfaceBody, (self.__position[0],40+self.__position[1]))
        
        
    
    async def __loop(self):
        await asyncio.sleep(0.1)
        
        
    def setPosition(self, position:tuple[int, int]) -> None:
        self.__position = position
        
    def getPosition(self) -> tuple[int,int]:
        return self.__position 
    
    def getSize(self) -> tuple[int,int]:
        return self.__size

    def __init__(self, name:str, size:tuple[int,int], body:windowBody | pygame.sprite.Group):
        
        # sprawdzanie błędów danych
        if window.checkWindow(name):
            raise Exception(f"Okno o id {name} juz istnieje!")
        
        if size[0] <= 40 or size[1] <= 40:
            raise Exception(f"Okno {name} ma {size[0]}x{size[1]} a powinno mieć co najmniej 40x40")
        
        self.__body = body
        self.__size = size
        self.visible = True
        self.__position = [100,100]
        
        self.__tempSurfaceBackground = pygame.surface.Surface(size=(size[0], size[1] + 40))
        self.__tempSurfaceBackground.fill((60,54,51))
        self.__tempSurfaceBackground = self.__tempSurfaceBackground.convert()
        
        self.__tempSurfaceBody = pygame.surface.Surface(size=size)
        self.__tempSurfaceBody.set_colorkey((60,54,51))
        self.__tempSurfaceBody.fill((60,54,51))
        
        
        window.addWindowToList(name, self, self.__loop())
        
        
        
    
    
# window()