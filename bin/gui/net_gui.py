import random
import pygame

import bin.window as wn
from bin.function import readJSON, scaleImage
import bin.savemanager as sm




def generate_gate(newQuestion: dict, client):
    
    # zabezpieczenie by okno się nie pojawiało w przypadku gameover
    _s = sm.get(alwaysNew=False)
    if(_s.getSafe('player.ratiolevel', default=0) <= 0): return
    
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
            _s.set("player.ratiolevel", _s.get('player.ratiolevel') + 1)
            _s.set('player.correct_ans', _s.get('player.correct_ans') + 1)
            kwargs['me'].getBody().getWindow().kill()
            
            client.correctAnswer()
        else:
            # informacja o złej odpowiedzi
            # _body: wn.windowBody = kwargs['me'].getBody()
            
            # # tworzenie informacji o złej odpowiedzi
            # if len(_body.findByName("n")) == 0:
            #     _body.add(
            #         wn.windowText(
            #             fontName="VERYSMALL_COMICSANS", 
            #             text="niepoprawna odpowiedz!", 
            #             color=(230,10,10),
            #             cords=(30, 220),
            #             name="n"
            #         )
            #     )
            _s = sm.get(alwaysNew=False)
            _s.set("player.ratiolevel", _s.get('player.ratiolevel') - 1)
            _s.set('player.incorrect_ans', _s.get('player.incorrect_ans') + 1)
            kwargs['me'].getBody().getWindow().kill()
            
            client.wrongAnswer()
            
            
            # # ustawianie spowrotem tekstu (przy jednym evencie jest usuwany, przy k) 
            # kwargs['me'].getBody().findByName("textBox")[0].setText(_text)
            
            # zwrócenie True przy jednym evencie blokuje usuwanie tekstu
            return True
    
    def handlerForChoice(*args, **kwargs):
        _s = sm.get(alwaysNew=False)
        print(kwargs['optionType'], kwargs['me'].getBody().getWindow().storage['correct'], kwargs['optionType'] == kwargs['me'].getBody().getWindow().storage['correct'])
        if kwargs['optionType'] == kwargs['me'].getBody().getWindow().storage['correct']:
            _s.set("player.ratiolevel", _s.get('player.ratiolevel') + 1)
            _s.set('player.correct_ans', _s.get('player.correct_ans') + 1)
            _s.set('player.correct_combo', _s.get('player.correct_combo') + 1)
            client.correctAnswer()
            kwargs['me'].getBody().getWindow().kill()
        else:
            _s.set("player.ratiolevel", _s.get('player.ratiolevel') - 1)
            _s.set('player.incorrect_ans', _s.get('player.incorrect_ans') + 1)
            _s.set('player.correct_combo', 0)
            client.wrongAnswer()
            kwargs['me'].getBody().getWindow().kill()
    
    # obiekt okna
    window = wn.window(
        name="net_gui",
        size=(500,300),
        body=wn.windowBody(
            wn.windowText(fontName="MEDIUM_TAHOMA", text="SIECI TIME", cords=(30,0), color=(233,233,233)),
            wn.windowText(fontName="VERYSMALL_TAHOMA", text="Dane:", cords=(10,113), color=(233,233,233)),
            wn.windowText(fontName="VERYSMALL_TAHOMA", text=newQuestion['Q_DATA'], cords=(15,134), color=(233,233,233)),
            
            
        )
    ).setPosition((50,50))
    
    if newQuestion['ANSWER'] in [False, True]:
        window.getBody().add(
        wn.windowText(fontName="MEDIUM_CONSOLAS", text="TAK", cords=(165, 200), color=(10, 240, 30))
        .addClickListener(lambda *args, **kwargs: handlerForChoice(*args, optionType=True, **kwargs)),
        wn.windowText(fontName="MEDIUM_CONSOLAS", text="NIE", cords=(285, 200), color=(240, 10, 30))
        .addClickListener(lambda *args, **kwargs: handlerForChoice(*args, optionType=False, **kwargs))
        )   
    else:
        window.getBody().add(
        _t := wn.windowTextBox(cords=(((500//2) - (40 * 4)) // 2 + 4, 180), xsize=40, name="textBox").
        setRegex("^[0-9\.]*$").setReturnListener(handler),
        wn.windowText(fontName="MEDIUM_CONSOLAS", text="ZATWIERDŹ", cords=((500//2) - ((30 * 3) + 4), 235), color=(240, 240, 240))
        .addClickListener(handler)
        )
        window.addObjectToListen(_t)
    
    
    # zapisanie w storagu poprawnej odpowiedzi
    window.storage['correct'] = newQuestion['ANSWER']
    #print(newQuestion)
    #print(window.storage['correct'], newQuestion['ANSWER'])
    
    # zrobienie napisu z pytaniem
    for id, element in enumerate(text):
        window.getBody().add(
            wn.windowText(fontName="VERYSMALL_COMICSANS", text=element, cords=(10,70+(20*id)), color=(233,233,233))
            )
        
    
    return window
    