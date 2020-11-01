import pygame, pathlib, threading

WIDTH = 400
HEIGHT = 600

pygame.init()

path = pathlib.Path(__file__).resolve().parent
font = str(path) + "/lib/font.ttf"

grid = 20
black = pygame.Color(0, 0, 0)
grey = pygame.Color(50, 50, 50)
light_grey = pygame.Color(190, 190, 190)

clock = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

def draw_grid(surface, spacebtwn, color):
    for x in range(1, int(HEIGHT/spacebtwn)):
        pygame.draw.line(surface, color, (0, x*grid), (WIDTH, x*grid))
    for y in range(1, int(WIDTH/spacebtwn)):
        pygame.draw.line(surface, color, (y*grid, 0), (y*grid, HEIGHT))

def draw_borders(surface, color):
    pygame.draw.rect(display, color, (0, HEIGHT-(5*grid), WIDTH, 5*grid))
    pygame.draw.rect(display, color, (0, 0, grid, HEIGHT))
    pygame.draw.rect(display, color, (WIDTH-grid, 0, grid, HEIGHT))

def show_fps(surface, font_size, color, xy):
    fps_font = pygame.font.Font(font, font_size)
    fps = fps_font.render(str(int(clock.get_fps())), True, color)
    surface.blit(fps, (xy[0], xy[1]))

while True:
    display.fill(pygame.Color(black))
    
    draw_grid(display, grid, grey)
    draw_borders(display, light_grey)
    show_fps(display, 15, black, (2, 2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)