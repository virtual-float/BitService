#################################
# function.py      
#
# Cel: różne podręczne funkcje         
#################################


# Importuj moduły niezbędne
import os, json
from tkinter import messagebox
import pygame

# Tryb kodowania znaków [ string ] ( Zmienna stała )
ENCODING_MODE : str = "UTF-8"

# Funkcja, która umożliwia odczytywanie danych z struktury json 
# Funkcja zwraca dane json w postaci słownika [ dict ]
def readJSON(localizationPath: str, showErrors:bool=True) -> dict:
    '''Funkcja, która umożliwia odczytywanie danych z struktury json\n
        Funkcja zwraca dane json w postaci słownika [ dict ]'''
    try:
        # Jeżeli ścieżka pliku nie kończy się na .json, zwróć błąd
        if not localizationPath.endswith(".json"):
            if showErrors: 
                messagebox.showerror('Rozszerzenie', f'Rozszerzenie pliku {localizationPath} nie jest typu json!')

        # Otwórz plik json 
        with open(os.getcwd() + localizationPath, mode='r', encoding=ENCODING_MODE) as file:
            # Jeżeli plik jest odczytywalny, zwróć dane z pliku json
            if file.readable():
                # Zwróć dane z pliku json jako słownik
                return json.load(file)
            
    except json.JSONDecodeError:
        # Zwróć poprawny komunikat jeśli nastąpił błąd z dekodowaniem znaków
        if showErrors: 
            messagebox.showerror('Dekodowanie', f'Plik {localizationPath} nie mógł zostać zdekodowany na UTF-8')
    except OSError:
        # Zwróć poprawny komunikat jeśli nastąpił błąd z otwarciem pliku
        if showErrors: 
            messagebox.showerror('Dostępność', f'Plik {localizationPath} nie mógł być otworzony ')
    # Fabrycznie zwróć pusty słownik
    return {}


# Funkcja, która umożliwia aktualizowanie danych do pliku json
# oraz zwraca wynik wykonania aktualizacji
def updateJSON(localizationPath: str, newData: dict, showErrors:bool=True) -> bool:
    '''Funkcja, która umożliwia aktualizowanie danych do pliku json oraz zwraca wynik wykonania aktualizacji'''
    try:
        # Jeżeli ścieżka pliku nie kończy się na .json, zwróć błąd
        if not localizationPath.endswith(".json"):
            if showErrors:
                messagebox.showerror('Rozszerzenie', f'Rozszerzenie {localizationPath} pliku nie jest typu json!')

        # Otwórz plik json
        with open(os.getcwd() + localizationPath, mode='w', encoding=ENCODING_MODE) as file:
            # Ustaw kursor pliku na pozycji początkowej (0)
            file.seek(0)
            # Wpisz nowe dane do pliku json
            file.write(json.dumps(newData, indent=4))

            # Zwróć wynik aktualizacji
            return True
    except OSError:
        # Zwróć poprawny komunikat jeśli nastąpił błąd z otwarciem pliku
        if showErrors:
            messagebox.showerror('Dostępność', f'Plik {localizationPath} nie mógł być otworzony')
    # Fabrycznie zwróć wynik aktualizacji danych json
    return False


def NestedDictValues(d):
    '''Funkcja, która zwróci wszelkie dane z słowników na całą jedną płaszczyzne\n
    Disclaimer: to jest funkcja z stackOverFlow, nie rościmy sobie do niej prawa,\n
    jednakże jest taka prosta że prawdopodobnie napisano ja już miliard razy\n'''
    for v in d.values():
        if isinstance(v, dict):
            yield from NestedDictValues(v)
        else:
            yield v


def hex_crypt(value: str | int, asciiEnabled: bool, sep: str = '') -> str:
    '''Funkcja, która zwróci zaszyfrowane dane w postaci szesnastkowej'''
    if asciiEnabled:
        return sep.join((map(lambda letter: hex(ord(letter)).removeprefix('0x'), value.split(sep))))
    return sep.join((map(lambda letter: hex(int(letter, base=0)).removeprefix('0x'), value.split(sep))))


def hex_decrypt(value: str, asciiEnabled: bool, sep: str = '') -> str:
    '''Funkcja, która zwraca odszyfrowane dane z postaci szesnastkowej'''
    if asciiEnabled:
        return sep.join(map(lambda hex_value: chr(int(hex_value, base=16)), value.split(sep)))
    return sep.join(map(lambda hex_value: str(int(hex_value, base=16)), value.split(sep)))


# TO BYŁO DO TESTOWANIA
# dane = '7F.0.1.0'

# print(hex_decrypt(dane, False, '.'))

# print(hex_crypt('127.0.1.0', False, '.'))


# Funkcja, która zwraca zeskalone obrazy
def scaleImage(imgSource: str, scaleBy: int) -> pygame.Surface:
    image = pygame.image.load(imgSource)

    return pygame.transform.scale(image, (image.get_width() * scaleBy, image.get_height() * scaleBy))