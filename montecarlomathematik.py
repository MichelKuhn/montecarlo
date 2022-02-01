# Monte Carlo Mathematik
import random
from enum import Enum
import matplotlib.pyplot as plt
import pylab


class Sortierung(Enum):
    KEINE = 1
    PFADLAENGE = 2
    GEWINN = 3


class Ereignis:
    def __init__(self, wahrscheinlichkeit, kraft, fehler=0):
        self.wahrscheinlichkeit = random.randint(wahrscheinlichkeit - fehler, wahrscheinlichkeit + fehler)
        self.kraft = kraft

    def wurf(self):
        wurf = random.randint(1, 100)
        return wurf <= self.wahrscheinlichkeit

    def eintreten(self):
        if self.wurf():
            return self.kraft

        return 0


class Wette(Ereignis):
    def __init__(self, wsk, gewinn, verlust):
        Ereignis.__init__(self, wsk, gewinn)
        self.verlust = verlust

    def eintreten(self):
        if self.wurf():
            return self.kraft
        else:
            return -self.verlust


class Pfad:
    def __init__(self, laenge, ereignis):
        self.laenge = laenge
        self.cash = 0

        for i in range(laenge):
            self.cash += ereignis.eintreten()
            if self.cash <= 0:
                return


class Terminal:
    def __init__(self, anzahl_pfade):
        self.anzahl_pfade = anzahl_pfade
        self.pfade = []
        for i in range(anzahl_pfade):
            pfadlaenge = random.randint(10, 1000)
            pfad = Pfad(pfadlaenge, Wette(95, 100, 1000))
            self.pfade.append(pfad)

    def ausfuehren(self, sortierung=Sortierung.KEINE):
        pfadleangen = []
        gewinne = []
        if sortierung is Sortierung.PFADLAENGE:
            self.pfade.sort(key=lambda x: x.laenge)
        elif sortierung is Sortierung.GEWINN:
            self.pfade.sort(key=lambda x: x.cash, reverse=True)

        for pfad in self.pfade:
            pfadleangen.append(pfad.laenge)
            gewinne.append(pfad.cash)
            print(str(pfad.laenge) + ": " + str(pfad.cash))

        return [pfadleangen, gewinne]


terminal = Terminal(100)
daten = terminal.ausfuehren(Sortierung.GEWINN)

fig, ax = plt.subplots()

# scatter the sepal_length against the sepal_width
ax.scatter(daten[0], daten[1])
# set a title and labels
ax.set_title('Iris Dataset')
ax.set_xlabel('Pfadlaenge')
ax.set_ylabel('Gewinn')

pylab.show()
