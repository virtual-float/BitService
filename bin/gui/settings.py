import tkinter as tk
from tkinter import ttk


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
        
        self.__status = newTab
        
        match newTab:
            case 'graphics':
                self.__graphics.pack(anchor="nw")
            case 'sounds':
                self.__sounds.pack(anchor="nw")
                self.__scale.after(20, lambda *args, **kwargs: self.__useUpd(self.__scaleInfo, self.__scale, self.__val)())
        
        
        
    def __init__(self, master: tk.Tk):
        # ustawienia mastera
        self.__master = master
    
        # podstawy
        self.__status = 'graphics'
    
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
        self.__menu.add_command(label = "Inne", command=lambda: self.__changeTab('graphics'))
        self.__menu.add_separator()
        self.__menu.add_separator()
        self.__menu.add_separator()
        self.__menu.add_separator()
        self.__menu.add_command(label = "Zapisz", command=self.kill)
        self.__menu.add_command(label = "Fabryczne", command=self.kill)    
        
        # grafika
        self.__graphics = ttk.Frame(master=self.__me, padding="10")
        self.__graphics.pack(anchor="nw")
        
        ttk.Label(
            master=self.__graphics,
            text = "Rozdzielczość natywna:",
            justify="left"
        ).grid(row=0, column=0)
        
        ttk.Combobox(master=self.__graphics, 
                     textvariable="test",
                     values=["100x100","200x200", "300x300"],
                    #  state="readonly",
                    state = tk.DISABLED,
                     justify="center",
                     ).grid(row=0, column=1, padx="10")
  

        ttk.Label(
            master=self.__graphics,
            text = "Rozdzielczość upscalowana:",
            justify="left"
        ).grid(row=1, column=0, pady=15)
        
        ttk.Combobox(master=self.__graphics, 
                     textvariable="test",
                     values=["100x100","200x200", "300x300"],
                    #  state="readonly",
                    state = tk.DISABLED,
                     justify="center",
                     ).grid(row=1, column=1, padx="10",pady=15)
      
        # ttk.Label(
        #     master=self.__graphics,
        #     text = "Pełny ekran:"
        # ).grid(row=2, column=0)
        
        ttk.Checkbutton(
            master=self.__graphics,
            text="Pełny ekran"
        ).grid(row=2, column=0, pady=10, sticky="w")
        
        ttk.Checkbutton(
            master=self.__graphics,
            text="niestandardowy kursor"
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
        
        # finalne
        self.__me.config(menu=self.__menu)
        self.__me.grab_set()

        
        # focus
        self.__me.focus()
        

