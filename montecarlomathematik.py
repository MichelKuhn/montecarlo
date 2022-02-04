# Monte Carlo Mathematik
import numpy
import numpy.random as random
from enum import IntEnum
import matplotlib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")


class Sortierung(IntEnum):
    KEINE = 0
    PFADLAENGE = 1
    GEWINN = 2


class Strategie(IntEnum):
    WAHRSCHEINLICHKEIT = 0
    ERWARTUNG = 1
    GEWINN = 2


class Ereignis:
    def __init__(self, wsk, gewinn, verlust=0):
        self.wahrscheinlichkeit = random.normal(wsk, 5)
        self.gewinn = gewinn
        self.verlust = verlust

    def wurf(self):
        wurf = random.randint(1, 100)
        return wurf <= self.wahrscheinlichkeit

    def eintreten(self):
        if self.wurf():
            return self.gewinn
            
        return -self.verlust

    def get_wsk(self):
        return self.wahrscheinlichkeit

    def get_erwartung(self):
        return self.wahrscheinlichkeit * self.gewinn + (1 - self.wahrscheinlichkeit) * self.verlust

    def get_gewinn(self):
        return self.gewinn


class Pfad:
    def __init__(self, laenge, akteur):
        self.gesamtlaenge = laenge
        self.zeit = 0
        self.akteur = akteur
        self.cash = 0

    def ereignen(self, ereignis):
        self.zeit += 1
        if self.akteur.strategie is Strategie.WAHRSCHEINLICHKEIT:
            if ereignis.get_wsk() < 50:
                return
        elif self.akteur.strategie is Strategie.ERWARTUNG:
            if ereignis.get_erwartung() < 0:
                return
        elif self.akteur.strategie is Strategie.GEWINN:
            if ereignis.get_gewinn() < 0:
                return

        self.cash += ereignis.eintreten()
        if self.cash <= 0:
            return


class Akteur:
    def __init__(self, strategie=Strategie.WAHRSCHEINLICHKEIT):
        self.strategie = strategie


class Terminal:
    def __init__(self, anzahl_pfade, pool):
        self.anzahl_pfade = anzahl_pfade
        self.pfade = []
        self.ereignispool = pool
        self.laengster_pfad = 0

        for i in range(anzahl_pfade):
            pfadlaenge = random.randint(10, 1000)
            if pfadlaenge > self.laengster_pfad:
                self.laengster_pfad = pfadlaenge

            wuerfel = random.randint(1, 7)
            if wuerfel == 6:
                pfad = Pfad(pfadlaenge, Akteur(Strategie.GEWINN))
            elif wuerfel % 2 == 0:
                pfad = Pfad(pfadlaenge, Akteur(Strategie.WAHRSCHEINLICHKEIT))
            else:
                pfad = Pfad(pfadlaenge, Akteur(Strategie.ERWARTUNG))
            self.pfade.append(pfad)

    def ausfuehren(self, sortierung=Sortierung.KEINE):
        pfadleangen = []
        gewinne = []
        strategie = []

        for i in range(self.laengster_pfad):
            for pfad in self.pfade:
                if pfad.zeit < pfad.gesamtlaenge:
                    pfad.ereignen(ereignispool[random.randint(len(ereignispool))])

        if sortierung is Sortierung.PFADLAENGE:
            self.pfade.sort(key=lambda x: x.laenge)
        elif sortierung is Sortierung.GEWINN:
            self.pfade.sort(key=lambda x: x.cash, reverse=True)

        for pfad in self.pfade:
            pfadleangen.append(pfad.zeit)
            gewinne.append(pfad.cash)
            strategie.append(int(pfad.akteur.strategie))
            print(str(pfad.zeit) + ": " + str(pfad.cash))

        return [pfadleangen, gewinne, strategie]


class Sitzung:
    def __init__(self):
        layout = [[sg.Text("Pfadsimulation mit unterschiedlichen Strategien")],
                  [sg.Canvas(key="-CANVAS-")],
                  [sg.Button("OK")]]
        self.window = sg.Window("Monte Carlo Mathematik", layout, finalize=True)

        self.fig = None
        self.ax = None

    def plot_generieren(self, daten):
        self.fig, self.ax = plt.subplots()
        colormap = numpy.array(["#0000FF", "#00FF00", "#FF0066"])
        self.ax.scatter(daten[0], daten[1], s=50, c=colormap[daten[2]])
        self.ax.set_title('Endzustand der Pfade')
        self.ax.set_xlabel('Pfadlaenge')
        self.ax.set_ylabel('Gewinn')

        figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.window["-CANVAS-"].TKCanvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg


ereignispool = [Ereignis(50, 100, 100), Ereignis(95, 10, 100), Ereignis(25, 150, 50), Ereignis(75, 50, 150)]
terminal = Terminal(200, ereignispool)
pfaddaten = terminal.ausfuehren(Sortierung.GEWINN)

sitzung = Sitzung()
sitzung.plot_generieren(pfaddaten)

while True:
    event, values = sitzung.window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break

sitzung.window.close()
