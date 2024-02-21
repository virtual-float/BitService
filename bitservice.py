# Importowanie modułow niezbędnych do uruchomienia gry
import pygame, asyncio
import random as rand
from tkinter import Button, Label, messagebox, Tk, Canvas
from PIL import Image, ImageTk
import numpy, os


# Zaimportuj lokalne moduły
from bin.function import readJSON, updateJSON, scaleImage
from bin.pausescreen import pauseScreen
from bin.achievements import achievement
import bin.window as window
import bin.savemanager as saveManager
import bin.util as game
from bin.devmode import devModeSprites, giveClock

# gui
from bin.gui.settings import settings as settingsGui
from bin.gui.gate_gui import generate_gate

# Game Setting
GS: dict

# GameOn
GameOn : bool = False

# gameClock (np do przesyłania fpsów)
GameClock: pygame.time.Clock | None = None

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

        self.BackgroundCanvas = Canvas(
            width=GS['ApplicationSize'][0],
            height=GS['ApplicationSize'][1]
        )
        self.BackgroundCanvas.place(x=0,y=0)

        image = Image.open(os.getcwd() + '\\bin\\images\\menu.jpg')
        tkinter_img = ImageTk.PhotoImage(image=image)

        self.BackgroundCanvas.create_image(-2, -2, anchor='nw', image=tkinter_img)

        c_text = self.BackgroundCanvas.create_text(
            192, 64, 
            text=GS['ApplicationName'], 
            font=('Consolas', 38, 'bold'),
            fill='#f0f0f0')
        
        c_version = self.BackgroundCanvas.create_text(
            GS['ApplicationSize'][0] - 32, 
            GS['ApplicationSize'][1] - 16,
            text=GS['ApplicationVersion'],
            font=('Consolas', 12),
            fill='#f0f0f0')

        PlayButton = Button(
            text='Graj',
            width=20,
            height=2,
            command=lambda: self.statusType('play')
        ).place(x=15, y=150)

        settings = Button(
            text='Ustawienia',
            width=20,
            height=2,
            command=lambda: settingsGui(self.handle)
        ).place(x=15, y=200)

        ExitButton = Button(
            text='Wyjdź',
            width=20,
            height=2,
            command=lambda: self.statusType('exit')
        ).place(x=15, y=250)

        self.handle.mainloop()
    
    def statusType(self, type: str) -> None:
        global GS
        if type == 'play':
            GS = readJSON('./bin/settings.json')
            self.status = 1
        self.handle.destroy()

# Funkcja, która zwróci ilość barów dla progress baru
def generateBars(repStatus: int):
    if repStatus > 0:
        for i in range(0, repStatus, 1):
            if i == repStatus - 1 and repStatus != 10: # 10 - max
                yield pygame.image.load('bin/images/bar_head.png'), pygame.image.load('bin/images/bar_head.png').get_rect()
                break
            yield pygame.image.load('bin/images/bar_body.png'), pygame.image.load('bin/images/bar_body.png').get_rect()
    else:
        return ''


# Klasa gracza
class Player:

    # Opcje emotek
    EmoteSad : int = -1
    EmoteAnger : int = 0
    EmoteHappy : int = 1
    EmoteCry : int = 2


    def __init__(self, initPlayerFile: str, x: int, y: int) -> None:
        self.__playerdata : dict = readJSON(initPlayerFile)
        
        # TODO: Zsynchronizować ilość ratio dla gracza w przypadku gdy istnieje save
        # self.ratio_level = dataManager.get('player.ratiolevel')

        if self.__playerdata == {}:
            messagebox.showerror(__name__, 'Dane animacji gracza są puste!')
            exit()

        self.emote_idle : pygame.image = scaleImage(self.__playerdata['STATE_IDLE'], RENDER_SCALE)

        self.rect : pygame.rect.Rect = self.emote_idle.get_rect()
        self.rect.x, self.rect.y = x, y

        self.animation_move : list = list(map(
            lambda a_path: scaleImage(a_path, RENDER_SCALE),
            self.__playerdata['STATE_MOVE']
        ))

        self.emote_sad : pygame.image = scaleImage(self.__playerdata['EMOTE_SAD'], RENDER_SCALE)

        self.emote_cry : pygame.image = scaleImage(self.__playerdata['EMOTE_CRY'], RENDER_SCALE)

        self.emote_happy : pygame.image = scaleImage(self.__playerdata['EMOTE_HAPPY'], RENDER_SCALE)

        self.current_img = self.emote_idle

        self.gameover : bool = False

    # Metoda, która będzie sprawdzała 'logiki' dla gracza
    def update(self) -> None:
        # Logika dla ratio level
        _s = saveManager.get(alwaysNew=False)
        
        if _s.getSafe('player.ratiolevel', default=0) >= 10:
            _s.set('player.ratiolevel', 10)
        elif _s.getSafe('player.ratiolevel', default=0) <= 0:
            _s.set('player.ratiolevel', 0)
            self.gameover = True

        # Logika emotek
        _ratio = _s.getSafe('player.ratiolevel', default=0)
        
        if _ratio <= 0:
            self.current_img = self.emote_cry
        elif _ratio > 0 and _ratio <= 4:
            self.current_img = self.emote_sad
        elif _ratio > 4 and _ratio <= 7:
            self.current_img = self.emote_idle
        elif _ratio > 7 and _ratio <= 10:
            self.current_img = self.emote_happy

        # Logika w przypadku game over
        if self.gameover:
            global GameOn, RENDER_SCALE, GS

            if not hasattr(self, 'new_dest_x') and not hasattr(self, 'new_dest_y'):
                self.new_dest_x, self.new_dest_y = self.rect.x - GS['ApplicationSize'][0] + self.current_img.get_width(), self.rect.y - 48
            
            if self.rect.y > self.new_dest_y:
                self.rect.y -= 1 * RENDER_SCALE
            elif self.rect.x > self.new_dest_x:
                self.rect.x -= 1 * (RENDER_SCALE * RENDER_SCALE) // 2
            
            if self.rect.x <= self.new_dest_x and self.rect.y <= self.new_dest_y:
                delattr(self, 'new_dest_x')
                delattr(self, 'new_dest_y')
                GameOn = False
            
        


async def main(gameSettings: dict):
    global GS, GameOn, GameClock
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
            if task.get_name() != "Task-1": task.cancel()
    
        # usuwanie devmoda
        
        # Tworzenie root dla tkinter menu
        root = Tk()
        root.title(GS['ApplicationName'])
        root.wm_resizable(False, False)
        root.iconbitmap('./' + str(GS['ApplicationIcon']).replace('.png', '.ico'))
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
        pb_x = (GS['ApplicationSize'][0] + ProgressBar.get_width()) // 2
        pb_y = GS['ApplicationSize'][1] // 2 + (8 * ProgressBar.get_height())
        ProgressBarRect.x = pb_x
        ProgressBarRect.y = pb_y

        # Objekt
        # Biurko z rzeczami od razu
        Stuff = scaleImage("bin/images/stuff_prefab.png", RENDER_SCALE).convert_alpha()
        StuffRect = Stuff.get_rect()
        StuffRect.x = GS['ApplicationSize'][0] // 2 + (Stuff.get_width() - 50)
        StuffRect.y = GS['ApplicationSize'][1] // 2 + (Stuff.get_height() // 12) - 32

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
        giveClock(GameClock)


        # Gameover
        GameoverScreenSurface = pygame.surface.Surface((GS['ApplicationSize'][0], GS['ApplicationSize'][1]), pygame.SRCALPHA, 32)
        GameoverScreenSurface.fill((0, 0, 0, 95))
        GameOverImage = scaleImage('bin/images/game_over.png', 4).convert_alpha()

        # Informacje o grze [game over]
        FontRender = pygame.font.Font(None, 28)
        InformationLabel = FontRender.render('Zostałeś wyrzucony z Bits & Services :( !!!', False, (255, 255, 255))

        # ...
        GameoverScreenSurface.blit(GameOverImage, (GS['ApplicationSize'][0] // 2 - GameOverImage.get_width() // 2, GS['ApplicationSize'][1] // 2 - GameOverImage.get_height()))
        GameoverScreenSurface.blit(InformationLabel, (GS['ApplicationSize'][0] // 2 - GameOverImage.get_width() // 2 + 32, GS['ApplicationSize'][1] // 2 + (GameOverImage.get_height() // 2)))

        
        
        # Obiekt pauseScreen służący do stopowania gry
        pauseScreenOb = pauseScreen(display)
        
        # Inicjalizacja menadżera savów
        save = saveManager.get(saveTime=GS['autoSavetime'] * 60)
        
        # usuwanie devmoda
        save.set("devmode", False)

        # Gracz
        kera = Player("./bin/images/player/init.json", 0, 0)
        kera.rect.x = GS['ApplicationSize'][0] - round(kera.emote_idle.get_width() * 1.5) - 112
        kera.rect.y = GS['ApplicationSize'][1] - kera.emote_idle.get_height() - 64
        
        # System osiągnieć (Inicjalizacja)
        achievement.configure(display)
        achievement("uruchomienie")


        # testy okien, możesz wyrzucić, moja "zabawa", jedynie renderują aktualnie, niewiem, bawię się ucząć
        # możesz zobaczyć, ale nie jest okomentowane mocno
        
        game.window.startTask()
        game.window.eraseWindows()

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
        
        # game.client.clientGroup.empty()
        game.client.startTask()
        
        game.client.restore()
        
        # funkcja ułatwiająca
        async def waitForOther():
            await asyncio.sleep(0.00002)

        while GameOn:
            await waitForOther()
            # obsługa eventów 
            
            # wyłączanie gdy już wcześniej ktoś włączył ekran pauzy i nagle jakimś cudem ma mniej (przeciwko bugom)
            if pauseScreenOb.getState() and kera.gameover:
                pauseScreenOb.toggle(forceState=False)
            
            EVENTS = pygame.event.get()
            game.window.sendEvents(EVENTS)
            for e in EVENTS:
                match e.type:
                    case pygame.QUIT:
                        GameOn = False
                    case pygame.KEYDOWN:
                        match e.key:
                            case pygame.K_ESCAPE:
                                if not kera.gameover:
                                    pauseScreenOb.toggle(checkFocus=False)
                            case pygame.K_q:
                                if not kera.gameover:
                                    pauseScreenOb.toggle()
                            # WYŁĄCZNIE DLA TESTU TO CO PONIŻEJ
                            case pygame.K_LEFT:
                                save.set('player.ratiolevel', save.getSafe('player.ratiolevel', default=0)-1)
                            case pygame.K_RIGHT:
                                save.set('player.ratiolevel', save.getSafe('player.ratiolevel', default=0)+1)
                            case pygame.K_UP:
                                if not game.window.checkWindow("gate_gui"):
                                    pass

    
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
            display.blit(Stuff, (StuffRect.x, StuffRect.y))

            # Renderowanie klientów 
            game.client.clientGroup.draw(display)
            
            # renderowanie efektów dla klientów
            game.client.clientEffectGroup.draw(display)

            if kera.gameover:
                display.blit(GameoverScreenSurface, (0, 0))
            else:
                # Progress bar
                display.blit(ProgressBar, (ProgressBarRect.x, ProgressBarRect.y))

                # Layout
                bars_t = generateBars(save.getSafe('player.ratiolevel', default=0))
                
                if not isinstance(bars_t, str):
                    # temp
                    temp_x = 0

                    # Render barów dla progress bar
                    for bar in list(bars_t):
                        bar[1].x, bar[1].y = (pb_x + 2) + temp_x, (pb_y + 2)

                        temp_x += bar[0].get_width()

                        display.blit(bar[0], (bar[1].x, bar[1].y))
                    

            
        
                
            # renderowanie okna
            window.window.draw(display)
            
            # renderowanie okna pauzy
            pauseScreenOb.draw(display, GS['devmode'])
            
            
            # renderowanie devmoda
            devModeSprites.draw(display)
            
            # renderowanie osiągnieć
            achievement.loopDraw()
            
            # upscalowanie
            pygame.transform.scale(
                surface=display, 
                size=pygame.display.get_surface().get_size(), 
                dest_surface=displayFinal)

            pygame.display.update()

            # Update metoda dla gracza
            kera.update()

            GameClock.tick(15)
            
        pygame.quit()



# testuje otwieranie bez okna windowsowego, wiem że to nie jest najlepsza metoda, ale niewiem
# jak zrobić inaczej to XD
# potem można to odwrócić łatwo jak coś
if __name__ == "__main__":
    
    # Odczytaj dane
    
    data = readJSON('./bin/settings.json', showErrors=False)

    if data == {}:
        data = readJSON("./bin/settingsPattern.json")
        updateJSON('./bin/settings.json', data)
    asyncio.run(main(data))
