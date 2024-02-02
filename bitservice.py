# Importowanie modułow niezbędnych do uruchomienia gry
import pygame, asyncio
import random as rand
from tkinter import Button, Label, messagebox, Tk


# Zaimportuj lokalne moduły
from bin.function import readJSON, updateJSON
from bin.pausescreen import pauseScreen
from bin.achievements import achievement
import bin.window as window
import bin.savemanager as saveManager
import bin.util as game

# gui
from bin.gui.settings import settings as settingsGui

# Game Setting
GS: dict

# Constant
RENDER_SCALE : int = 4

# Interfejs z oknem menu
class Menu:
    # Konstruktor
    def __init__(self, rootHandle: Tk) -> None:
        global GS
        
        self.handle = rootHandle

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
        
        settings = Button(
            text='Ustawienia',
            width=20,
            height=2,
            command=lambda: settingsGui(self.handle)
        ).place(x=15, y=250)

        VersionLabel = Label(
            text=GS['ApplicationVersion']
        ).place(x=GS['ApplicationSize'][0] - 125, y=GS['ApplicationSize'][1] - 50)

        # TODO: Zrobić menu z tłem bin/images/menu.jpg

        self.handle.mainloop()
    
    def statusType(self, type: str) -> None:
        global GS
        if type == 'play':
            GS = readJSON('./bin/settings.json')
            self.status = 1
        self.handle.destroy()

# Funkcja, która zwraca zeskalone obrazy
def scaleImage(imgSource: str, scaleBy: int) -> pygame.Surface:
    image = pygame.image.load(imgSource)

    return pygame.transform.scale(image, (image.get_width() * scaleBy, image.get_height() * scaleBy))


# Funkcja, która zwróci ilość barów dla progress baru
def generateBars(repStatus: int):
    if repStatus <= 0: yield []
    elif repStatus > 10: repStatus = 10

    for i in range(0, repStatus, 1):
        if i == repStatus - 1 and repStatus != 10: # 10 - max
            yield pygame.image.load('bin/images/bar_head.png'), pygame.image.load('bin/images/bar_head.png').get_rect()
            break
        yield pygame.image.load('bin/images/bar_body.png'), pygame.image.load('bin/images/bar_body.png').get_rect()


# Klasa gracza
class Player:

    # Opcje animacji
    AnimationDefault : int = -1
    AnimationTypewrite : int = 0
    AnimationMove : int = 1

    def __init__(self, initPlayerFile: str, x: int, y: int, dataManager: saveManager) -> None:
        self.__playerdata : dict = readJSON(initPlayerFile)
        
        # TODO: Zsynchronizować ilość ratio dla gracza w przypadku gdy istnieje save
        self.ratio_level = 10

        if self.__playerdata == {}:
            messagebox.showerror(__name__, 'Dane animacji gracza są puste!')
            exit()

        self.animation_idle : pygame.image = [
            scaleImage(self.__playerdata['STATE_IDLE'], RENDER_SCALE),
            pygame.transform.flip(scaleImage(self.__playerdata['STATE_IDLE'], RENDER_SCALE), True, False)
        ]

        self.rect : pygame.rect.Rect = self.animation_idle[0].get_rect()
        self.rect.x, self.rect.y = x, y

        self.animation_move : list = list(map(
            lambda a_path: (scaleImage(a_path, RENDER_SCALE), pygame.transform.flip(scaleImage(a_path, RENDER_SCALE), True, False)),
            self.__playerdata['STATE_MOVE']
        ))

        self.animation_typewrite : list = list(map(
            lambda a_path: (scaleImage(a_path, RENDER_SCALE), pygame.transform.flip(scaleImage(a_path, RENDER_SCALE), True, False)),
            self.__playerdata['STATE_TYPEWRITE']
        ))

        self.current_img = self.animation_idle[0]

    # Metoda, która zwraca aktualny tryb animacji oraz obrazy png dla tej animacji
    @classmethod
    def get_from_state(self) -> tuple:
        Data = None

        match self.state:
            case self.AnimationDefault:
                Data = self.animation_idle
            case self.AnimationTypewrite:
                Data = self.animation_typewrite
            case self.AnimationMove:
                Data = self.animation_move 
        
        return self.state, Data




async def main(gameSettings: dict):
    global GS
    # messagebox.showinfo('Informacja', 'uruchomiono pomyślnie')

    # Przypisanie ustawień do GS
    GS = gameSettings

    # by nie było błędu
    class __Tsave:
        def kill(self): pass
    save = __Tsave()

    beRunned = True
    while beRunned:
        # usuwanie starych tasków z gry
        # save.kill()
        # achievement.kill()
        
        for task in asyncio.all_tasks():
            if task.get_name() in ['windowManager', 'saveManager', 'saveManagerSec', 'achievementManager', 'gameClock', 'eventManager']: task.cancel()
    
        
        
        # Tworzenie root dla tkinter menu
        root = Tk()
        root.title(GS['ApplicationName'])
        root.iconbitmap('./' + GS['ApplicationIcon'])
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
        pygame.display.set_icon(pygame.image.load(GS['ApplicationIcon']))

        # Tło gry
        Background = scaleImage('bin/images/background.png', RENDER_SCALE).convert_alpha()

        # Dla gry
        ProgressBar = pygame.image.load('bin/images/progress_bar.png').convert_alpha()
        ProgressBarRect = ProgressBar.get_rect()
        pb_x = GS['ApplicationSize'][0] // 2 + (ProgressBar.get_width() // 2)
        pb_y = GS['ApplicationSize'][1] // 2 + (8 * ProgressBar.get_height())
        ProgressBarRect.x = pb_x
        ProgressBarRect.y = pb_y

        # Objekty
        # Biurko
        Table = scaleImage("bin/images/table.png", RENDER_SCALE).convert_alpha()
        TableRect = Table.get_rect()
        TableRect.x = GS['ApplicationSize'][0] // 2 + (Table.get_width() - 50)
        TableRect.y = GS['ApplicationSize'][1] // 2 + (Table.get_height() // 3) + 10

        # Monitor
        Screen = scaleImage("bin/images/monitor.png", RENDER_SCALE).convert_alpha()
        ScreenRect = Screen.get_rect()
        ScreenRect.x = GS['ApplicationSize'][0] // 2 + (Screen.get_width() + 50)
        ScreenRect.y = GS['ApplicationSize'][1] // 2 + (Screen.get_height() // 3) - 50

        # Klawiatura
        Keyboard = scaleImage("bin/images/keyboard.png", RENDER_SCALE).convert_alpha()
        KeyboardRect = Keyboard.get_rect()

        # Kubek
        Cup = scaleImage("bin/images/cup.png", RENDER_SCALE).convert_alpha()
        CupRect = Cup.get_rect()

        # Komputer
        # ...

        # Chmury
        Cloud0 = scaleImage('bin/images/cloud.png', RENDER_SCALE // RENDER_SCALE).convert_alpha()
        Cloud1 = scaleImage('bin/images/cloud.png', RENDER_SCALE // 2).convert_alpha()
        CloudRect0 = Cloud0.get_rect()
        CloudRect1 = Cloud1.get_rect()
        CloudRect0.y = GS['ApplicationSize'][1] // 2 - Cloud0.get_height()
        CloudRect1.y = GS['ApplicationSize'][1] // 2 - Cloud1.get_height() + 48

        # Zmienne gry
        GameOn = True
        # Zegar gry
        GameClock = pygame.time.Clock()
        
        
        # Obiekt pauseScreen służący do stopowania gry
        pauseScreenOb = pauseScreen(display)
        
        # Inicjalizacja menadżera savów
        save = saveManager.get()

        # Gracz
        kera = Player("./bin/images/player/init.json", 0, 0, save)
        kera.rect.x = GS['ApplicationSize'][0] - int(kera.animation_idle[0].get_width() * 1.5) - 128 + 16
        kera.rect.y = GS['ApplicationSize'][1] - kera.animation_idle[0].get_height() - 64
        
        # System osiągnieć (Inicjalizacja)
        achievement.configure(display)
        achievement("uruchomienie")


        # testy okien, możesz wyrzucić, moja "zabawa", jedynie renderują aktualnie, niewiem, bawię się ucząć
        # możesz zobaczyć, ale nie jest okomentowane mocno
        
        game.window.startTask()
        game.window.eraseWindows()

        game.question('test')
        # chmura = game.windowElement(Cloud0)
        # chmura.addClickListener(lambda pressed, pos: print('test'))
        # game.window('test', (400,100), pygame.sprite.Group(
        #     # chmura,
        #     # game.windowText('SMALL_COMICSANS', 'Test', (5,5))
        #     box := game.windowTextBox((20,20), "", xsize=7, maxlength=3, marginleft=7).setReturnListener(lambda text: print(text))
        # ), closable=True).addObjectToListen(box)
        
        # game.window.getWindow('test').setPosition((400,200))
        # game.window('test2', (200,200), pygame.sprite.Group(), closable=True)
        # game.window.getWindow('test2').setPosition((0,300))
        
        # funkcja ułatwiająca
        async def waitForOther():
            await asyncio.sleep(0.02)  
               
        while GameOn:
            await waitForOther()
            # obsługa eventów 
            EVENTS = pygame.event.get()
            game.window.sendEvents(EVENTS)
            for e in EVENTS:
                match e.type:
                    case pygame.QUIT:
                        GameOn = False
                    case pygame.KEYDOWN:
                        match e.key:
                            case pygame.K_ESCAPE:
                                pauseScreenOb.toggle(checkFocus=False)
                            case pygame.K_q:
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

            # Chmury
            display.blit(Cloud0, (CloudRect0.x, CloudRect0.y))
            display.blit(Cloud1, (CloudRect1.x, CloudRect1.y))

            # Budynek
            display.blit(Background, (0, 0))

            # Renderowanie gracza
            display.blit(kera.current_img, (kera.rect.x, kera.rect.y))

            # Renderowanie objektów
            display.blit(Table, (TableRect.x, TableRect.y))
            display.blit(Screen, (ScreenRect.x, ScreenRect.y))

            # Renderowanie klientów 
            # ...

            # Progress bar
            display.blit(ProgressBar, (ProgressBarRect.x, ProgressBarRect.y))

            # Layout
            bars_t = list(generateBars(kera.ratio_level))
            
            if bars_t != []:
                # TODO: Wyświetl gameover screen
                pass

            # temp
            temp_x = 0

            # Render barów dla progress bar
            for bar in bars_t:
                bar[1].x, bar[1].y = (pb_x + 2) + temp_x, (pb_y + 2)

                temp_x += bar[0].get_width()

                display.blit(bar[0], (bar[1].x, bar[1].y))
                
                
                
            # renderowanie okna
            window.window.draw(display)
            
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

    if data == {}:
        messagebox.showerror('Błąd', 'Wykryto puste dane ustawień. Nie można uruchomić gry!')
        exit()
    asyncio.run(main(data))    
