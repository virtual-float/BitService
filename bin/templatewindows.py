# UWAGA! PLIK NIEUŻYWANY

#################################
# templatewindow.py      
#
# Cel: brak     
#################################


import bin.window as wn

# szatan tworzył regexa

def question(name: str) -> wn.window:
    _window = wn.window(name=name, size=(400,250), body=wn.windowBody(
        wn.windowText(fontName='MEDIUM_COMICSANS', text='Zadanie', cords=(10, 0), color=(255,255,255)),
        wn.windowText(fontName='VERYSMALL_COMICSANS', text='Adres ip i jakieś coś', cords=(10, 45), color=(136,136,136)),
        wn.windowText(fontName='VERYSMALL_COMICSANS', text='Adres broadcast', cords=(10, 100)),
        textbox1 := wn.windowTextBox(startingText="", cords=(10, 140), xsize=30, marginleft=5, name="test")
        .setRegex('^[0-9]{0,3}|[0-9]{1,3}\.|[0-9]{1,3}\.[0-9]{0,3}|[0-9]{1,3}\.[0-9]{1,3}\.|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{0,3}$'),
        wn.windowText(fontName='VERYSMALL_COMICSANS', text='ZATWIERDZ', cords=(265, 220)).addClickListener(
            lambda me, pressed, pos, posRelative, events, window: window.kill()
        )
    )).setPosition((200,100)).addObjectToListen(textbox1)

    return _window