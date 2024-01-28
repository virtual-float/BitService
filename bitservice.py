# Importowanie modułow niezbędnych do uruchomienia gry
import pygame, asyncio
import random as rand
import tkinter


# Zaimportuj lokalne moduły
from bin.function import readJSON, updateJSON
from bin.pausescreen import pauseScreen
from bin.achievements import achievement
import bin.savemanager as saveManager

# Game Setting
GS: dict

# Constant
RENDER_SCALE : int = 4

# Interfejs z oknem menu
class Menu:
    # Konstruktor
    def __init__(self, rootHandle: tkinter.Tk) -> None:
        self.handle = rootHandle

        # Status
        # 0 = exit
        # 1 = play
        self.status = 0

        PlayButton = tkinter.Button(
            text='Graj',
            width=20,
            height=2,
            command=lambda: self.statusType('play')
        ).place(x=15, y=150)

        ExitButton = tkinter.Button(
            text='Wyjdź',
            width=20,
            height=2,
            command=lambda: self.statusType('exit')
        ).place(x=15, y=200)

        VersionLabel = tkinter.Label(
            text=GS['ApplicationVersion']
        ).place(x=GS['ApplicationSize'][0] - 125, y=GS['ApplicationSize'][1] - 50)

        self.handle.mainloop()
    
    def statusType(self, type: str):
        if type == 'play':
            self.status = 1
        self.handle.destroy()

# Funkcja, która zwraca zeskalone obrazy
def scaleImage(imgSource: str, scaleBy: int) -> pygame.Surface:
    image = pygame.image.load(imgSource)

    return pygame.transform.scale(image, (image.get_width() * scaleBy, image.get_height() * scaleBy))


# Funkcja, która zwróci ilość barów dla progress baru
def generateBars(repStatus: int):
    if repStatus <= 0:
        yield []

    for i in range(0, repStatus, 1):
        if i == repStatus - 1:
            yield pygame.image.load('bin/images/bar_head.png'), pygame.image.load('bin/images/bar_head.png').get_rect()
            break
        yield pygame.image.load('bin/images/bar_body.png'), pygame.image.load('bin/images/bar_body.png').get_rect()


# Klasa gracza
class Player:
    def __init__(self):
        pass

    def animate(self, AnimationOption):
        pass



async def main(gameSettings: dict):
    global GS
    # messagebox.showinfo('Informacja', 'uruchomiono pomyślnie')

    # Przypisanie ustawień do GS
    GS = gameSettings

    

    # by nie było błędu
    class __Tsave:
        def kill(self): pass
    save = __Tsave()

    # Dla testu
    to_iterate = 10

    beRunned = True
    while beRunned:
        # usuwanie starych tasków z gry
        # save.kill()
        # achievement.kill()
        
        for task in asyncio.all_tasks():
            if task.get_name() in ['saveManager', 'saveManagerSec', 'achievementManager', 'gameClock', 'eventManager']: task.cancel()
    
        
        
        # Tworzenie root dla tkinter menu
        root = tkinter.Tk()
        root.title(GS['ApplicationName'])
        root.geometry("{}x{}".format(GS['ApplicationSize'][0], GS['ApplicationSize'][1]))
        
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
        Background = scaleImage('bin/images/background.png', RENDER_SCALE).convert_alpha()

        # Dla gry
        ProgressBar = pygame.image.load('bin/images/progress_bar.png').convert_alpha()
        ProgressBarRect = ProgressBar.get_rect()
        pb_x = GS['ApplicationSize'][0] // 2 + (ProgressBar.get_width() // 2)
        pb_y = GS['ApplicationSize'][1] // 2 + (8 * ProgressBar.get_height())
        ProgressBarRect.x = pb_x
        ProgressBarRect.y = pb_y

        # Chmury
        Cloud0 = scaleImage('bin/images/cloud.png', RENDER_SCALE // RENDER_SCALE).convert_alpha()
        Cloud1 = scaleImage('bin/images/cloud.png', RENDER_SCALE // 2).convert_alpha()
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

        # funkcja ułatwiająca
        async def waitForOther():
            await asyncio.sleep(0.02)  
               
        while GameOn:
            await waitForOther()
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

            # Progress bar
            display.blit(ProgressBar, (ProgressBarRect.x, ProgressBarRect.y))

            # Layout
            bars_t = list(generateBars(to_iterate))
            
            if bars_t == []:
                # TODO: Wyświetl gameover screen
                pass

            # temp
            temp_x = 0

            for bar in bars_t:
                bar[1].x, bar[1].y = (pb_x + 2) + temp_x, (pb_y + 2)

                temp_x += bar[0].get_width()

                display.blit(bar[0], (bar[1].x, bar[1].y))
            
            # renderowanie okna pauzy
            pauseScreenOb.draw(display, GS['devmode'])
            
            
            achievement.loopDraw()
            
            # upscalowanie
            pygame.transform.scale(
                surface=display, 
                size=pygame.display.get_surface().get_size(), 
                dest_surface=displayFinal)


            pygame.display.update()
            GameClock.tick(15)
            
        pygame.quit()




if __name__ == "__main__":
    
    # Odczytaj dane
    data = readJSON('./bin/settings.json')
    
    if data != {}:
        asyncio.run(main(data))
    else:
        tkinter.messagebox.showerror('Błąd', 'Wykryto puste dane ustawień. Nie można uruchomić gry!')
        exit()