import random
import pygame

import bin.window as wn
from bin.function import readJSON, scaleImage




def generate_gate():
    questions = readJSON("./bin/quests/gate_question.json")
    print(questions)
    newQuestion = questions[random.randint(0, len(questions)-1)]
    
    text : tuple[str] = newQuestion['QUESTION'].split("\n")
    
    def handler(*args, **kwargs):

        
        # pozyskiwanie tekstu niezależne od rodzaju eventu
        if not 'text' in kwargs:
            _text = kwargs['me'].getBody().findByName("textBox")[0].getText()
            kwargs['me'].getBody().findByName("textBox")[0].setText("")
        else:
            _text = kwargs['text']
    
        # zabezpieczenie przed niepotrzebnym wysyłaniem pustaków
        if _text == "": return
        
        correct = kwargs['me'].getBody().getWindow().storage['correct']
    
        print(f"twoje: {_text}, poprawna: {correct}")
    
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
    
    window.storage['correct'] = newQuestion['ANSWER']
    
    for id, element in enumerate(text):
        window.getBody().add(
            wn.windowText(fontName="VERYSMALL_COMICSANS", text=element, cords=(10,70+(20*id)))
            )
        
    
    return window
    