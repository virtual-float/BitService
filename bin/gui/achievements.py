# podstawowe importy
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import datetime

# wewnętrzne
import bin.achievements as ach
import bin.savemanager as sm
from bin.function import updateJSON, readJSON

class achievementsGui:
    def __init__(self, master: tk.Tk) -> None:
        self.__master = master
        
        # podstawy
        self.__me = tk.Toplevel(master=self.__master)
        self.__me.geometry('350x400')
        self.__me.resizable(False, False)
        self.__me.title("Osiągniecia")
        self.__me.attributes("-toolwindow", True)
        self.__me.focus()
        self.__me.grab_set()
        
        self.__achievementsData = readJSON("./bin/achievements.json", True)
        
        _s = sm.save(saveToCurrent=False)
        if _s.getSafe("ERROR", default=False) != False:
            self.__me.destroy()
        else:
            _s.save()
            ach.achievement.achievementShown.clear()
            _l = 0
            for achName, achData in self.__achievementsData.items():
                _saveData = _s.getSafe(f"achievements.{achName}", default={
                    "gain": False
                })
                
                if _saveData['gain']:
                    _ze = round(_saveData['gainDate']/1000 / 1000000)
                    _tObj = datetime.datetime.fromtimestamp(_ze)
                    gainDate = f"{_tObj}" 
                    
                    match _saveData['gainVersion']:
                        case 100:
                            gainVersion = "1.0.0v"
                        case _:
                            gainVersion = _saveData['gainVersion']
                else:
                    gainDate = "??"
                    gainVersion = "??"          
                
                _c = tk.Frame(
                    master=self.__me,
                    height=100,
                )

                
                # zdjęcie osiągniecia
                AchievementImage = ImageTk.PhotoImage(Image.open(achData['image']).resize((80,80)))
                
                imageLabel = tk.Label(
                    master = _c,
                    image = AchievementImage,
                    state=tk.ACTIVE if _saveData['gain'] else tk.DISABLED
                )
                imageLabel.image = AchievementImage
                
                imageLabel.pack(side='left')

                # nazwa
                
                tk.Label(
                    master=_c,
                    text=achData['shownNameLong'],
                    font='Helvetica 16 bold',
                    state=tk.ACTIVE if _saveData['gain'] else tk.DISABLED
                ).pack(side='top')
                
                # opis
                
                tk.Label(
                    master=_c,
                    text=achData['description'],
                    font='Consolas 13',
                    state=tk.ACTIVE if _saveData['gain'] else tk.DISABLED
                ).pack(side='top')

                # dodatkowe
                
                
                tk.Label(
                    master=_c,
                    text=f"Data: {gainDate}, wersja: {gainVersion}",
                    state=tk.ACTIVE if _saveData['gain'] else tk.DISABLED
                ).pack(side='bottom')

                # reszta

                _c.grid(column=0, row=_l)
                
                _l += 1
            
            # generowanie znaczników osiagnięć