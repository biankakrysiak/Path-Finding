import pygame as p
from PathFinding import engine

SIDEBAR_WIDTH = 250
GRID_WIDTH = 720
WIDTH = SIDEBAR_WIDTH + GRID_WIDTH
HEIGHT = 720
DIMENSIONS = 20
SQR_SIZE = HEIGHT // DIMENSIONS
FPS = 15
IMAGES = {}

def loadImages():
    textures = ['grass', 'mud', 'rocks', 'sand']
    for texture in textures:
        IMAGES[texture] = p.transform.scale(p.image.load("img/" + texture + ".png"), (SQR_SIZE, SQR_SIZE))
    IMAGES["player"] = p.transform.scale(p.image.load("img/player.png"), (20, 36))
    IMAGES["player2"] = p.transform.scale(p.image.load("img/player2.png"), (20, 36))
    IMAGES["end"] = p.transform.scale(p.image.load("img/end.png"), (SQR_SIZE, SQR_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    p.display.set_caption("A*")

    bs = engine.BoardState()
    loadImages()

    lastMove = p.time.get_ticks()
    delay = 400

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        currentTime = p.time.get_ticks()
        if currentTime - lastMove > delay:
            if bs.playerPos != bs.end or bs.playerPos2 != bs.end:
                if bs.playerPos != bs.end:
                    bs.stepTowardsEnd()
                if bs.playerPos2 != bs.end:
                    bs.stepTowardsEnd2()
                lastMove = currentTime

        drawBoardState(screen, bs)
        p.display.flip()
        clock.tick(FPS)

def drawBoardState(screen, bs):
    drawBoard(screen, bs)
    drawUsed(screen, bs)
    drawPlayer(screen, bs)
    drawPlayer2(screen, bs)
    drawEnd(screen, bs)
    drawSidebar(screen, bs)

def drawBoard(screen, bs):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            texture = bs.board[r][c]
            screen.blit(IMAGES[texture], p.Rect(c * SQR_SIZE + SIDEBAR_WIDTH, r * SQR_SIZE, SQR_SIZE, SQR_SIZE))

def drawUsed(screen, bs):
    used_a_star = p.Surface((SQR_SIZE, SQR_SIZE), p.SRCALPHA)
    used_a_star.fill((200, 0, 0, 140))

    used_dijkstra = p.Surface((SQR_SIZE, SQR_SIZE), p.SRCALPHA)
    used_dijkstra.fill((0, 0, 200, 120))

    for r, c in bs.moveLog:
        screen.blit(used_a_star, p.Rect(c * SQR_SIZE + SIDEBAR_WIDTH, r * SQR_SIZE, SQR_SIZE, SQR_SIZE))

    for r, c in bs.moveLog2:
        screen.blit(used_dijkstra, p.Rect(c * SQR_SIZE + SIDEBAR_WIDTH, r * SQR_SIZE, SQR_SIZE, SQR_SIZE))

def drawPlayer(screen, bs):
    r, c = bs.playerPos
    x_offset = (SQR_SIZE - 20) // 2
    y_offset = (SQR_SIZE - 36) // 2
    screen.blit(IMAGES["player"], p.Rect(c * SQR_SIZE + x_offset + SIDEBAR_WIDTH, r * SQR_SIZE + y_offset, 20, 36))

def drawPlayer2(screen, bs):
    r, c = bs.playerPos2
    x_offset = (SQR_SIZE - 20) // 2
    y_offset = (SQR_SIZE - 36) // 2
    screen.blit(IMAGES["player2"], p.Rect(c * SQR_SIZE + x_offset + SIDEBAR_WIDTH, r * SQR_SIZE + y_offset, 20, 36))

def drawEnd(screen, bs):
    r, c = bs.end
    screen.blit(IMAGES["end"], p.Rect(c * SQR_SIZE + SIDEBAR_WIDTH, r * SQR_SIZE, SQR_SIZE, SQR_SIZE))

def drawSidebar(screen, bs):
    padding = 10
    font = p.font.SysFont("arial", 18)
    bold_font = p.font.SysFont("arial", 18, bold=True)
    header_font = p.font.SysFont("arial", 20, bold=True)

    sidebar_rect = p.Rect(0, 0, SIDEBAR_WIDTH, HEIGHT)
    p.draw.rect(screen, (240, 240, 240), sidebar_rect)

    title_text = header_font.render("Terrain Difficulty", True, (0, 0, 0))
    title_x = (SIDEBAR_WIDTH - title_text.get_width()) // 2
    screen.blit(title_text, (title_x, padding))

    textures = ["grass", "sand", "mud", "rocks"]
    difficulties = [1, 2, 3, 4]
    texture_images = [p.image.load(f"img/{name}.png") for name in textures]
    texture_images = [p.transform.scale(img, (30, 30)) for img in texture_images]

    table_top = 45
    row_height = 40
    img_x = padding
    text_x = padding + 40

    for i, (img, name, diff) in enumerate(zip(texture_images, textures, difficulties)):
        y = table_top + i * row_height
        screen.blit(img, (img_x, y))
        screen.blit(font.render(name.capitalize(), True, (0, 0, 0)), (text_x, y))
        screen.blit(font.render(f"Diff: {diff}", True, (100, 100, 100)), (text_x, y + 20))
        p.draw.line(screen, (200, 200, 200), (padding, y + row_height), (SIDEBAR_WIDTH - padding, y + row_height), 1)

    result_y = y + row_height + 20
    p.draw.line(screen, (0, 0, 0), (padding, result_y - 10), (SIDEBAR_WIDTH - padding, result_y - 10), 2)
    
    results_text = header_font.render("Results", True, (0, 0, 0))
    results_x = (SIDEBAR_WIDTH - results_text.get_width()) // 2
    screen.blit(results_text, (results_x, result_y))

    steps_astar = len(bs.moveLog)
    cost_astar = bs.getScore()
    steps_dijkstra = len(bs.moveLog2)
    cost_dijkstra = sum(bs.board_difficulty[r][c] for r, c in bs.moveLog2)

    screen.blit(font.render(f"A* steps: {steps_astar}", True, (200, 0, 0)), (padding, result_y + 30))
    screen.blit(font.render(f"A* cost: {cost_astar}", True, (200, 0, 0)), (padding, result_y + 55))
    screen.blit(font.render(f"Dijkstra steps: {steps_dijkstra}", True, (0, 0, 200)), (padding, result_y + 90))
    screen.blit(font.render(f"Dijkstra cost: {cost_dijkstra}", True, (0, 0, 200)), (padding, result_y + 115))

if __name__ == "__main__":
    main()
