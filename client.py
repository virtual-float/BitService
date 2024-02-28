#################################
# client.py      
#
# Cel: ogólne zarządzanie klientami            
#################################

# importy
import pygame
from pygame import Vector2
import random
import asyncio
import abc

# importy lokalne
from bin.function import readJSON, updateJSON
import bin.savemanager as sm
import bin.achievements as ah
import bin.fonts as fn
import bin.util as game
import bin.pausescreen as ps
from bin.answerIndicator import answerIndicator

# guis
import bin.gui.gate_gui as gi
import bin.gui.bit_gui as bi
import bin.gui.net_gui as ni

class client(pygame.sprite.Sprite):
    '''Poprostu klient'''
    
    # grupy spritów które obsługują i efekty oraz samych kientów
    clientGroup = pygame.sprite.Group()
    clientEffectGroup = pygame.sprite.Group()
    clientBackEffectGroup = pygame.sprite.Group()
    
    # wartosci tymczasowe służące do obliczania stanu kolejki
    gameStage = 0
    __timeForNextClient = 0
    __timeForNextClientTemplate = 25
    
    # referencja do ekranu (praktycznie prawie nie wykorzystywana (oprócz paru rzeczy))
    screen = None
    
    
    @classmethod
    def restore(cls) -> None:
        '''Służy do odzyskania klientów z savu'''
        smv = sm.get(alwaysNew=False)
        
        # wyczyść poprzednie dane
        cls.clientEffectGroup.empty()
        cls.clientGroup.empty()
        cls.gameStage = 0
        cls.__timeForNextClient = 0
        __timeForNextClientTemplate = 25
        
        # pobierz charaktery z savu
        _char = smv.getSafe("characters", default={})
        
        if _char == {}:
            # gdy brak charakterów rozpocznij kolejkę od nowa
            cls.startNewQueue()
            
            cls.gameStage = 1
        else:
            # odzyskiwanie
            
            # przypisz ważne dane
            cls.gameStage = smv.get('queueStage', default=0)
            
            # załaduj charaktery
            for char in _char:
                cls.loadCharacter(char)
                
            # w przypadku braku gameStaga lub zerowego ustaw 1 (rzadko się to zdarza, ale zdarza)
            if cls.gameStage == 0: cls.gameStage = 1
                
    
    @classmethod
    def loadCharacter(cls, charInfo:dict) -> None:
        '''Ładowanie charakteru\n
            -------------------\n
            Argumenty:\n
            * charInfo (dict, informacje o charakterze pozyskane najczęściej z savaManagera)\n
            \n
            Zwaraca:
            * None'''
        # samo tworzenie charakteru
        _char = cls(forceID = charInfo['id'], forceGender = charInfo['gender'], forceName = charInfo['nickname'],
                    forceGraphicsBody = charInfo['graphicsBody'], pos = charInfo['pos'], tempVars = charInfo['tempVars'],
                    forceState=charInfo['state'])
        
        
        # przypisywanie danych których nie można przypisać w inicjatorze
        _char.setGraphics(charInfo['imageName'])
        _char.tempVars = charInfo['tempVars']
        _char.queueXMax = _char.tempVars['queueXMax']
        
        
        # przywoływanie spowrotem okna z pytaniem
        if _char.state == "askingDone":
            match _char.tempVars['question']['questionType']:
                case 'gate_question':
                    gi.generate_gate(_char.tempVars['question'], _char)
                case 'bit_question':
                    bi.generate_gate(_char.tempVars['question'], _char)
                case 'net_question':
                    ni.generate_gate(_char.tempVars['question'], _char)
    
    @classmethod
    def save(cls):
        '''Służy do zapisu wszystkich klientów oraz stanu kolejki'''
        smv = sm.get(alwaysNew=False)
        
        # zapis wszystkich klientów
        smv.set("characters", [
            {
                "id": cl.id,
                "nickname": cl.nickname,
                "gender": cl.gender,
                "type": "client",
                "graphicsBody": cl.graphicsBody,
                "imageName": cl.imageForJson,
                "pos": (cl.pos.x, cl.pos.y),
                "state": cl.state,
                "tempVars": cl.tempVars,
            }
            for cl in cls.clientGroup.sprites()
        ])    
        
        # dane kolejki
        smv.set("charactersLength", len(cls.clientGroup.sprites()))
        smv.set("queueStage", cls.gameStage)
    
    #################
    # parametry
    #################
    
    
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
    
    # nickname
    
    @property
    def nickname(self):
        return self.__nickname
    
    @nickname.setter
    def nickname(self, val):
        self.newIdentity(name=val)
       
    # gender
        
    @property
    def gender(self):
        return self.__gender
    
    @gender.setter
    def gender(self, val):
        self.newIdentity(gender=val)   
        
    # graphicsBody
        
    @property
    def graphicsBody(self):
        return self.__graphicsJson
    
    @graphicsBody.setter
    def graphicsBody(self, val):
        self.newIdentity(graphicsBody=val) 
        
        
    # @property
    # def pos(self):
    #     return self.pos
    
    # @pos.setter
    # def pos(self, val):
    #     self.pos = val
    #     self.rect = self.image.get_rect()
    #     self.rect.topleft = self.pos
     
    
        
    @classmethod
    async def __loop(cls):
        '''Prywatna metoda; nie powinna być wywoływana ręcznie;pętla ogólna kolejki'''
        while True:
            # sprawdzanie czy pausescreen jest włączony
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
                            if len(cls.clientGroup) < 7:
                                cls.newClientToQueue()
                    
                    
                            
                            
                
                # wywoływanie selfLoopa dla każdego klienta
                for client in cls.clientGroup.sprites():
                    client.selfLoop()
                
                # to samo co powyżej, tylko że dla klientów z tyłu (szczerze, nie jest to używane,
                # ale nie wpływa prawie w żadeń sposób na performance, więc zostanie to usunięte dopiero gdy
                # będzie się szukać dość mocno fpsów;
                # albowiem według mnie to może zaoszczędzić wiele czasu w przyszłości)
                for ef in filter(lambda obj: isinstance(obj, client), cls.clientBackEffectGroup):
                    ef.selfLoop()
                    
            await asyncio.sleep(0.05)
            
    @classmethod
    def startNewQueue(cls) -> None:
        '''Rozpoczęcie nowej kolejki (nie usuwa danych, tylko zaczyna ją)'''
        cls.gameStage = 1
            
    @classmethod
    def startTask(cls, screen: pygame.surface.Surface | None = None) -> None:
        '''Rozpoczęcie tasku wymaganego dla client.py\n
        ----------------------\n
        Argumenty:\n
        * screen (pygame.surface.Surface; miejsce rysowania klientów)\n
        \n
        Zwraca:\n
        * None'''
        # screenek
        if screen == None:
            cls.screen = pygame.display.get_surface()
        else:
            cls.screen = screen
        
        # podstawowe dane
        cls.gameStage = 0
        cls.clientGroup.empty()
        cls.clientEffectGroup.empty()
        asyncio.create_task(cls.__loop(), name="clientManager")
        
    def setGraphics(self, name:str) -> None:
        '''Ustawienie grafiki klienta z tego co ma w sobie zapisane\n
        ------------------\n
        Argumenty:\n
        * name (str, nazwa grafiki)\n
        \n
        Zwraca:\n
        * None'''
        if not name in self.__graphics:
            raise Exception(f"Błąd z grafiką w kliencie id {self.id}, nieznaleziono grafiki o nazwie {name}")
        
        self.image = self.__graphics[name]
        
    def selfLoop(self):
        '''20Hz, wykonuje sie 20 razy na sekunde\n
        wewnętrzna pętla klienta, nie tykać'''
        # 20Hz, wykonuje sie 20 razy na sekunde
        _m = sm.get(alwaysNew=False)
        
        # naprawienie recta
        self.rect.topleft = self.pos
        
        # pobranie pozycji
        _pos = (
            pygame.mouse.get_pos()[0] * (client.screen.get_size()[0] / pygame.display.get_surface().get_size()[0]),
            pygame.mouse.get_pos()[1] * (client.screen.get_size()[1] / pygame.display.get_surface().get_size()[1])
        )
        
        # tekst nad klientem
        if self.rect.collidepoint(_pos):
            clientTextEffect(self)
        
        # obsługa stanów
        match self.state:
            # idzie zając swoje miejsce
            case 'joining':
                self.pos += Vector2(10,0)
                
                if self.image == self.__graphics['leftStepRight']:
                    self.image = self.__graphics['rightStepRight']
                    self.imageForJson = 'rightStepRight'
                else:
                    self.image = self.__graphics['leftStepRight']
                    self.imageForJson = 'leftStepRight'
                    
                if self.pos.x > self.queueXMax:
                    self.pos.x = self.queueXMax
                    if _m.getSafe("clientQueue", default=[])[0] == self.__id:
                        self.state = "awaitingFirst"
                        self.tempVars["awaitingFirstTime"] = 0
                        self.imageForJson = 'idleRight'
                        self.image = self.__graphics['idleRight']
                    else:
                        self.state = "awaiting"
                        self.imageForJson = 'idleRight'
                        self.image = self.__graphics['idleRight']
                 
            # czeka jako pierwszy w kolejce już w miejscu       
            case 'awaitingFirst':
                self.tempVars["awaitingFirstTime"] = self.tempVars.get("awaitingFirstTime") + 1
                
                if self.tempVars["awaitingFirstTime"] > 60:
                    self.state = "asking"
            
            # pyta o coś
            case 'asking':
                questionType = random.choice(["gate_question","bit_question", "net_question"])
                
                match questionType:
                    case 'gate_question':
                        questions = readJSON("./bin/quests/gate_question.json")
                        newQuestion = questions[random.randint(0, len(questions)-1)]
                        gi.generate_gate(newQuestion, self)
                    case 'bit_question':
                        questions = readJSON("./bin/quests/bit_question.json")
                        newQuestion = questions[random.randint(0, len(questions)-1)]
                        bi.generate_gate(newQuestion, self)
                    case 'net_question':
                        questions = readJSON("./bin/quests/net_question.json")
                        newQuestion = questions[random.randint(0, len(questions)-1)]
                        ni.generate_gate(newQuestion, self)
                
                self.tempVars['question'] = {
                    "questionType": questionType,
                    **newQuestion
                }
                
                # gi.generate_gate(newQuestion, self)
                
                self.tempVars['angryLevel'] = 0
                self.state = 'askingDone'
                
            # skończył pytać
            case 'askingDone':
                self.tempVars['angryLevel'] += 1
               
            # wychodzi wkurzony 
            case 'leavingAngry':
                self.pos -= Vector2(10,10)
                
                
                self.tempVars['leavingStageOne'] += 1
                if self.tempVars['leavingStageOne'] >= 6:
                    _m.get("clientQueue", default=[]).remove(self.id)
                    self.state = 'leavingAngry2'
                
            # kończy wychodzic wkurzony    
            case 'leavingAngry2':
                self.pos -= Vector2(10,0)
                
                
                if self.pos.x < -80:
                    self.kill()

            # wychodzi szczęśliwy
            case 'leavingHappy':
                self.pos -= Vector2(10,10)
                
                
                self.tempVars['leavingStageOne'] += 1
                if self.tempVars['leavingStageOne'] >= 6:
                    _m.get("clientQueue", default=[]).remove(self.id)
                    self.state = 'leavingHappy2'
                    
            # kończy wychodzić szczęśliwy
            case 'leavingHappy2':
                self.pos -= Vector2(10,0)
                
                
                if self.pos.x < -80:
                    self.kill()                    

            # oczekuje aż dostanie role (w kolejce)
            case 'awaiting':
                self.__regenerateXMax()
                if self.pos.x != self.queueXMax:
                    self.state = "joining"
                    self.__regenerateXMax()
                    
                
                
        # zapisz wszystko do savu 
        self.save()        
    
    def __regenerateXMax(self) -> None:
        '''Metoda prywatna; Ustala miejsce w kolejce'''
        _sm = sm.get(alwaysNew=False)
        
        try:
            self.queueXMax = 150 * 4 - 90 * (_sm.get("clientQueue", default=[]).index(self.id)+1)
        except:
            self.queueXMax = 150 * 4 - 90 * (len(_sm.get("clientQueue", default=[]))+1)
            
        self.tempVars['queueXMax'] = self.queueXMax

    def wrongAnswer(self) -> None:   
        '''Przekaż że gracz udzielił złej odpowiedzi'''
        
        self.state = 'leavingAngry'
        self.tempVars['as'] = 'backEffect'
        self.tempVars['leavingStageOne'] = 0
        self.setGraphics('disappointedLeft')
        self.imageForJson = 'disappointedLeft'
        self.save()      
        
        # indicator
        answerIndicator(status=False)
        
    def correctAnswer(self) -> None:
        '''Przekaż że gracz udzielił poprawnej odpowiedzi'''
        
        self.state = 'leavingHappy'
        self.tempVars['as'] = 'backEffect'
        self.tempVars['leavingStageOne'] = 0
        self.setGraphics('happyLeft')
        self.imageForJson = 'happyLeft'
        self.save()            
        
        # indicator
        answerIndicator()
                
                
    @classmethod
    def newClientToQueue(cls, *args, **kwargs) -> None:
        '''Dodaje nowego klienta'''
        _s = sm.get(alwaysNew=False)
        _cl = cls(*args, **kwargs)
        
        _s.set("clientQueue", [*_s.getSafe("clientQueue", default=[]), _cl.id])
                
    
    
    def __init__(self, forceID: int|None = None, forceGender:bool|None = None, forceName: int|None = None, forceGraphicsBody: dict|None = None, pos:list|None = None, tempVars:dict={}, forceState:str="joining"):
        super().__init__(client.clientGroup)
        
        self.tempVars = {}
        
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
            
        # płeć
        if forceGender == None:
            self.__gender = bool(random.randint(0,1))
        else:
            self.__gender = forceGender
            
        # imie i nazwisko
        if forceName == None:
            _temp = readJSON("./bin/clientsNames.json")
            
            _firstName = _temp['firstNames'][1 if self.__gender else 0][random.randint(0,len(_temp['firstNames'][1 if self.__gender else 0])-1)]
            _surname = _temp['surnames'][1 if self.__gender else 0][random.randint(0,len(_temp['surnames'][1 if self.__gender else 0])-1)]            
            
            self.__nickname = f"{_firstName} {_surname}"
            
            print(self.__nickname)
            
        else:
            self.__nickname = forceName
            
        # grafika
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
            
        # wczytanie grafiki z plików
        self.__graphics = {
            "idleLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['idle']), (25*4,61*4)).convert_alpha(),
            "idleRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['idle']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(),
            "disappointedLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['disappointed']), (25*4,61*4)).convert_alpha(),
            "disappointedRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['disappointed']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(),
            "leftStepLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['leftStep']), (25*4,61*4)).convert_alpha(),      
            "leftStepRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['leftStep']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(), 
            "rightStepLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['rightStep']), (25*4,61*4)).convert_alpha(),         
            "rightStepRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['rightStep']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(),   
            "happyLeft": pygame.transform.scale(pygame.image.load(self.__graphicsJson['happy']), (25*4,61*4)).convert_alpha(),         
            "happyRight": pygame.transform.scale(pygame.transform.flip(pygame.image.load(self.__graphicsJson['happy']),flip_x=True, flip_y=False), (25*4,61*4)).convert_alpha(),   
        }
        
        # rect oraz finalne załadowanie grafiki
        self.image = self.__graphics['leftStepRight']
        self.imageForJson = 'leftStepRight'
        self.rect = self.image.get_rect()
        
        # pozycja
        if pos == None:
            self.pos = Vector2(-100,4*70+ 4 * random.randint(0,8))
        else:
            if isinstance(pos, Vector2): self.pos = pos
            else: self.pos = Vector2(pos)
            
        self.rect.topleft = self.pos
        
        # stan klienta
        self.state = forceState
        self.stateName = False
        
        # pozycja klienta w kolejce
        self.__regenerateXMax()
        
        # print(client.clientGroup.sprites())
        # zapisanie do sava
        client.save()
        
        # NOTKA: * 4 jest do zmiennych rozdzielczości, staram się robić by łatwo było przerobić,
        # nie wpływa to znacząco na wydajność aż tak bardzo
        
class clientEffect(pygame.sprite.Sprite, abc.ABC):
    '''Klasa abstrakcyjna do efektów'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class clientTextEffect(clientEffect):
    '''nickname nad głową; efekt'''
    async def __loop(self):
        while True:
            self.__generateRect()
            
            _pos = (
                pygame.mouse.get_pos()[0] * (client.screen.get_size()[0] / pygame.display.get_surface().get_size()[0]),
                pygame.mouse.get_pos()[1] * (client.screen.get_size()[1] / pygame.display.get_surface().get_size()[1])
            )
            
            print(_pos)
            
            if (not self.client.rect.collidepoint(_pos)) or ps.pauseScreen.object.getState():
                self.client.stateName = False
                self.kill()
                break
            
            await asyncio.sleep(0.05)
    
    def __generateRect(self):
        self.rect.center = (self.client.pos.x + self.client.rect.width / 2, self.client.pos.y - 1.5 * 4)
    
    def __init__(self, client: client):
        if client.stateName: return
        
        client.stateName = True
        self.client = client
        
        
        
        super().__init__(client.clientEffectGroup)
        
        self.image = fn.getfonts()['TINY_COMICSANS'].render(client.nickname, False, (0,0,0))
        self.rect = self.image.get_rect()
        self.__generateRect()
        
        asyncio.create_task(self.__loop(), name=f"clientTextEffectName_{client.id}")
        