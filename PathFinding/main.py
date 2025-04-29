# vscode otworzyc terminal w folderze 
# ...\VisualStudioCode\pathFinding> py -m PathFinding.main

import pygame as p
from PathFinding import engine

WIDTH = 720
HEIGHT = 720
DIMENSIONS = 20
SQR_SIZE = HEIGHT//DIMENSIONS
FPS = 15 # jezeli robimy animacje jak player przechodzi do nastepnego kwadratu 
IMAGES = {}

def loadImages(): # wczytywanie obrazow
    textures = ['grass', 'mud', 'rocks', 'sand']
    for texture in textures:
        IMAGES[texture] = p.transform.scale(p.image.load("img/" + texture + ".png"), (SQR_SIZE, SQR_SIZE))
    IMAGES["player"] = p.transform.scale(p.image.load("img/player.png"), (20, 36))
    IMAGES["end"] = p.transform.scale(p.image.load("img/end.png"), (SQR_SIZE, SQR_SIZE))
    
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    p.display.set_caption("A*")

    bs = engine.BoardState()
    loadImages()

    lastMove = p.time.get_ticks() # zapisuje kiedy ostatni raz poruszyl sie gracz
    delay = 400 # przyspieszenie animacji przechodzenia do kolejnego kwadratu

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False # klikniecie wyjscia w oknie

        currentTime = p.time.get_ticks()
        if currentTime - lastMove > delay:
            if bs.playerPos != bs.end: # czy gracz dotarl do konca
                bs.stepTowardsEnd()
                lastMove = currentTime

        drawBoardState(screen, bs)
        p.display.flip() # aktualizuje ekran
        clock.tick(FPS) 
    

def drawBoardState(screen, bs):
    drawBoard(screen, bs)
    drawUsed(screen,bs)
    drawEnd(screen, bs)
    drawPlayer(screen, bs)

def drawBoard(screen, bs):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            texture = bs.board[r][c]
            screen.blit(IMAGES[texture], p.Rect(c * SQR_SIZE, r * SQR_SIZE, SQR_SIZE, SQR_SIZE))


def drawUsed(screen, bs): # przyciemnienie uzytych pól
    used = p.Surface((SQR_SIZE, SQR_SIZE), p.SRCALPHA)
    used.fill((0, 0, 0, 150))
    for r, c in bs.moveLog:
        screen.blit(used, p.Rect(c * SQR_SIZE, r * SQR_SIZE, SQR_SIZE, SQR_SIZE))

def drawPlayer(screen, bs): # wyskalowanie, wysrodkowanie player
    r, c = bs.playerPos
    x_offset = (SQR_SIZE - 20) // 2
    y_offset = (SQR_SIZE - 36) // 2
    screen.blit(IMAGES["player"], p.Rect(c * SQR_SIZE + x_offset, r * SQR_SIZE + y_offset, 20, 36))

def drawEnd(screen, bs): # flaga mety
    r, c = bs.end
    screen.blit(IMAGES["end"], p.Rect(c * SQR_SIZE, r * SQR_SIZE, SQR_SIZE, SQR_SIZE))

if __name__ == "__main__":
    main()
