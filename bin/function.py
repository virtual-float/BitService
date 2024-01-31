# Importuj moduły niezbędne
import os, json
from tkinter import messagebox

# Tryb kodowania znaków [ string ] ( Zmienna stała )
ENCODING_MODE : str = "UTF-8"

# Funkcja, która umożliwia odczytywanie danych z struktury json 
# Funkcja zwraca dane json w postaci słownika [ dict ]
def readJSON(localizationPath: str) -> dict:
    try:
        # Jeżeli ścieżka pliku nie kończy się na .json, zwróć błąd
        if not localizationPath.endswith(".json"):
            messagebox.showerror('Rozszerzenie', f'Rozszerzenie pliku {localizationPath} nie jest typu json!')

        # Otwórz plik json 
        with open(os.getcwd() + localizationPath, mode='r', encoding=ENCODING_MODE) as file:
            # Jeżeli plik jest odczytywalny, zwróć dane z pliku json
            if file.readable():
                # Zwróć dane z pliku json jako słownik
                return json.load(file)
            
    except json.JSONDecodeError:
        # Zwróć poprawny komunikat jeśli nastąpił błąd z dekodowaniem znaków
        messagebox.showerror('Dekodowanie', f'Plik {localizationPath} nie mógł zostać zdekodowany na UTF-8')
    except OSError:
        # Zwróć poprawny komunikat jeśli nastąpił błąd z otwarciem pliku
        messagebox.showerror('Dostępność', f'Plik {localizationPath} nie mógł być otworzony ')
    # Fabrycznie zwróć pusty słownik
    return {}

# Funkcja, która umożliwia aktualizowanie danych do pliku json
# oraz zwraca wynik wykonania aktualizacji
def updateJSON(localizationPath: str, newData: dict) -> bool:
    try:
        # Jeżeli ścieżka pliku nie kończy się na .json, zwróć błąd
        if not localizationPath.endswith(".json"):
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
        messagebox.showerror('Dostępność', f'Plik {localizationPath} nie mógł być otworzony')
    # Fabrycznie zwróć wynik aktualizacji danych json
    return False

# Funkcja, która zwróci wszelkie dane z słowników na całą jedną płaszczyzne
def NestedDictValues(d):
  for v in d.values():
    if isinstance(v, dict):
      yield from NestedDictValues(v)
    else:
      yield v

# Funkcja, która zwróci zaszyfrowane dane w postaci szesnastkowej
def hex_crypt(value: str | int) -> list[hex]:
    return list(map(lambda letter: hex(ord(letter)), list(value)))

# Funkcja, która zwraca odszyfrowane dane z postaci szesnastkowej
def hex_decrypt(value: list[hex]) -> str:
    return ''.join(map(lambda hex_value: chr(int(hex_value, base=16)), value))