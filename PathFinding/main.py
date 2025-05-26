import pygame as p
from PathFinding import engine

# Config
SIDEBAR_WIDTH = 250
SQR_SIZE = 4
DIMENSIONS = 200
FINAL_ZOOM = 0.90
map_pixel_size = DIMENSIONS * SQR_SIZE * FINAL_ZOOM
WIDTH = SIDEBAR_WIDTH + int(DIMENSIONS * SQR_SIZE * FINAL_ZOOM)
HEIGHT = int(map_pixel_size)
INITIAL_ZOOM = WIDTH / DIMENSIONS
FPS = 60
IMAGES = {}

def loadImages():
    textures = ['grass', 'mud', 'rocks', 'sand']
    for texture in textures:
        IMAGES[texture] = p.image.load("img/" + texture + ".png")
    IMAGES["player"] = p.image.load("img/player.png")
    IMAGES["player2"] = p.image.load("img/player2.png")
    IMAGES["end"] = p.image.load("img/end.png")

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    p.display.set_caption("A* vs Dijkstra - 200x200")

    bs = engine.BoardState()
    loadImages()

    start_button = p.Rect(30, HEIGHT - 120, 190, 40)
    restart_button = p.Rect(30, HEIGHT - 70, 190, 40)
    started = False
    
    # Ustawienia zoomowania
    zoom = FINAL_ZOOM
    follow = False

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if start_button.collidepoint(e.pos) and not started:
                    bs.start_pathfinding()
                    started = True
                    follow = True
                elif restart_button.collidepoint(e.pos):
                    bs = engine.BoardState()
                    started = False
                    zoom = FINAL_ZOOM
                    follow = False

        if started and (bs.playerPos != bs.end or bs.playerPos2 != bs.end):
            bs.stepTowardsEnd()
            bs.stepTowardsEnd2()
        elif started and bs.playerPos == bs.end and bs.playerPos2 == bs.end:
            zoom = FINAL_ZOOM
            follow = False

        # Determine camera offset
        if started and follow and (bs.playerPos != bs.end or bs.playerPos2 != bs.end):
            avg_x = (bs.playerPos[1] + bs.playerPos2[1]) // 2
            avg_y = (bs.playerPos[0] + bs.playerPos2[0]) // 2
            zoom = INITIAL_ZOOM
        else:
            avg_x = DIMENSIONS // 2
            avg_y = DIMENSIONS // 2
            zoom = FINAL_ZOOM

        offset_x = (avg_x * SQR_SIZE * zoom) - (WIDTH - SIDEBAR_WIDTH) // 2
        offset_y = avg_y * SQR_SIZE * zoom - HEIGHT // 2

        screen.fill((0, 0, 0))
        drawBoard(screen, bs, offset_x, offset_y, zoom)
        drawUsed(screen, bs, offset_x, offset_y, zoom)
        drawPlayer(screen, bs, offset_x, offset_y, zoom)
        drawPlayer2(screen, bs, offset_x, offset_y, zoom)
        drawEnd(screen, bs, offset_x, offset_y, zoom)
        drawSidebar(screen, bs, start_button, restart_button, started)

        p.display.flip()
        clock.tick(FPS)

def drawBoard(screen, bs, offset_x, offset_y, zoom):
    sqr_size_scaled = int(SQR_SIZE * zoom) + 1  # +1 piksel nakładania
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            texture = bs.board[r][c]
            img = p.transform.scale(IMAGES[texture], (sqr_size_scaled, sqr_size_scaled))
            x = int(c * SQR_SIZE * zoom + SIDEBAR_WIDTH - offset_x)
            y = int(r * SQR_SIZE * zoom - offset_y)
            screen.blit(img, (x, y))

def drawUsed(screen, bs, offset_x, offset_y, zoom):
    alpha_a = p.Surface((int(SQR_SIZE * zoom), int(SQR_SIZE * zoom)), p.SRCALPHA)
    alpha_a.fill((200, 0, 0, 100))
    alpha_d = p.Surface((int(SQR_SIZE * zoom), int(SQR_SIZE * zoom)), p.SRCALPHA)
    alpha_d.fill((0, 0, 200, 100))

    for r, c in bs.moveLog:
        x = int(c * SQR_SIZE * zoom + SIDEBAR_WIDTH - offset_x)
        y = int(r * SQR_SIZE * zoom - offset_y)
        screen.blit(alpha_a, (x, y))
    for r, c in bs.moveLog2:
        x = int(c * SQR_SIZE * zoom + SIDEBAR_WIDTH - offset_x)
        y = int(r * SQR_SIZE * zoom - offset_y)
        screen.blit(alpha_d, (x, y))

def drawPlayer(screen, bs, offset_x, offset_y, zoom):
    r, c = bs.playerPos
    img = p.transform.scale(IMAGES["player"], (int(SQR_SIZE * zoom), int(SQR_SIZE * zoom)))
    x = int(c * SQR_SIZE * zoom + SIDEBAR_WIDTH - offset_x)
    y = int(r * SQR_SIZE * zoom - offset_y)
    screen.blit(img, (x, y))

def drawPlayer2(screen, bs, offset_x, offset_y, zoom):
    r, c = bs.playerPos2
    img = p.transform.scale(IMAGES["player2"], (int(SQR_SIZE * zoom), int(SQR_SIZE * zoom)))
    x = int(c * SQR_SIZE * zoom + SIDEBAR_WIDTH - offset_x)
    y = int(r * SQR_SIZE * zoom - offset_y)
    screen.blit(img, (x, y))

def drawEnd(screen, bs, offset_x, offset_y, zoom):
    r, c = bs.end
    img = p.transform.scale(IMAGES["end"], (int(SQR_SIZE * zoom), int(SQR_SIZE * zoom)))
    x = int(c * SQR_SIZE * zoom + SIDEBAR_WIDTH - offset_x)
    y = int(r * SQR_SIZE * zoom - offset_y)
    screen.blit(img, (x, y))

def drawSidebar(screen, bs, start_button, restart_button, started):
    padding = 10
    font = p.font.SysFont("arial", 16)
    bold_font = p.font.SysFont("arial", 18, bold=True)
    header_font = p.font.SysFont("arial", 20, bold=True)

    sidebar_rect = p.Rect(0, 0, SIDEBAR_WIDTH, HEIGHT)
    p.draw.rect(screen, (240, 240, 240), sidebar_rect)

    title = header_font.render("Terrain Difficulty", True, (0, 0, 0))
    screen.blit(title, (padding, padding))

    textures = ["grass", "sand", "mud", "rocks"]
    difficulties = [1, 2, 3, 4]
    texture_images = [p.image.load(f"img/{name}.png") for name in textures]
    texture_images = [p.transform.scale(img, (30, 30)) for img in texture_images]

    for i, (img, name, diff) in enumerate(zip(texture_images, textures, difficulties)):
        y = 45 + i * 40
        screen.blit(img, (padding, y))
        screen.blit(font.render(name.capitalize(), True, (0, 0, 0)), (padding + 40, y))
        screen.blit(font.render(f"Diff: {diff}", True, (100, 100, 100)), (padding + 40, y + 20))

    result_y = 230
    p.draw.line(screen, (0, 0, 0), (padding, result_y - 10), (SIDEBAR_WIDTH - padding, result_y - 10), 2)
    screen.blit(header_font.render("Results", True, (0, 0, 0)), (padding, result_y))

    if bs.started:
        # Statystyki A* (czerwone)
        astar_y = result_y + 35
        screen.blit(bold_font.render("A* Algorithm:", True, (150, 0, 0)), (padding, astar_y))
        screen.blit(font.render(f"Steps: {len(bs.moveLog)}", True, (200, 0, 0)), (padding + 10, astar_y + 25))
        screen.blit(font.render(f"Path cost: {bs.getScore()}", True, (200, 0, 0)), (padding + 10, astar_y + 45))
        
        
        # Tekstury dla A* - w dwóch wierszach
        texture_y = astar_y + 65
        screen.blit(font.render("Terrain usage:", True, (150, 0, 0)), (padding + 10, texture_y))
        
        # Pierwszy wiersz: grass i sand
        row1_y = texture_y + 20
        grass_count = bs.texture_count[1]
        sand_count = bs.texture_count[2]
        screen.blit(font.render(f"grass: {grass_count}", True, (200, 0, 0)), (padding + 15, row1_y))
        screen.blit(font.render(f"sand: {sand_count}", True, (200, 0, 0)), (padding + 90, row1_y))
        
        # Drugi wiersz: mud i rocks
        row2_y = texture_y + 38
        mud_count = bs.texture_count[3]
        rocks_count = bs.texture_count[4]
        screen.blit(font.render(f"mud: {mud_count}", True, (200, 0, 0)), (padding + 15, row2_y))
        screen.blit(font.render(f"rocks: {rocks_count}", True, (200, 0, 0)), (padding + 90, row2_y))

        screen.blit(font.render(f"Time: {bs.astar_time:.4f}s", True, (200, 0, 0)), (padding + 10, astar_y + 120))

        # Odstęp między algorytmami
        dijkstra_y = astar_y + 160  # 120 (ostatni element) + 40 odstępu

        # Statystyki Dijkstra (niebieskie)
        screen.blit(bold_font.render("Dijkstra Algorithm:", True, (0, 0, 150)), (padding, dijkstra_y))
        screen.blit(font.render(f"Steps: {len(bs.moveLog2)}", True, (0, 0, 200)), (padding + 10, dijkstra_y + 25))
        cost_dijkstra = sum(bs.board_difficulty[r][c] for r, c in bs.moveLog2)
        screen.blit(font.render(f"Path cost: {cost_dijkstra}", True, (0, 0, 200)), (padding + 10, dijkstra_y + 45))
        
        # Tekstury dla Dijkstra - w dwóch wierszach
        texture2_y = dijkstra_y + 65
        screen.blit(font.render("Terrain usage:", True, (0, 0, 150)), (padding + 10, texture2_y))
        
        # Pierwszy wiersz: grass i sand
        row1_y_d = texture2_y + 20
        grass_count2 = bs.texture_count2[1]
        sand_count2 = bs.texture_count2[2]
        screen.blit(font.render(f"grass: {grass_count2}", True, (0, 0, 200)), (padding + 15, row1_y_d))
        screen.blit(font.render(f"sand: {sand_count2}", True, (0, 0, 200)), (padding + 90, row1_y_d))
        
        # Drugi wiersz: mud i rocks
        row2_y_d = texture2_y + 38
        mud_count2 = bs.texture_count2[3]
        rocks_count2 = bs.texture_count2[4]
        screen.blit(font.render(f"mud: {mud_count2}", True, (0, 0, 200)), (padding + 15, row2_y_d))
        screen.blit(font.render(f"rocks: {rocks_count2}", True, (0, 0, 200)), (padding + 90, row2_y_d))
        
        screen.blit(font.render(f"Time: {bs.dijkstra_time:.4f}s", True, (0, 0, 200)), (padding + 10, dijkstra_y + 120))


    # Przyciski
    start_button.y = HEIGHT - 120
    restart_button.y = HEIGHT - 70

    # Draw start button
    button_color = (180, 255, 180) if not started else (180, 180, 180)
    p.draw.rect(screen, button_color, start_button, border_radius=6)
    if not started:
        btn_label = "Start"
    elif bs.playerPos == bs.end and bs.playerPos2 == bs.end:
        btn_label = "Done"
    else:
        btn_label = "Running..."
    screen.blit(bold_font.render(btn_label, True, (0, 0, 0)), (start_button.x + 15, start_button.y + 10))

    # Draw restart button
    restart_color = (255, 200, 200)
    p.draw.rect(screen, restart_color, restart_button, border_radius=6)
    screen.blit(bold_font.render("Restart", True, (0, 0, 0)), (restart_button.x + 15, restart_button.y + 10))

if __name__ == "__main__":
    main()