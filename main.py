import pygame, pathlib, time, threading, random, shapes
from itertools import groupby

GAMEOVER = False

WIDTH = 400
HEIGHT = 600

pygame.init()

path = pathlib.Path(__file__).resolve().parent
font = str(path) + "/lib/font.ttf"

shapes_list = [shapes.S, shapes.Z, shapes.I, shapes.O, shapes.J, shapes.T]
shapes_to_draw = []

grid = 20
black = pygame.Color(0, 0, 0)
grey = pygame.Color(50, 50, 50)
light_grey = pygame.Color(190, 190, 190)
blue = pygame.Color(0, 0, 255)

clock = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

class Piece:
    def __init__(self, shape):
        self.x = grid
        self.y = 0
        self.shape = shape
        self.rotation = 0
        self.locked_position = []
        self.locked = False
    
    def show(self):
        x = 0
        y = 0

        for row in self.shape[self.rotation % len(self.shape)]:
            for col in row:
                if col == "0" and self.y+y >= HEIGHT-(6*grid):
                    self.locked_position.extend((self.x, self.y))
                    self.locked = True
                
                x_pos = self.x if len(self.locked_position) == 0 else self.locked_position[0]
                y_pos = self.y if len(self.locked_position) == 0 else self.locked_position[1]

                if col == "0":
                    pygame.draw.rect(display, blue, (x_pos+x, y_pos+y, grid, grid))
                x += grid
            x = 0
            y += grid

def move_piece():
    while not GAMEOVER:
        time.sleep(1)
        piece.y += grid

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def draw_grid(surface, spacebtwn, color):
    for x in range(1, int(HEIGHT/spacebtwn)):
        pygame.draw.line(surface, color, (0, x*grid), (WIDTH, x*grid))
    for y in range(1, int(WIDTH/spacebtwn)):
        pygame.draw.line(surface, color, (y*grid, 0), (y*grid, HEIGHT))

def draw_borders(surface, color):
    pygame.draw.rect(surface, color, (0, HEIGHT-(5*grid), WIDTH, 5*grid))
    pygame.draw.rect(surface, color, (0, 0, grid, HEIGHT))
    pygame.draw.rect(surface, color, (WIDTH-grid, 0, grid, HEIGHT))

def show_fps(surface, font_size, color, xy):
    fps_font = pygame.font.Font(font, font_size)
    fps = fps_font.render(str(int(clock.get_fps())), True, color)
    surface.blit(fps, (xy[0], xy[1]))

threading.Thread(target = move_piece).start()

piece = Piece(random.choice(shapes_list))
shapes_to_draw.append(piece)

while not GAMEOVER:
    display.fill(black)

    for shape in shapes_to_draw:
        shape.show()

    if all_equal(shape.locked for shape in shapes_to_draw):
        if len(shapes_to_draw) == 1 and shapes_to_draw[0].locked or len(shapes_to_draw) > 1:
            piece = Piece(random.choice(shapes_list))
            shapes_to_draw.append(piece)

    draw_grid(display, grid, grey)
    draw_borders(display, light_grey)
    show_fps(display, 15, black, (2, 2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEOVER = True
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            #! grid = one block
            
            for shape in shapes_to_draw:
                if shape.locked == False:
                    # Rotate
                    if event.key == pygame.K_UP:
                        if len(piece.locked_position) == 0:
                            shape.rotation += 1
                    
                    # Move
                    if event.key == pygame.K_RIGHT:
                        shape.x += grid
                    if event.key == pygame.K_LEFT:
                        shape.x -= grid
                    if event.key == pygame.K_DOWN:
                        shape.y += grid

    pygame.display.update()
    clock.tick(60)