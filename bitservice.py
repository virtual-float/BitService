# Importowanie modułow niezbędnych do uruchomienia gry
import pygame, json
import asyncio, os
import random as rand
from tkinter import messagebox, Button, Tk, Label


# Zaimportuj lokalne moduły
from bin.function import readJSON, updateJSON
from bin.pausescreen import pauseScreen
from bin.achievements import achievement
import bin.savemanager as saveManager

# Game Setting
GS: dict

# Interfejs z oknem menu
class Menu:
    # Konstruktor
    def __init__(self, handle: Tk):
        self.handle = handle

        # Status
        # 0 = exit
        # 1 = play
        self.status = 0

        PlayButton = Button(
            text='Graj',
            width=20,
            height=2,
            command=lambda: self.statusType('play')
        ).place(x=15, y=150)

        ExitButton = Button(
            text='Wyjdź',
            width=20,
            height=2,
            command=lambda: self.statusType('exit')
        ).place(x=15, y=200)

        VersionLabel = Label(
            text=GS['ApplicationVersion']
        ).place(x=500, y=250)

        self.handle.mainloop()
    
    def statusType(self, type: str):
        if type == 'exit':
            self.status = 0
        else:
            self.status = 1
        self.handle.destroy()

# Funkcja, która zwraca zeskalone obrazy
def scaleImage(imgSource: str, scaleBy: int) -> pygame.Surface:
    image = pygame.image.load(imgSource)

    return pygame.transform.scale(image, (image.get_width() * scaleBy, image.get_height() * scaleBy))


async def main(gameSettings: dict):
    global GS
    # messagebox.showinfo('Informacja', 'uruchomiono pomyślnie')

    # Przypisanie ustawień do GS
    GS = gameSettings


    beRunned = True
    while beRunned:
        # Tworzenie root dla tkinter menu
        root = Tk(GS['ApplicationName'], GS['ApplicationName'])
        # Utwarzanie tytułu dla roota
        root.title(GS['ApplicationName'])
        # Ustawianie rozmiaru okna roota
        root.geometry('{}x{}'.format(GS['ApplicationSize'][0], GS['ApplicationSize'][1]))
        
        # Wywołaj klasę Menu o handle root
        menu = Menu(root)
        # jeżeli status wyjściowy wynosi 0 (exit) to niech wyjdzie z gry
        if menu.status == 0:
            break

        # Stwórz display gry
        pygame.init()
        pygame.font.init()
        if GS['fullscreen']:
             displayFinal = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            displayFinal = pygame.display.set_mode((GS['renderSize'][0], GS['renderSize'][1]))
        
        display = pygame.surface.Surface((GS['ApplicationSize'][0], GS['ApplicationSize'][1]))
        
        # Ustaw nazwę gry
        pygame.display.set_caption(GS['ApplicationName'])

        # Tło gry
        Background = scaleImage('bin/images/background.png', 4).convert_alpha()

        # Chmury
        Cloud0 = scaleImage('bin/images/cloud.png', 1).convert_alpha()
        Cloud1 = scaleImage('bin/images/cloud.png', 2).convert_alpha()
        CloudRect0 = Cloud0.get_rect()
        CloudRect1 = Cloud1.get_rect()
        CloudRect0.y = GS['ApplicationSize'][1] // 2 - Cloud0.get_height()
        CloudRect1.y = GS['ApplicationSize'][1] // 2 - Cloud1.get_height() + 50

        # Zmienne gry
        GameOn = True
        # Zegar gry
        GameClock = pygame.time.Clock()
        
        # Obiekt pauseScreen służący do stopowania gry
        pauseScreenOb = pauseScreen(display)
        
        # Inicjalizacja menadżera savów
        save = saveManager.get()
        
        # System osiągnieć (Inicjalizacja)
        achievement.configure(display)
        achievement("uruchomienie")


        # testy savów      
          
        # print(save.get('player.nickname'))
        # save.set("player.nickname", "ika")
        # print(save.get('player.nickname'))
        # print(save.get("player"))
        # save.set("d.character.5", {"type":False})
        # print(save.get(""))
        # print("\n\n")
        # print(save.get("characters"))
        # print(save.get("test.test", {"test":"test"}))
        # save.save()
    
        # próby zrobienia autosava ale te asyncio coś nie asyncionuje, mimo że powinno
        # asyncio.get_event_loop().create_task(save.autoSave())
        
        while GameOn:
            # obsługa eventów 
            EVENTS = pygame.event.get()
            for e in EVENTS:
                match e.type:
                    case pygame.QUIT:
                        GameOn = False
                    case pygame.KEYDOWN:
                        match e.key:
                            case pygame.K_ESCAPE | pygame.K_q:
                                pauseScreenOb.toggle()
                                
                                
                                
            # obliczanie elementów gry
            
            if pauseScreenOb.getState(): 
                # obsługa zdarzeń z eventHandlera z menu pauzy
                _temp = pauseScreenOb.eventHandler(GS['devmode'], EVENTS, save)
                # obsługa opcji
                if _temp == 1:
                    # wyjście do menu
                    GameOn = False
                    continue
                elif _temp == 2:
                    # całkowite wyjście z gry
                    GameOn = False
                    beRunned = False
                    continue
            else:
                # obsługa obliczeń w grze
                
                # chmurki
                if CloudRect0.x < -Cloud0.get_width():
                    CloudRect0.x = GS['ApplicationSize'][0] + 100
                    CloudRect0.y = rand.randint(100, GS['ApplicationSize'][1] - 300)

                if CloudRect1.x < -Cloud1.get_width():
                    CloudRect1.x = GS['ApplicationSize'][0] + 100
                    CloudRect1.y = rand.randint(100, GS['ApplicationSize'][1] - 300) 
                    
                CloudRect0.x -= 1
                CloudRect1.x -= 3     
                
                

            # renderowanie gry

            display.fill((98, 125, 206))


            display.blit(Cloud0, (CloudRect0.x, CloudRect0.y))
            display.blit(Cloud1, (CloudRect1.x, CloudRect1.y))

            display.blit(Background, (0, 0))
            
            
            # renderowanie okna pauzy
            pauseScreenOb.draw(display, GS['devmode'])
            
            
            achievement.loop()
            
            
            # upscalowanie
            pygame.transform.scale(
                surface=display, 
                size=pygame.display.get_surface().get_size(), 
                dest_surface=displayFinal)


            pygame.display.update()
            GameClock.tick(15)
        pygame.quit()
    exit()



if __name__ == "__main__":
    
    # Odczytaj dane
    data = readJSON('./bin/settings.json')
    
    if data != {}:
        asyncio.run(main(data))
    else:
        messagebox.showerror('Błąd', 'Wykryto puste dane ustawień. Nie można uruchomić gry!')
        exit()