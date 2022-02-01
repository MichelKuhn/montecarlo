#Monte Carlo Mathematik
import random
from enum import Enum

class Sortierung(Enum):
    KEINE = 1
    PFADLAENGE = 2
    GEWINN = 3

class Ereignis:
    def __init__(self, wahrscheinlichkeit, kraft, fehler = 0):
        self.wahrscheinlichkeit = random.randint(wahrscheinlichkeit - fehler, wahrscheinlichkeit + fehler)
        self.kraft = random.randint(kraft - fehler, kraft + fehler)

    def eintreten(self):
        wurf = random.randint(1, 100)
        if wurf <= self.wahrscheinlichkeit:
            return self.kraft

        return 0

class Pfad:
    def __init__(self, laenge):
        self.ereignisse = []
        self.laenge = laenge
        self.cash = 0
        
        for i in range(laenge):
            ereignis = Ereignis(50, 5, 1)
            self.cash += ereignis.eintreten()


class Terminal:
    def __init__(self, anzahl_pfade):
        self.anzahl_pfade = anzahl_pfade
        self.pfade = []
        for i in range(anzahl_pfade):
            pfadlaenge = random.randint(10, 1000)
            pfad = Pfad(pfadlaenge)
            self.pfade.append(pfad)

    def ausfuehren(self, sortierung=Sortierung.KEINE):
        if sortierung is Sortierung.PFADLAENGE:
            self.pfade.sort(key=lambda x: x.laenge)
        elif sortierung is Sortierung.GEWINN:
            self.pfade.sort(key=lambda x: x.cash, reverse=True)

        for pfad in self.pfade:
            print(str(pfad.laenge) + ": " + str(pfad.cash))
                
terminal = Terminal(10)
print("Terminal normal:")
terminal.ausfuehren()
print("Terminal sortiert nach Pfadlänge")
terminal.ausfuehren(Sortierung.PFADLAENGE)
print("Terminal sortiert nach Gewinn")
terminal.ausfuehren(Sortierung.GEWINN)
