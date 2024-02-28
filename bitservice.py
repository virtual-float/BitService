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
from bin.answerIndicator import answerIndicator

# gui
from bin.gui.settings import settings as settingsGui
# from bin.gui.gate_gui import generate_gate
from bin.gui.achievements import achievementsGui

# Game Setting
GS: dict

# GameOn
GameOn : bool = False

# Stałe
MAX_USEFULNESS_COUNT : int = 35

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

        AchievementsButton = Button(
            text='Osiągnięcia',
            width=20,
            height=2,
            command=lambda: achievementsGui(self.handle)
        ).place(x=15, y=200)

        settings = Button(
            text='Ustawienia',
            width=20,
            height=2,
            command=lambda: settingsGui(self.handle)
        ).place(x=15, y=250)

        ExitButton = Button(
            text='Wyjdź',
            width=20,
            height=2,
            command=lambda: self.statusType('exit')
        ).place(x=15, y=300)

        self.handle.mainloop()
    
    def statusType(self, type: str) -> None:
        global GS
        if type == 'play':
            GS = readJSON('./bin/settings.json')
            self.status = 1
        self.handle.destroy()

# Funkcja, która zwróci ilość barów dla wskaźnika użyteczności
def generate_use_bars(current_amount: int):
    if current_amount > 0 and current_amount <= MAX_USEFULNESS_COUNT:
        for i in range(0, current_amount, 1):
            if i == current_amount - 1 and current_amount < MAX_USEFULNESS_COUNT: # 35 - max
                yield pygame.image.load('bin/images/bar_head.png'), pygame.image.load('bin/images/bar_head.png').get_rect()
                break
            yield pygame.image.load('bin/images/bar_body.png'), pygame.image.load('bin/images/bar_body.png').get_rect()
    else:
        return ''

# Klasa gracza
class Player:

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
        
        if _s.getSafe('player.ratiolevel', default=0) >= MAX_USEFULNESS_COUNT:
            _s.set('player.ratiolevel', MAX_USEFULNESS_COUNT)
        elif _s.getSafe('player.ratiolevel', default=0) <= 0:
            _s.set('player.ratiolevel', 0)
            self.gameover = True
        
        # Logika emotek
        _ratio = _s.getSafe('player.ratiolevel', default=0)
        
        if _ratio <= 0:                   self.current_img = self.emote_cry
        elif _ratio > 0 and _ratio <= 10:  self.current_img = self.emote_sad
        elif _ratio > 10 and _ratio <= 20:  self.current_img = self.emote_idle
        elif _ratio > 20 and _ratio <= 35: self.current_img = self.emote_happy

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
        
        # usuwanie poprzednich tasków
        for task in asyncio.all_tasks():
            if task.get_name() != "Task-1": task.cancel()

        # Stwórz display gry
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        if GS['fullscreen']:
            displayFinal = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            displayFinal = pygame.display.set_mode((GS['renderSize'][0], GS['renderSize'][1]))
        
        display = pygame.surface.Surface((GS['ApplicationSize'][0], GS['ApplicationSize'][1]))
        
        # Ustaw nazwę gry
        pygame.display.set_caption(GS['ApplicationName'])
        pygame.display.set_icon(pygame.image.load(GS['ApplicationIcon']))

        FontRender = pygame.font.Font(os.getcwd() + '\\bin\\franklin_gothic.TTF', 22)
        FontRenderSmall = pygame.font.Font(os.getcwd() + '\\bin\\franklin_gothic.TTF', 18)
        FontBitRender = pygame.font.Font(os.getcwd() + '\\bin\\vgafixe.FON', 24)

        # Inicjalizacja menadżera savów
        save = saveManager.get(saveTime=GS['autoSavetime'] * 60)
        # pozyskiwanie błędu ładowania sava
        if save.getSafe("ERROR", default=False) != False:
            GameOn = False

        # Tło za tłem gry
        BackgroundBehind = scaleImage('bin/images/background_behind.png', RENDER_SCALE).convert_alpha()
        # Tło gry
        Background = scaleImage('bin/images/background.png', RENDER_SCALE).convert_alpha()
        # Tło (emiter światła)
        BackgroundFilter = scaleImage('bin/images/background_filter.png', RENDER_SCALE).convert_alpha()

        # Stats
        Board = scaleImage('bin/images/stats_board.png', RENDER_SCALE).convert_alpha()
        rBoard = Board.get_rect()
        rBoard.x = GS['ApplicationSize'][0] - Board.get_width() - 16
        rBoard.y = (GS['ApplicationSize'][1] // 6) * -1


        # Dla gry
        UsefulnessBar = pygame.image.load('bin/images/usefulness_bar.png').convert_alpha()
        UsefulnessBarRect = UsefulnessBar.get_rect()
        ub_x = (GS['ApplicationSize'][0] + UsefulnessBar.get_width()) // 3 + 86
        ub_y = GS['ApplicationSize'][1] // 2 + (18 * UsefulnessBar.get_height())
        UsefulnessBarRect.x = ub_x
        UsefulnessBarRect.y = ub_y


        # Objekt
        # Biurko z rzeczami od razu
        Stuff = scaleImage("bin/images/stuff_prefab.png", RENDER_SCALE).convert_alpha()
        StuffRect = Stuff.get_rect()
        StuffRect.x = GS['ApplicationSize'][0] // 2 + (Stuff.get_width() - 50)
        StuffRect.y = GS['ApplicationSize'][1] // 2 + (Stuff.get_height() // 12) - 32

        # Chmury (gfx)
        Clouds : list[pygame.Surface] = [
            scaleImage('bin/images/cloud.png', RENDER_SCALE // RENDER_SCALE).convert_alpha(),
            scaleImage('bin/images/cloud.png', RENDER_SCALE // 2).convert_alpha(),
            scaleImage('bin/images/cloud.png', RENDER_SCALE // 2 + 1).convert_alpha(),
        ]
        # Chmury (orct)
        rClouds : list  = []
        for i in range(0, len(Clouds), 1):
            rClouds.append(Clouds[i].get_rect())
        #
        rClouds[0].y = GS['ApplicationSize'][1] // 2 - Clouds[0].get_height()
        rClouds[1].y = GS['ApplicationSize'][1] // 2 - Clouds[1].get_height() + 48
        rClouds[2].y = GS['ApplicationSize'][1] // 2 - Clouds[2].get_height() + 16


        # Zmienne gry
        GameOn = True
        # Zegar gry
        GameClock = pygame.time.Clock()
        giveClock(GameClock)

        # Gameover
        GameoverScreenSurface = pygame.surface.Surface((GS['ApplicationSize'][0], GS['ApplicationSize'][1]), pygame.SRCALPHA, 32)
        GameoverScreenSurface.fill((0, 0, 0, 95))
        GameOverImage = scaleImage('bin/images/game_over.png', RENDER_SCALE).convert_alpha()

        # Informacje o grze [game over]
        InformationLabel = FontRender.render('ZOSTAŁEŚ WYRZUCONY Z FIRMY BITS & SERVICE', True, (255, 255, 255))
        IndexLabel = FontRenderSmall.render('WSKAŹNIK POŻYTECZNOŚCI', True, (250, 250, 250))

        # ...
        GameoverScreenSurface.blit(GameOverImage, (GS['ApplicationSize'][0] // 2 - GameOverImage.get_width() // 2, GS['ApplicationSize'][1] // 2 - GameOverImage.get_height()))
        GameoverScreenSurface.blit(InformationLabel, (GS['ApplicationSize'][0] // 2 - GameOverImage.get_width() // 2 + 32, GS['ApplicationSize'][1] // 2 + (GameOverImage.get_height() // 2)))
        
        # Obiekt pauseScreen służący do stopowania gry
        pauseScreenOb = pauseScreen(display)
        
        # usuwanie devmoda
        save.set("devmode", False)

        # Gracz
        kera = Player("./bin/images/player/init.json", 0, 0)
        kera.rect.x = GS['ApplicationSize'][0] - round(kera.emote_idle.get_width() * 1.5) - 112
        kera.rect.y = GS['ApplicationSize'][1] - kera.emote_idle.get_height() - 64
        
        # System osiągnieć (Inicjalizacja)
        achievement.configure(display)
        # achievement("uruchomienie")
        
        # okna
        game.window.startTask(screen=display)
        game.window.eraseWindows()

        
        # game.client.clientGroup.empty()
        game.client.startTask(screen=display)
        
        # ładuj klientów z sava gdy gra jest do włączenia
        if GameOn:
            game.client.restore()
        
        # osiągniecie za włączenie gry :3
        achievement.pointHere('firstJob')
        
        # funkcja ułatwiająca
        async def waitForOther():
            await asyncio.sleep(0.00002)
        
        paused : bool = False

        if GameOn:
            pygame.mixer.music.load('./bin/audio/gameplay_theme.wav')
            pygame.mixer.music.set_volume(GS['soundMusic'] * GS['soundAll'])
            pygame.mixer.music.play(-1, 0)

        while GameOn:
            await waitForOther()
            # obsługa eventów 

            answers : list = [
                save.getSafe('player.correct_ans', default=0),
                save.getSafe('player.incorrect_ans', default=0)
            ]
            
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
                            # case pygame.K_LEFT:
                            #     save.set('player.ratiolevel', save.getSafe('player.ratiolevel', default=0)-1)
                            # case pygame.K_RIGHT:
                            #     save.set('player.ratiolevel', save.getSafe('player.ratiolevel', default=0)+1)
                            case pygame.K_UP:
                                if not game.window.checkWindow("gate_gui"):
                                    pass

    
            # obliczanie elementów gry
            if pauseScreenOb.getState():
                if not paused:
                    pygame.mixer.music.pause()
                    paused = True
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
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False

                for i in range(0, len(rClouds), 1):
                    if rClouds[i].x < -Clouds[0].get_width():
                        rClouds[i].x = GS['ApplicationSize'][0] + 100
                        rClouds[i].y = rand.randint(250, GS['ApplicationSize'][1] - 300)
                
                # chmurki
                rClouds[0].x -= 1
                rClouds[1].x -= 3
                rClouds[2].x -= 2
                
            # renderowanie gry
            display.fill((0, 0, 0))

            # Chmury
            for i in range(0, len(Clouds), 1):
                display.blit(Clouds[i], (rClouds[i]))

            # Tło "behind"
            display.blit(BackgroundBehind, (0, -64))
            # Siedziba główna
            display.blit(Background, (0, 0))
            # Filter
            display.blit(BackgroundFilter, (0, 0))

            # Stats
            display.blit(Board, (rBoard.x, rBoard.y))
            CorrectAnswersLabel = FontBitRender.render('POPRAWNYCH ODPOWIEDZI: {}'.format(str(answers[0])), True, (250, 250, 250))
            IncorrectAnswersLabel = FontBitRender.render('NIEPOPRAWNYCH ODPOWIEDZI: {}'.format(str(answers[1])), True, (250, 250, 250))
            display.blit(CorrectAnswersLabel, (rBoard.x + 15, (rBoard.y * -1) + 25))
            display.blit(IncorrectAnswersLabel, (rBoard.x + 15, (rBoard.y * -1) + 75))
            
            # Renderowanie gracza
            display.blit(kera.current_img, (kera.rect.x, kera.rect.y))

            

            # Renderowanie objektów
            display.blit(Stuff, (StuffRect.x, StuffRect.y))

            # Renderowanie klientów 
            game.client.clientGroup.draw(display)
            
            # renderowanie efektów dla klientów
            game.client.clientEffectGroup.draw(display)

            if kera.gameover:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                display.blit(GameoverScreenSurface, (0, 0))
            else:
                # Progress bar
                display.blit(UsefulnessBar, (UsefulnessBarRect.x, UsefulnessBarRect.y))
                display.blit(IndexLabel, (UsefulnessBarRect.x, UsefulnessBarRect.y - 28))

                # Layout
                ub_bars = generate_use_bars(save.getSafe('player.ratiolevel', default=0))
                
                if not isinstance(ub_bars, str):
                    # temp
                    temp_x = 0

                    # Render barów dla wskaźnika 
                    for bar in list(ub_bars):
                        bar[1].x, bar[1].y = (ub_x + 2) + temp_x, (ub_y + 2)

                        temp_x += bar[0].get_width()

                        display.blit(bar[0], (bar[1].x, bar[1].y))
                
            # renderowanie powiadomień o poprawnej odpowiedzi
            answerIndicator.indicatorGroup.draw(display)
                
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

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
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
