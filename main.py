import pygame, pathlib, time, threading, random, shapes
from itertools import groupby

GAMEOVER = False

WIDTH = 400
HEIGHT = 600

pygame.init()

path = pathlib.Path(__file__).resolve().parent
font = str(path) + "/lib/font.ttf"

grid = 20
black = pygame.Color(0, 0, 0)
grey = pygame.Color(50, 50, 50)
light_grey = pygame.Color(190, 190, 190)
blue = pygame.Color(0, 0, 255)

clock = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

shapes_list = [shapes.S, shapes.Z, shapes.I, shapes.O, shapes.J, shapes.T]
colors_list = [pygame.Color(3, 65, 174), pygame.Color(114, 203, 59), pygame.Color(255, 213, 0), pygame.Color(255, 151, 28), pygame.Color(255, 50, 19)]
locked_shapes = []

class Piece:
    def __init__(self, shape, color):
        self.x = grid
        self.y = 0
        self.shape = shape
        self.rotation = 0
        self.color = color
        self.collision = False
    
    def show(self):
        x = 0
        y = 0
        for row in self.shape[self.rotation % len(self.shape)]:
            for col in row:
                if col == "0" and self.y+y == HEIGHT-(6*grid):
                    self.collision = True
                if col == "0":
                    pygame.draw.rect(display, self.color, (self.x+x, self.y+y, grid, grid))
                x += grid
            x = 0
            y += grid
            
        for _ in locked_shapes:
            lckd_x = 0
            lckd_y = 0
            locked_shape = _.shape[_.rotation % len(_.shape)]
            for lckd_row in locked_shape:
                for lckd_col in lckd_row:
                    if lckd_col == "0":
                        pygame.draw.rect(display, _.color, (_.x+lckd_x, _.y+lckd_y, grid, grid))
                    lckd_x += grid
                lckd_x = 0
                lckd_y += grid

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

piece = Piece(random.choice(shapes_list), random.choice(colors_list))

while not GAMEOVER:
    display.fill(black)

    piece.show()

    if piece.collision:
        locked_shapes.append(piece)
        piece = Piece(random.choice(shapes_list), random.choice(colors_list))

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
            
            # Rotate
            if event.key == pygame.K_UP:
                piece.rotation += 1
            
            # Move
            if event.key == pygame.K_RIGHT:
                piece.x += grid
            if event.key == pygame.K_LEFT:
                piece.x -= grid
            if event.key == pygame.K_DOWN:
                piece.y += grid

    pygame.display.update()
    clock.tick(90)