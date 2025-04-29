import numpy as np
import random

class BoardState():
    def __init__(self):
        self.DIMENSIONS = 20
        self.textures = ['grass', 'mud', 'rocks', 'sand']
        # losowanie pól
        self.board = [[random.choice(self.textures) for _ in range(self.DIMENSIONS)] for _ in range(self.DIMENSIONS)] 
        self.playerPos = (19, 0)
        self.end = (0,19)
        self.moveLog = []

# macierz 20x20 
# lewy gorny [0,0]
# prawy gorny [19,0]
# lewy dolny [0,19]
# prawy dolny [19, 19]

    def stepTowardsEnd(self):
        r, c = self.playerPos
        end_r, end_c = self.end
        # Zapisz bieżącą pozycję jako odwiedzoną
        self.moveLog.append(self.playerPos)
        # Oblicz różnicę
        dr = end_r - r
        dc = end_c - c
        # Przesuń się o 1 w kierunku celu (w pionie i/lub poziomie)
        new_r = r + (1 if dr > 0 else -1 if dr < 0 else 0)
        new_c = c + (1 if dc > 0 else -1 if dc < 0 else 0)
        self.playerPos = (new_r, new_c)

