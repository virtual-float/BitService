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
    gameStage = 0
    __timeForNextClient = 0
    __timeForNextClientTemplate = 25
    
    
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
                "pos": (cl.pos.x, cl.pos.y),
                "state": cl.state
            }
            for cl in cls.clientGroup.sprites()
        ])    
        
        smv.set("charactersLength", len(cls.clientGroup.sprites()))
        smv.set("queueStage", cls.gameStage)
    
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
            
                _s = sm.get(alwaysNew=False)
                match cls.gameStage:
                    # 1: oczekiwanie 6 sekund od rozpoczęcia gry na pojawienie pierwszego klienta
                    case 1:
                        if _s.getSafe('time.totalSec', default=0) > 6:
                            cls.gameStage = 2
                            
                            cls.newClientToQueue()
                
                    # dodawanie potem kolejnych 
                    case 2:
                        cls.__timeForNextClient += 1
                        if cls.__timeForNextClient >= cls.__timeForNextClientTemplate:
                            cls.__timeForNextClient = 0
                            if len(cls.clientGroup) < 3:
                                cls.newClientToQueue()
                    
                    
                            
                            
                
                
                for client in cls.clientGroup.sprites():
                    client.selfLoop()
            await asyncio.sleep(0.05)
            
    @classmethod
    def startQueue(cls):
        cls.gameStage = 1
            
    @classmethod
    def startTask(cls):
        cls.gameStage = 0
        cls.clientGroup.empty()
        asyncio.create_task(cls.__loop(), name="clientManager")
        
    def selfLoop(self):
        _m = sm.get(alwaysNew=False)
        
        match self.state:
            case 'joining':
                self.pos += Vector2(10,0)
                
                if self.image == self.__graphics['leftStepRight']:
                    self.image = self.__graphics['rightStepRight']
                else:
                    self.image = self.__graphics['leftStepRight']
                    
                if self.pos.x > self.queueXMax:
                    self.pos.x = self.queueXMax
                    if _m.getSafe("clientQueue", default=[])[0] == self.__id:
                        self.state = "awaitingFirst"
                        self.image = self.__graphics['idleRight']
                    else:
                        self.state = "awaiting"
                        self.image = self.__graphics['idleRight']
                        
                    
                
                
    @classmethod
    def newClientToQueue(cls, *args, **kwargs):
        _s = sm.get(alwaysNew=False)
        _cl = cls(*args, **kwargs)
        
        _s.set("clientQueue", [*_s.getSafe("clientQueue", default=[]), _cl.id])
                
    
    
    def __init__(self, forceID: int|None = None, forceGender:bool|None = None, forceName: int|None = None, forceGraphicsBody: dict|None = None, pos:list|None = None):
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
            "idleLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['idle']), (25*4,61*4)).convert_alpha(),
            "idleRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['idle']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(),
            "disappointedLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['disappointed']), (25*4,61*4)).convert_alpha(),
            "disappointedRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['disappointed']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(),
            "leftStepLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['leftStep']), (25*4,61*4)).convert_alpha(),      
            "leftStepRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['leftStep']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(), 
            "rightStepLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['rightStep']), (25*4,61*4)).convert_alpha(),         
            "rightStepRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['rightStep']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(),   
        }
        
        self.image = self.__graphics['leftStepRight']
        self.rect = self.image.get_rect()
        
        if pos == None:
            self.__pos = Vector2(0,4*70)
        else:
            if isinstance(pos, Vector2): self.__pos = pos
            else: self.__pos = Vector2(pos)
            
        self.rect.topleft = self.__pos
        
        
        self.state = "joining"
        
        self.queueXMax = 135 * 4 - 90 * len(client.clientGroup.sprites())
        
        print(client.clientGroup.sprites())
        client.save()
        
        # NOTKA: * 4 jest do zmiennych rozdzielczości, staram się robić by łatwo było przerobić,
        # nie wpływa to znacząco na wydajność aż tak bardzo