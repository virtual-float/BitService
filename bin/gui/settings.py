import tkinter as tk
from tkinter import ttk

from bin.function import updateJSON, readJSON

class settings:
    # def __del__(self) -> None:
    #     self.kill()
        
        
    def kill(self) -> None:
        self.__me.grab_release()
        self.__me.destroy()
        
        
    def __setToGraphics(self) -> None:
        pass
        
        
    def __changeTab(self, newTab:str) -> None:
        match self.__status:
            case 'graphics':
                self.__graphics.pack_forget()
                
            case 'sounds':
                self.__sounds.pack_forget()
                
            case 'other':
                self.__other.pack_forget()
        
        self.__status = newTab
        
        match newTab:
            case 'graphics':
                self.__graphics.pack(anchor="nw")
            case 'sounds':
                self.__sounds.pack(anchor="nw")
                self.__scale.after(20, lambda *args, **kwargs: self.__useUpd(self.__scaleInfo, self.__scale, self.__val)())
            case 'other':
                self.__other.pack(anchor="nw")
        
    def __checkSave(self) -> None:
        print(self.__newSettings, self.__previousSettings)
        print(self.__newSettings != self.__previousSettings)
        if self.__newSettings != self.__previousSettings:
            self.__hasSettingsChanged = True
            self.__menu.entryconfig('Zapisz', state=tk.ACTIVE)
        else:
            self.__menu.entryconfig('Zapisz', state=tk.DISABLED)
            self.__hasSettingsChanged = False
            
    def __handleSave(self) -> None:
        if not self.__hasSettingsChanged: return
        
        self.__previousSettings = self.__newSettings.copy()
        self.__checkSave()
        
        updateJSON('./bin/settings.json', self.__newSettings)
        
        
    def __init__(self, master: tk.Tk):
        # ustawienia mastera
        self.__master = master
    
        # podstawy
        self.__status = 'graphics'
        self.__hasSettingsChanged = False
        self.__previousSettings = readJSON('./bin/settings.json')
        self.__newSettings =  self.__previousSettings.copy()
    
        # podstawy
        self.__me = tk.Toplevel(self.__master)
        self.__me.geometry('450x200')
        self.__me.resizable(False, False)
        self.__me.title("Ustawienia")
        self.__me.attributes("-toolwindow", True)
        
        # menu
        self.__menu = tk.Menu()
        self.__menu.add_command(label = "Grafika", command=lambda: self.__changeTab('graphics'))
        self.__menu.add_command(label = "Dźwięk", command=lambda: self.__changeTab('sounds'))
        self.__menu.add_command(label = "Konto", command=lambda: self.__changeTab('graphics'))
        self.__menu.add_command(label = "Inne", command=lambda: self.__changeTab('other'))
        self.__menu.add_separator()
        self.__menu.add_separator()
        self.__menu.add_separator()
        self.__menu.add_separator()
        self.__menu.add_command(label = "Zapisz", command=self.__handleSave, state="disabled")
        self.__menu.add_command(label = "Fabryczne", command=self.kill)    
        
        # ------------
        # grafika
        # ------------
        
        # podstawy
        self.__graphics = ttk.Frame(master=self.__me, padding="10")
        self.__graphics.pack(anchor="nw")
        
        # rozdzielczość natywna
        ttk.Label(
            master=self.__graphics,
            text = "Rozdzielczość natywna:",
            justify="left"
        ).grid(row=0, column=0)
        
        self.__appSizeVar = tk.StringVar(self.__me, f"{self.__newSettings['ApplicationSize'][0]}x{self.__newSettings['ApplicationSize'][1]}")
        
        ttk.Combobox(master=self.__graphics, 
                     values=["100x100","200x200", "300x300"],
                    #  state="readonly",
                    state = tk.DISABLED,
                     justify="center",
                    textvariable=self.__appSizeVar
                     ).grid(row=0, column=1, padx="10")
  

        ttk.Label(
            master=self.__graphics,
            text = "Rozdzielczość upscalowana:",
            justify="left"
        ).grid(row=1, column=0, pady=15)
        
        
        
        # rozdzielczość upscalowana
        self.__appRenderVar = tk.StringVar(self.__me, f"{self.__newSettings['renderSize'][0]}x{self.__newSettings['renderSize'][1]}")
        
        ttk.Combobox(master=self.__graphics, 
                     values=["100x100","200x200", "300x300"],
                    #  state="readonly",
                    state = tk.DISABLED,
                     justify="center",
                    textvariable=self.__appRenderVar
                     ).grid(row=1, column=1, padx="10",pady=15)
      


        # pełny ekran
        
        def handleFullscreen(*args):
            self.__newSettings['fullscreen'] = self.__fullscreen.get()
            self.__checkSave()
            
        
        self.__fullscreen = tk.BooleanVar(self.__me, self.__previousSettings['fullscreen'])
        self.__fullscreen.trace_add('write', handleFullscreen)
        
        ttk.Checkbutton(
            master=self.__graphics,
            text="Pełny ekran",
            variable=self.__fullscreen
        ).grid(row=2, column=0, pady=10, sticky="w")
        
        
        # customowy kursor
        def handleCustomCursor(*args):
            self.__newSettings['customCursor'] = self.__customCursor.get()
            self.__checkSave()
            
        
        self.__customCursor = tk.BooleanVar(self.__me, self.__previousSettings['fullscreen'])
        self.__customCursor.trace_add('write', handleCustomCursor)
        
        ttk.Checkbutton(
            master=self.__graphics,
            text="niestandardowy kursor",
            variable=self.__customCursor
        ).grid(row=2, column=1, pady=10, sticky="w")
        
        
        # sounds
        self.__sounds = ttk.Frame(master=self.__me, padding="10", width=400, height=400)
        # self.__soundsInfo = ttk.Frame(master=self.__me, padding="10",
        #                               width=400, height=200)
        
        ttk.Label(
            master=self.__sounds,
            text = "Dźwięk ogólny:",
            justify="left"
        ).place(y=0, x=0)
        
        def useUpd(label, scale, val):
            def scale_upd(*args):
                x, _ = scale.coords()
                y, h = scale.winfo_y(), scale.winfo_height()
                label.place(x=x+scale.winfo_x()-20, y=h+y-20)
                label.configure(text=str(round(val.get(),2)) + "%")
                
            return scale_upd
        
        self.__useUpd = useUpd

        self.__val = tk.IntVar(self.__me)
        self.__scaleInfo = ttk.Label(master=self.__sounds)
        self.__scale = ttk.Scale(master=self.__sounds,
                  from_=0,
                  to=100,
                  variable=self.__val,
                  length=200,
                  )
        self.__scaleInfo.lift()
        self.__scale.place(y=0, x=120)
        
        self.__scale.bind('<Configure>', lambda ev: self.__scale.after(10, useUpd(self.__scaleInfo, self.__scale, self.__val)))
        
        self.__val.trace_add('write', useUpd(self.__scaleInfo, self.__scale, self.__val))
        
        self.__val.set(100)
        
        
        # -------------------
        # inne
        # -------------------
        
        # podstawy
        self.__other = ttk.Frame(master=self.__me, padding="10")
        
        # czas autosavu
        def autoSaveHandler(*args):
            self.__newSettings['autoSavetime'] = {
                    "co 10 sekund": 0.16,
                    "co minutę": 1,
                    "co 5 minut": 5,
                    "co 10 minut": 10,
                    "co 15 minut": 15,
                    "co 30 minut": 30,
                    "co 60 minut": 60,
                    "nigdy": 99999999
                }[self.__autoSaveTime.get()]
            self.__checkSave()        
        
        ttk.Label(
            master=self.__other,
            text = "Czas autosavu:",
            justify="left"
        ).grid(row=0, column=0)
        
        self.__autoSaveTime = tk.StringVar(self.__me, {
                "0.16": "co 10 sekund",
                '1': "co minutę",
                "5": "co 5 minut",
                "10": "co 10 minut",
                "15": "co 15 minut",
                "30": "co 30 minut",
                "60": "co 60 minut",
                "99999999": "nigdy"
            }[str(self.__previousSettings['autoSavetime'])])
        
        
        self._cmm = ttk.Combobox(master=self.__other, 
                     values=["co 10 sekund", "co minutę", "co 5 minut", "co 10 minut", "co 15 minut", "co 30 minut", "co 60 minut", "nigdy"],
                     justify="center",
                     state="readonly",
                    textvariable=self.__autoSaveTime
                     ).grid(row=0, column=1, padx="10")
        
        self.__autoSaveTime.trace_add('write', autoSaveHandler)
        
        # finalne
        self.__me.config(menu=self.__menu)
        self.__me.grab_set()

        
        # focus
        self.__me.focus()
        

