import pygame, pathlib, threading, random, shapes
from itertools import groupby

GAMEOVER = False

WIDTH = 360
HEIGHT = 600

pygame.init()

path = pathlib.Path(__file__).resolve().parent
font = str(path) + "/lib/font.ttf"
background = pygame.image.load(str(path) + "/lib/background.jpg")

SCORE = 0

grid = 20
black = pygame.Color(0, 0, 0)
# grey = pygame.Color(50, 50, 50)
grey = pygame.Color(200, 200, 200)
light_grey = pygame.Color(190, 190, 190)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(255, 255, 255)

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
        
        self.next_piece = [random.choice(shapes_list), random.choice(colors_list)]
    
    def show(self):
        x = 0
        y = 0
        for row in self.shape[self.rotation % len(self.shape)]:
            for col in row:
                if col == "0":
                    if self.y+y == HEIGHT-(8*grid):
                        self.collision = True
                    pygame.draw.rect(display, self.color, (self.x+x, self.y+y, grid, grid))
                    
                for _ in locked_shapes:
                    lckd_x = 0
                    lckd_y = 0
                    locked_shape = _.shape[_.rotation % len(_.shape)]
                    for lckd_row in locked_shape:
                        for lckd_col in lckd_row:
                            if lckd_col == "0":
                                if col == "0" and (_.x+lckd_x) == self.x+x and (_.y+lckd_y)-grid == self.y+y:
                                    self.collision = True
                                pygame.draw.rect(display, _.color, (_.x+lckd_x, _.y+lckd_y, grid, grid))
                            lckd_x += grid
                        lckd_x = 0
                        lckd_y += grid
                x += grid
            x = 0
            y += grid
    
    def move(self, x_dir, y_dir):
        self.y += y_dir*grid
        self.x += x_dir*grid

def move_piece():
    while not GAMEOVER:
        pygame.time.wait(1000)
        piece.move(0, 1)

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
    
def draw_scoreboard(surface, color):
    pygame.draw.rect(surface, color, (grid, HEIGHT-(6*grid), WIDTH-(grid*8), HEIGHT-(HEIGHT-(5*grid))), border_radius = 5)

def draw_gameboard(surface, color):
    display.blit(background, (0, 0))
    pygame.draw.rect(display, black, (grid, 0, WIDTH-(grid*2), HEIGHT-(7*grid)))

def show_next_piece(surface):
    x = 0
    y = 0

    pygame.draw.rect(surface, grey, (WIDTH-(grid*len(piece.next_piece[0][0])+grid), HEIGHT-(6*grid), WIDTH-(WIDTH-(grid*len(piece.next_piece[0][0])+grid)+grid), HEIGHT-(HEIGHT-grid*5)), border_radius=5)
    for row in piece.next_piece[0][0]:
        for col in row:
            if col == "0":
                pygame.draw.rect(surface, piece.next_piece[1], (WIDTH-(grid*len(row)+grid)+x, HEIGHT-(6*grid)+y, grid, grid))
            x += grid
        x = 0
        y += grid
        

def show_score(surface, color, font, font_size):
    score_font = pygame.font.Font(font, font_size)
    score = score_font.render("Score: " + str(SCORE), True, color)
    surface.blit(score, (grid*1.5, HEIGHT-(5.8*grid)))

def show_fps(surface, font_size, color, xy):
    fps_font = pygame.font.Font(font, font_size)
    fps = fps_font.render(str(int(clock.get_fps())), True, color)
    surface.blit(fps, (xy[0], xy[1]))

threading.Thread(target = move_piece).start()

piece = Piece(random.choice(shapes_list), random.choice(colors_list))

while not GAMEOVER:
    draw_gameboard(display, black)
    # draw_grid(display, grid, grey)
    # draw_borders(display, light_grey)
    
    piece.show()

    if piece.collision:
        locked_shapes.append(piece)
        piece = Piece(piece.next_piece[0], piece.next_piece[1])
    
    # Scoreboard
    draw_scoreboard(display, grey)
    show_score(display, black, font, 17)

    # show_fps(display, 15, black, (2, 2))
    show_next_piece(display)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEOVER = True
        
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                GAMEOVER = True
                       
            # Rotate
            if event.key == pygame.K_UP:
                piece.rotation += 1
            
            # Move
            if event.key == pygame.K_RIGHT:
                piece.move(1, 0)
            if event.key == pygame.K_LEFT:
                piece.move(-1, 0)
            if event.key == pygame.K_DOWN:
                piece.move(0, 1)

    pygame.display.update()
    clock.tick(60)


pygame.quit()
exit()