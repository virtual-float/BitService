#################################
# savemanager.py      
#
# Cel: zarzadzanie savem i czasem gry oraz jej eventami          
#################################


# importy ogólne
from tkinter import messagebox
import json
import asyncio
import time
import pygame
import os
from dataclasses import dataclass

# importy wewnętrzne
import bin.function as fc
import bin.window as wn
import bin.pausescreen as ps

@dataclass
class eventTimeStamp:
    hour: int
    minute: int
    second: int

@dataclass
class gameEvent:
    name: str
    time: eventTimeStamp
    useNumber: int
    callback: object

SAVECANCELPROCEDURE = "SM_ERR_CANCEL"
    

class save:
    currentSave = None
    
    '''Save gry'''
    def save(self, notMakingSure:bool=False, showInfo:bool=True) -> bool:
        '''Ręczne zapisywanie stanu gry\n
            --------------\n
            Argumenty:\n
                * Brak\n
            Zwraca:\n
                * Bool (czy się udało)'''
        # wiem że to troche lenistwo że wyświetlam to za pomocą osiągnieć
        # informacja o zapisywaniu gry
        import bin.achievements as ach
        if ach.achievement.screen != None and showInfo: 
            try:
                _zapAch = ach.achievement("Zapisuję grę...")
            except: pass


        # naprawa folderu jakby co
        os.makedirs(os.getcwd() + "/data/", exist_ok=True)

        # aktualnianie informacji
        if not notMakingSure:
            wn.window.makeSureToBeUpToDate()
        
        
        self.set("lastGame", time.time_ns())
        self.set("lastVersion", 10000)
        self.set("checkSum", 0)
         
        # checksum
        _check = 0
        for _value in fc.NestedDictValues(json.loads(json.dumps(self.__save))):
            _check += int.from_bytes(str(_value).encode('utf-8'), 'little')
            
        _check = ((_check % 10000000000000000) + (_check % 2856 * 4) + _check) % 10000000000000000
        
            
        self.set("checkSum", _check)
            
        
        # sam zapis gry
        _info = fc.updateJSON(self.__fileSave, self.__save)
        
        # informacja o końcu zapisu gry (i usunięcie jakby co informacji o zapisywaniu)
        if ach.achievement.screen != None and showInfo:
            try:
                ach.achievement.achievementShown.remove(_zapAch)
                del(_zapAch)
                if ach.achievement.screen != None: ach.achievement("Gra zapisana!")
            except: pass
        
        # zwrócenie stanu czy się udało
        return _info
    
    def set(self, loc: str, value) -> bool:  
        '''Pozwala ustawić daną wartość w save\n
            Przykład użycia dla uzyskania imienia gracza:\n
            set("player.nickname", 'janusz')\n
            --------------\n
            Argumenty:\n
                * loc (typ: str) (lokalizacja)\n
                * wartość\n
            Zwraca:\n
                * Bool (czy się udało)'''
        _loctList = loc.split(".")
        _pointer = self.__save
        
        if "".join(_loctList) == "":
            self.__save = value
        
        _last = _loctList.pop()
        
        for where in _loctList:
            try:
                _pointer = _pointer[where]
            except:
                _pointer[where] = {}
                _pointer = _pointer[where]
            
        _pointer[_last] = value
                  
        return True
    
    
    def getSafe(self, loc:str, default = {"error":True, "errorMessage": "pathError"}) -> any:
        '''Nie wyświetla komunikatu błądu\n
            Użyj jeśli nie masz pewności że coś istnieje w save\n
            ---------------------------\n
            Pozwala uzyskać daną wartość w save\n
            Przykład użycia dla uzyskania imienia gracza:\n
            getSafe("player.nickname", default="Nieznajomy")\n
            --------------\n
            Argumenty:\n
                * loc (typ: str) (lokalizacja)\n
                * default (domyślna wartość gdy nie znajdzie)\n
            Zwraca:\n
                * wartość / Bool (False)'''
                
                
        _loctList = loc.split(".")
        _pointer = self.__save
        
        if "".join(_loctList) == "":
            return _pointer
        
        try:
            for where in _loctList:
                _pointer = _pointer[where]
        except:
            _pointer = default
                  
        return _pointer
            
            
    def exist(self, loc:str) -> bool:
        '''Pozwala sprawdzić daną wartość czy istnieje w save\n
            Przykład użycia dla uzyskania imienia gracza:\n
            exist("player.nickname")\n
            --------------\n
            Argumenty:\n
                * loc (typ: str) (lokalizacja)\n
            Zwraca:\n
                * Bool'''
        _loctList = loc.split(".")
        _pointer = self.__save
        
        if "".join(_loctList) == "":
            return True
        
        try:
            for where in _loctList:
                _pointer = _pointer[where]
        except:
            return False
        
        return True
    
             
    def get(self, loc:str = "", default = {"error":True, "errorMessage": "pathError"}) -> any:
        '''Pozwala uzyskać daną wartość w save\n
            Przykład użycia dla uzyskania imienia gracza:\n
            get("player.nickname")\n
            --------------\n
            Argumenty:\n
                * loc (typ: str) (lokalizacja)\n
                * default (domyślna wartość gdy nie znajdzie)\n
            Zwraca:\n
                * wartość'''
        _loctList = loc.split(".")
        _pointer = self.__save
        
        if "".join(_loctList) == "":
            return _pointer
        
        try:
            for where in _loctList:
                _pointer = _pointer[where]
        except:
            messagebox.showerror('Dostępność', f"Savemanager nie może uzyskać dostępu do '{loc}'")
            _pointer = default
                    
        return _pointer
    
    
    def erase(self) -> None:
        '''
            Czyści save do stanu początkowego\n
            Argumenty:\n
                * Brak\n
            Zwraca:\n
                * None\n
        '''
        self.__save = self.__pattern.copy()
        print(time.time_ns())
        self.set('firstRun', time.time_ns())
        
        
    def getGameTime(self) -> dict:
        '''
            Pozyskuje czas sava\n
            Argumenty:\n
                * Brak\n
            Zwraca:\n
                * Dict\n
        '''
        return self.get("time")
    
    def resetGameTime(self, notTotalSeconds:bool=False) -> None:
        '''
            Czyści czas save'a do stanu początkowego\n
            Argumenty:\n
                * notTotalSeconds (bool) -> Ustala czy zresertować też łaczną liczbę sekund\n
            Zwraca:\n
                * None\n
        '''
        if notTotalSeconds: _ts = self.get("time.totalSec")
        
        self.set("time",
                 self.__pattern['time'])
        
        if notTotalSeconds: self.set("time.totalSec", _ts)
        
    def getGameEvents(self):
        return self.__events
    
    def newEvent(self, time: eventTimeStamp, name:str, useNumber: int):
        def _newEvent(func):
            self.addGameEvent(gameEvent(name, time, useNumber, func))
            
        return _newEvent

    def addGameEvent(self, event: gameEvent):
        self.__events.append(event)
        self.get('gameState.lastEvents').append(
            {
                'name': event.name,
                'time': {
                    'hour': event.time.hour,
                    'minute': event.time.minute,
                    'second': event.time.second
                    },
                'useNumber': event.useNumber
            }
        )
        
        
    async def __eventManager(self):
        while True:
            await asyncio.sleep(0.1) 
        
    async def __autoSave(self):
        while True:
            await asyncio.sleep(self.__saveTime)
            self.save()
            
    async def __addSec(self):
        while True:
            await asyncio.sleep(1)
            
            # totalSec
            self.set('time.totalSec', self.get('time.totalSec')+1)
            

    async def __gameClock(self):
        while True:
            await asyncio.sleep(0.075)
            if ps.pauseScreen.object.getState(): continue
            # second
            self.set('time.second', self.get('time.second')+1)
            if self.get('time.second') > 60:
                self.set('time.second', 0)
                self.set('time.minute', self.get('time.minute')+1)
                
            # minutes
            if self.get('time.minute') > 60:
                self.set('time.minute', 0)
                self.set('time.hour', self.get('time.hour')+1)

            # hour
            if self.get('time.hour') > 24:
                self.set('time.hour', 0)
                self.set('time.day', self.get('time.day')+1)
                        
            
        
    def __init__(self, file:str="./data/save.json", pattern:str="./bin/savePattern.json", saveTime:int=10, saveToCurrent:bool=True, tasks:bool=True):
        self.__fileSave, self.__patternSave, self.__saveTime = file, pattern, saveTime
        
        self.__events = []


        self.__pattern = fc.readJSON(self.__patternSave)
        if self.__pattern == {}:
            raise Exception("Błąd wczytywania wzóru zapisu")
        
        
        if os.path.isfile(os.getcwd() + self.__fileSave):
            self.__save = fc.readJSON(self.__fileSave)
            if self.__save == {}:
                messagebox.showwarning("Savamanager", "Nie można zdekodować nawet sava. Automatycznie został utworzony nowy save. Jeśli uważasz że to nie właściwe, to nie zapisuj gry!")
        else: self.__save = {}
        
        
        if self.__save == {}:
            self.erase()
        else:
            # checksum
            _previousCheck = self.get('checkSum')
            self.set("checkSum", 0)
         
            _check = 0
            for _value in fc.NestedDictValues(self.__save):
                _check += int.from_bytes(str(_value).encode('utf-8'), 'little')
                
            _check = ((_check % 10000000000000000) + (_check % 2856 * 4) + _check) % 10000000000000000
            
            self.set("checkSum", _previousCheck)
            
            _err = False
            
            
            # sprawdzanie danych
            if self.get("type", default="notsave") == "save" and self.get("game", default="notsave") == "bitservice":
                if self.get("player.ratiolevel", default={}) == {}: _err = True
                if self.get("gameState", default="e") == "e": _err = True
                if self.get("orginVersion", default={}) == {}: _err = True
                if self.get("log", default={}) == {}: _err = True
                if self.get("lastVersion", default={}) == {}: _err = True
                if self.get("devmode", default={}) == {}: _err = True
                if self.get("everdevmode", default={}) == {}: _err = True
                if self.get("time", default={}) == {}: _err = True
                if self.get("characters", default="e") == "e": _err = True
            else: _err = True
            
            if self.getSafe("game", default="notsave") != "bitservice":
                 messagebox.showwarning('Suma kontrolna', "Istneje podejrzenie że ten save jest do innej gry!")
                 
            if self.getSafe("type", default="notsave") != "save":
                 messagebox.showwarning('Suma kontrolna', "Istneje podejrzenie że to nie jest save!")
                
            
            self.set("lastVersion", 10000)
            
            
            if (_previousCheck != _check) or _err:
                # # informacja do logów
                # self.set("log", self.getSafe("log", default=[]))
                
                messagebox.showwarning('Suma kontrolna', "Istneje podejrzenie że save został uszkodzony!")
                _choice = messagebox.askyesnocancel("Suma kontrolna", "Czy spróbować przywrócic sava? (Nie = Utworzenie nowego, anulowanie = wyjście z gry, miej pod uwagą to że przywrócony save może nie być stabilny i powodować crashe)")
                
                match _choice:
                    case None:
                        # pygame.quit()
                        global SAVECANCELPROCEDURE
                        self.set("ERROR", SAVECANCELPROCEDURE)
                    case False:
                        self.erase()
                    case True:
                        # najpierw dodanie tego czego nie ma w save
                        for element, key in self.__pattern.items():
                            if element not in self.__save:
                                self.set(element, key)
                                
                        # naprawianie podstawowych informacji
                        self.set("type", "save")
                        self.set("game", "bitservice")
                        
                        # postacie
                        # nie robie przywracania dla bezpieczeństwa
                        # for id, char in enumerate(self.get("characters")):
                        #     if self.getSafe(f"characters.{id}.nickname", default="ERR") == "ERR":
                        #         self.set(f"characters.{id}.nickname", "Brak nazwy")
                                
                        #     if self.getSafe(f"characters.{id}.nickname", default="ERR") == "ERR":
                        #         self.set(f"characters.{id}.nickname", "Brak nazwy")
                            
                            
                        # TODO: funkcja naprawiająca i sprawdzająca poprawność danych może kiedyś
                        
                
            # self.save(notMakingSure=True)
                
                
                
        # wyczyść aktualny stan gry
        self.set('gameState', {
            'lastEvents': []
        })
        
        # autozapis
        if tasks:
            loop = asyncio.get_event_loop()
            loop.create_task(self.__autoSave(), name="saveManager")
        
        # zegar gry
            loop.create_task(self.__addSec(), name="saveManagerSec")
            loop.create_task(self.__gameClock(), name="gameClock")
            loop.create_task(self.__eventManager(), name="eventManager")
            
        if saveToCurrent:
            save.currentSave = self
            
            
        # autozapis
        # async def auto():
        #     print("g")
        #     while True:
        #         asyncio.sleep(1)
        #         self.save()
        #         print("save")
                
        # asyncio.run_coroutine_threadsafe(coro=auto, loop=asyncio.get_event_loop())
        # print(asyncio.get_event_loop())
        # asyncio.create_task(asyncio.get_event_loop)
        # asyncio.ensure_future(auto)
        # await auto()


        
        
        
        
        
        
        
        
        
def get(file="./data/save.json", pattern="./bin/savePattern.json", saveTime:int=10, alwaysNew:bool=True, *args, **kwargs) -> save:
    if not alwaysNew and save.currentSave != None:
        return save.currentSave
    else:
        return save(file,pattern, saveTime=saveTime, *args, **kwargs)     
    