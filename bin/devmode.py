# -----------------------------
# devmode.py
# zarządzanie 
# -----------------------------

# importy ogólne
import pygame
from pygame import Vector2
import asyncio
import functools

# importy lokalne
import bin.savemanager as sm
import bin.achievements as ach
import bin.fonts as fn

# lista spritów
devModeSprites = pygame.sprite.Group()

# sprity poszczególne
s1 = None
s2 = None
s3 = None
s4 = None

# dodatkowe info
isrunning = False
clockRef: None | pygame.time.Clock = None


# funkcja do dawania clocka bo importowanie sie popsuje w takim wypadku
def giveClock(clock):
    global clockRef
    clockRef = clock

# pętla ogólna
async def __loop():
    # globaliki
    global s1
    global s2
    global s3
    global s4
    
    while True:
        # savemanager
        _m = sm.get(alwaysNew=False)
        
        # aktulizacja danych
        s1.image = fn.getfonts()['TINY_COMICSANS'].render(f"{len(asyncio.tasks.all_tasks())} tasks", True, (0,0,0)).convert_alpha()
        
        def _r(a,b):
            return f"{a}, {b}"
        s2.image = fn.getfonts()['KINDATINY_COMICSANS'].render(f"{functools.reduce(_r, [task.get_name() for task in asyncio.tasks.all_tasks()])}", True, (0,0,0)).convert_alpha()
        
        s3.image = fn.getfonts()['TINY_COMICSANS'].render(f"{round(clockRef.get_fps(),2)} FPS {clockRef.get_time()} MS", True, (0,0,0)).convert_alpha()
        
        s4.image = fn.getfonts()['TINY_COMICSANS'].render(f"mousePos: {pygame.mouse.get_pos()}, mousePressed: {pygame.mouse.get_pressed()}", True, (0,0,0)).convert_alpha()
            
        # sprawdzanie czy devmode nie został przerwany jeżeli tak, to przerywa taska    
        if not _m.get("devmode", default=False):
            print("h")
            s1 = None
            s2 = None
            s3 = None
            s4 = None
            devModeSprites.empty()
            break
        
        await asyncio.sleep(0.1)
            
# uruchamianie dev moda
def runDevMode():
    # globaliki
    global s1
    global s2
    global s3
    global s4
    global clockRef
    
    s1 = pygame.sprite.Sprite()
    s1.image = fn.getfonts()['TINY_COMICSANS'].render(f"{len(asyncio.tasks.all_tasks())} tasks", True, (0,0,0)).convert_alpha()
    s1.rect = s1.image.get_rect()
    
    s2 = pygame.sprite.Sprite()
    def _r(a,b):
        return f"{a}, {b}"
    s2.image = fn.getfonts()['KINDATINY_COMICSANS'].render(f"{functools.reduce(_r, [task.get_name() for task in asyncio.tasks.all_tasks()])}", True, (0,0,0)).convert_alpha()
    s2.rect = s2.image.get_rect()
    s2.rect.topleft += Vector2(0,20)
    
    s3 = pygame.sprite.Sprite()
    s3.image = fn.getfonts()['TINY_COMICSANS'].render(f"{round(clockRef.get_fps(),2)} FPS {clockRef.get_time()} MS", True, (0,0,0)).convert_alpha()
    s3.rect = s1.image.get_rect()
    s3.rect.topleft += Vector2(0,40)
    
    s4 = pygame.sprite.Sprite()
    s4.image = fn.getfonts()['TINY_COMICSANS'].render(f"mousePos: {pygame.mouse.get_pos()}, mousePressed: {pygame.mouse.get_pressed()}", True, (0,0,0)).convert_alpha()
    s4.rect = s1.image.get_rect()
    s4.rect.topleft += Vector2(0,60)
    
    devModeSprites.add(s1, s2, s3, s4)
    
    asyncio.create_task(__loop(), name="devmodeManager")
