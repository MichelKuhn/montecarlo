#Monte Carlo Mathematik
import random

#Funktional
def bedingtes_ereignis(wahrscheinlichkeit):
    wurf = random.randint(1, 100)
    return wurf <= wahrscheinlichkeit

def sample_path(laenge, wahrscheinlichkeit):
    cash = 0
    for i in range(laenge):
        ereignis = bedingtes_ereignis(wahrscheinlichkeit)
        if ereignis:
            cash += 1

    return cash


for i in range(1, 10):
    print(sample_path(100, 50))

#Objektorientiert
class Ereignis:
    def __init__(self, wahrscheinlichkeit, kraft, fehler = 0):
        self.wahrscheinlichkeit = random.randint(wahrscheinlichkeit - fehler, wahrscheinlichkeit + fehler)
        self.kraft = random.randint(kraft - fehler, kraft + fehler)

    def eintreten(self):
        wurf = random.randint(1, 100)
        if wurf <= self.wahrscheinlichkeit:
            return self.kraft

        return 0

cash = 0
for i in range(100):
    ereignis = Ereignis(50, 5, 1)
    cash += ereignis.eintreten()
    
