# importy
import pygame
from pygame import Vector2
import random
import asyncio

# importy lokalne
from bin.function import readJSON, updateJSON
import bin.savemanager as sm
import bin.achievements as ah
import bin.fonts as fn
import bin.util as game
import bin.pausescreen as ps

class client(pygame.sprite.Sprite):
    clientGroup = pygame.sprite.Group()
    
    
    @classmethod
    def save(cls):
        '''Służy do zapisu wszystkich klientów'''
        smv = sm.get(alwaysNew=False)
        
        smv.set("characters", [
            {
                "id": cl.id,
                "nickname": cl.nickname,
                "gender": cl.gender,
                "type": "client",
                "graphicsBody": cl.graphicsBody,
                "pos": (cl.pos.x, cl.pos.y)
            }
            for cl in cls.clientGroup.sprites()
        ])    
    
    # id
    @property
    def id(self):
        '''id klienta (służy do celów odróżnienia klientów do obliczeń, id nie można zmienić, jest generowane randomowo)'''
        return self.__id
    
    @id.setter
    def id(self, val):
        raise Exception("Nie możesz zmienić id!")
    
    # notka: niewiem czy getter jest potrzebny, ale napewno poprawia kolejność podpowiadania więc git
    @id.getter
    def id(self):
        return self.__id
    
    @id.deleter
    def id(self):
        raise Exception("Nie możesz usunąć id")
    
    
    @property
    def nickname(self):
        return self.__nickname
    
    @nickname.setter
    def nickname(self, val):
        self.newIdentity(name=val)
       
        
    @property
    def gender(self):
        return self.__gender
    
    @gender.setter
    def gender(self, val):
        self.newIdentity(gender=val)   
        
    @property
    def graphicsBody(self):
        return self.__graphicsJson
    
    @graphicsBody.setter
    def graphicsBody(self, val):
        self.newIdentity(graphicsBody=val) 
        
        
    @property
    def pos(self):
        return self.__pos
    
    @pos.setter
    def pos(self, val):
        self.__pos = val
        self.rect = self.image.get_rect()
        self.rect.topleft = self.__pos
        
        
    @classmethod
    async def __loop(cls):
        while True:
            if not ps.pauseScreen.object.getState():
            
                for client in cls.clientGroup.sprites():
                    client.selfLoop()
            await asyncio.sleep(0.05)
            
            
    @classmethod
    def startTask(cls):
        cls.clientGroup.sprites()
        cls.clientGroup.empty()
        print(cls.clientGroup.sprites())
        asyncio.create_task(cls.__loop(), name="clientManager")
        
    def selfLoop(self):
        match self.__state:
            case 'joining':
                self.pos += Vector2(10,0)
                
    
    
    def __init__(self, forceID: int|None = None, forceGender:bool|None = None, forceName: int|None = None, forceGraphicsBody: dict|None = None, pos:list = Vector2(0,280)):
        super().__init__(client.clientGroup)
        
        # pozyskanie unikalnego id
        if forceID == None:
            g = True
            while g:
                self.__id = random.randint(0,9999999)
                g = False
                for cl in client.clientGroup.sprites():
                    if cl != self and self.__id == cl.id:
                        g = True
                        break
        else:
            self.__id = forceID
            
        if forceGender == None:
            self.__gender = bool(random.randint(0,1))
        else:
            self.__gender = forceGender
            
        # imie i nazwisko
        if forceName == None:
            _temp = readJSON("./bin/clientsNames.json")
            
            _firstName = _temp['firstNames']["f" if self.__gender else "m"][random.randint(0,len(_temp['firstNames']["f" if self.__gender else "m"])-1)]
            _surname = _temp['surnames']["f" if self.__gender else "m"][random.randint(0,len(_temp['surnames']["f" if self.__gender else "m"])-1)]            
            
            self.__nickname = f"{_firstName} {_surname}"
            
            print(self.__nickname)
            
        else:
            self.__nickname = forceName
            
        
        if forceGraphicsBody == None:
            _json = readJSON("./bin/clientsGraphics.json")
            while True:
                _body = _json[random.randint(0,len(_json)-1)]
                self.__graphicsJson = _body
                if _body['forGender'] == "n": break
                elif _body['forGender'] == "m" and not self.__gender: break
                elif _body['forGender'] == "f" and self.__gender: break
                    
        else:
            self.__graphicsJson = forceGraphicsBody
            
            
        self.__graphics = {
            "idle": pygame.transform.scale(pygame.image.load(self.__graphicsJson['idle']), (25*4,61*4)).convert_alpha(),
            "disappointed": pygame.transform.scale(pygame.image.load(self.__graphicsJson['disappointed']), (25*4,61*4)).convert_alpha(),
            "leftStep": pygame.transform.scale(pygame.image.load(self.__graphicsJson['leftStep']), (25*4,61*4)).convert_alpha(),      
            "rightStep": pygame.transform.scale(pygame.image.load(self.__graphicsJson['rightStep']), (25*4,61*4)).convert_alpha(),         
        }
        
        self.image = self.__graphics['idle']
        self.rect = self.image.get_rect()
        
        self.__pos = pos
        self.rect.topleft = self.__pos
        
        
        self.__state = "joining"
        
            
        client.save()