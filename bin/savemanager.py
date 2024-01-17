# importy
from tkinter import messagebox
import json
import asyncio
import time
import pygame

import bin.function as fc



class save:
    '''Save gry'''
    def save(self) -> bool:
        '''Ręczne zapisywanie stanu gry\n
            --------------\n
            Argumenty:\n
                * Brak\n
            Zwraca:\n
                * Bool (czy się udało)'''
        # wiem że to troche lenistwo że wyświetlam to za pomocą osiągnieć
        # informacja o zapisywaniu gry
        import bin.achievements as ach
        if ach.achievement.screen != None: _zapAch = ach.achievement("Zapisuję grę...")
        
        self.set("lastGame", time.time_ns())
        self.set("checkSum", 0)
         
        # checksum
        _check = 0
        for _value in fc.NestedDictValues(self.__save):
            _check += int.from_bytes(str(_value).encode('utf-8'), 'little')
            
        _check = ((_check % 10000000000000000) + (_check % 2856 * 4) + _check) % 10000000000000000
        
            
        self.set("checkSum", _check)
            
        
        # sam zapis gry
        _info = fc.updateJSON(self.__fileSave, self.__save)
        
        # informacja o końcu zapisu gry (i usunięcie jakby co informacji o zapisywaniu)
        if ach.achievement.screen != None:
            ach.achievement.achievementShown.remove(_zapAch)
            del(_zapAch)
            if ach.achievement.screen != None: ach.achievement("Gra zapisana!")
        
        # zwrócenie stanu czy się udało
        return _info
    
    def set(self, loc: str, value) -> bool:  
        '''Pozwala ustawić daną wartość w save\n
            Przykład użycia dla uzyskania imienia gracza:\n
            get("player.nickname")\n
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
    
    
    def getSafe(self, loc:str, default = {"error":True, "errorMessage": "pathError"}) -> bool | dict:
        '''Nie wyświetla komunikatu błądu\n
            Użyj jeśli nie masz pewności że coś istnieje w save\n
            ---------------------------\n
            Pozwala uzyskać daną wartość w save\n
            Przykład użycia dla uzyskania imienia gracza:\n
            get("player.nickname")\n
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
    
             
    def get(self, loc:str = "", default = {"error":True, "errorMessage": "pathError"}) -> dict:
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
        
        
    async def autoSave(self):
        await asyncio.sleep(1)
        self.save()
        print("save")
        
    def __init__(self, file="./bin/save.json", pattern="./bin/savePattern.json"):
        self.__fileSave, self.__patternSave = file, pattern

        self.__pattern = fc.readJSON(self.__patternSave)
        if self.__pattern == {}:
            raise Exception("Błąd wczytywania wzóru zapisu")
        
        self.__save = fc.readJSON(self.__fileSave)
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
            
            if _previousCheck != _check:
                messagebox.showwarning('Suma kontrolna', "Istneje podejrzenie że save został uszkodzony!")
                _choice = messagebox.askyesnocancel("Suma kontrolna", "Czy spróbować przywrócic sava? (Nie = Utworzenie nowego, anulowanie = wyjście z gry, miej pod uwagą to że przywrócony save może nie być stabilny i powodować crashe)")
                
                match _choice:
                    case None:
                        pygame.quit()
                    case False:
                        self.erase()
                    case True:
                        pass
                        # TODO: funkcja naprawiająca i sprawdzająca poprawność danych może kiedyś
                        
                
            self.save()
                
        
            
            
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


        
        
        
        
        
        
        
        
        
def get(file="./bin/save.json", pattern="./bin/savePattern.json") -> save:
    return save(file,pattern)     
    