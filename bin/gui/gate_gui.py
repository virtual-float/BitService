import random
import pygame

import bin.window as wn
from bin.function import readJSON, scaleImage
import bin.savemanager as sm




def generate_gate():
    questions = readJSON("./bin/quests/gate_question.json")
    print(questions)
    newQuestion = questions[random.randint(0, len(questions)-1)]
    
    text : tuple[str] = newQuestion['QUESTION'].split("\n")
    
    def handler(*args, **kwargs):

        
        # pozyskiwanie tekstu niezależne od rodzaju eventu
        if not 'text' in kwargs:
            _text = kwargs['me'].getBody().findByName("textBox")[0].getText()
            # kwargs['me'].getBody().findByName("textBox")[0].setText("")
        else:
            _text = kwargs['text']
    
        # zabezpieczenie przed niepotrzebnym wysyłaniem pustaków
        if _text == "": return
        
        correct = kwargs['me'].getBody().getWindow().storage['correct']
        if(correct == _text):
            # poprawna odpowiedź
            _s = sm.get(alwaysNew=False)
            _s.set("player.ratiolevel",
                    _s.get('player.ratiolevel')+1)
            kwargs['me'].getBody().getWindow().kill()
        else:
            # informacja o złej odpowiedzi
            _body: wn.windowBody = kwargs['me'].getBody()
            
            # tworzenie informacji o złej odpowiedzi
            if len(_body.findByName("n")) == 0:
                _body.add(
                    wn.windowText(
                        fontName="VERYSMALL_COMICSANS", 
                        text="niepoprawna odpowiedz!", 
                        color=(230,10,10),
                        cords=(30, 220),
                        name="n"
                    )
                )
            
            # # ustawianie spowrotem tekstu (przy jednym evencie jest usuwany, przy k) 
            # kwargs['me'].getBody().findByName("textBox")[0].setText(_text)
            
            # zwrócenie True przy jednym evencie blokuje usuwanie tekstu
            return True
    
    # obiekt okna
    window = wn.window(
        name="gate_gui",
        size=(500,300),
        body=wn.windowBody(
            wn.windowText(fontName="MEDIUM_COMICSANS", text="Problem z bramkami!", cords=(60,0)),
            wn.windowElement(scaleImage(newQuestion['Q_DATA'],3), cords=(300,55)),
            _t := wn.windowTextBox(cords=(40, 180), xsize=40, name="textBox").
            setRegex("^[0-9]*$").setReturnListener(handler),
            wn.windowText(fontName="SMALL_COMICSANS", text="SPRAWDZ", cords=(185, 255))
            .addClickListener(handler)
            
            
        )
    ).setPosition((50,50)).addObjectToListen(_t)
    
    # zapisanie w storagu poprawnej odpowiedzi
    window.storage['correct'] = newQuestion['ANSWER']
    
    # zrobienie napisu z pytaniem
    for id, element in enumerate(text):
        window.getBody().add(
            wn.windowText(fontName="VERYSMALL_COMICSANS", text=element, cords=(10,70+(20*id)))
            )
        
    
    return window
    