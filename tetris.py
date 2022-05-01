from cv2 import rotate
import pygame
import random
import tetris_ai
import Agents

max_pop = 5
agent = Agents.GeneticAgent()
agent.get_pop(max_pop)

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    gen = 1
    pop = 0
    pop_score = []
    best = 0

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.pop += 1
        if self.pop > max_pop:
            agent.pop, self.best = tetris_ai.update_pop(self.pop_score, agent.pop, max_pop)
            print(agent.pop)
            self.pop = 1
            self.pop_score = []
            self.gen += 1
        print('Gen:',self.gen)    
        print("Pop:",self.pop)
        print(agent.pop[self.pop-1][0])
        print(agent.pop[self.pop-1][1])
        print(agent.pop[self.pop-1][2])
        print(agent.pop[self.pop-1][3])
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)


    def new_figure(self):
        self.figure = Figure(3, 0)
        

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.pop_score.append(self.score)
            self.state = "gameover"
            print(self.score)
            game. __init__(20, 10)
    
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (550, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")


done = True
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

pause = False

while done:
    if game.best > 100:
        done = False
    score = 0
    bestscore = -99999
    bestx = 0
    if game.figure is None:
        game.new_figure()
    counter += 1

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()   
            
    for rotation in range(len(game.figure.figures[game.figure.type])):
        fig = game.figure.figures[game.figure.type][rotation]     
        for x in range(-1, game.width-2):             
            score = (tetris_ai.future_board(game.field, x, game.figure.y, game.width, game.height, fig, game.pop-1))
            if bestscore < score:
                bestscore = score
                bestx = x
                bestrotation = rotation
    # for event in pygame.event.get():
    for event in list(pygame.event.get()) + tetris_ai.decision(game.figure, bestx, bestrotation):
        if event.type == pygame.QUIT:
            done = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE: #restart
                game.__init__(20, 10)
            
    if event.type == pygame.KEYUP: #lift key
            if event.key == pygame.K_DOWN:
                pressing_down = False
            

    screen.fill(WHITE)

    for i in range(game.height): #draw grid
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0: #draw color
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None: # draw block falling down
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    font2 = pygame.font.SysFont('Calibri', 20, True, False)
    font3 = pygame.font.SysFont('Calibri', 13, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_gen = font2.render("Gen: " + str(game.gen), True, BLACK)
    text_pop = font2.render("Pop: " + str(game.pop), True, BLACK)
    text_weight_hole = font3.render("Weight holes: " + str(agent.pop[game.pop-1][0]), True, BLACK)
    text_weight_bumpiness = font3.render("Weight bumpiness: " + str(agent.pop[game.pop-1][1]), True, BLACK)
    text_weight_line_clear = font3.render("Weight line clear: " + str(agent.pop[game.pop-1][2]), True, BLACK)
    text_weight_height = font3.render("Weight height: " + str(agent.pop[game.pop-1][3]), True, BLACK)
    text_best_score = font.render("Best Score: " + str(game.best), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    screen.blit(text_gen, [310, 100])
    screen.blit(text_pop, [310, 120])
    screen.blit(text_weight_hole, [310, 150])
    screen.blit(text_weight_bumpiness, [310, 170])
    screen.blit(text_weight_line_clear, [310, 190])
    screen.blit(text_weight_height, [310, 210])
    screen.blit(text_best_score, [350, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()