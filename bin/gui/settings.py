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
        self.__menu.add_command(label = "Grafika", command=self.__setToGraphics)
        self.__menu.add_command(label = "Dźwięk", command=self.__setToGraphics)
        self.__menu.add_command(label = "Konto", command=self.__setToGraphics)
        self.__menu.add_command(label = "Inne", command=self.__setToGraphics)
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
        
        # finalne
        self.__me.config(menu=self.__menu)
        self.__me.grab_set()

        
        # focus
        self.__me.focus()
        

