import pygame
from copy import deepcopy
import Agents

e = []
agent = Agents.GeneticAgent()

class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key


counter = 0

def intersects(game_field, x, y, game_width, game_height, game_figure_image):
    intersection = False
    for i in range(4):
        for j in range(4):
            if i * 4 + j in game_figure_image:
                if i + y > game_height - 1 or \
                        j + x > game_width - 1 or \
                        j + x < 0 or \
                        game_field[i + y][j + x] > 0:
                    intersection = True
    return intersection



def get_hole(game_height, game_width, game_field):
        hole = 0
        for j in range(game_width):
            h = (game_height - col_height(game_height, j, game_field))
            for i in range(h, game_height):
                if game_field[i][j] == 0:
                    hole += 1
        return hole

def col_height(game_height, row, game_field):
        x = 0
        for i in range(game_height):
            if game_field[i][row] == 0:   
                x += 1
            if game_field[i][row] != 0:
                break   
        height = game_height - x       
        return height

def sum_col_height(game_width, game_height, game_field):
        sum_height = 0
        for j in range(game_width):
            x = 0
            for i in range(game_height):
                if game_field[i][j] == 0:   
                    x += 1
                if game_field[i][j] != 0:
                    break   
            sum_height += game_height - x     
        return sum_height

def get_bumpiness(game_height, game_width, game_field):
    bumpiness = 0
    for j in range(game_width-1):
        bumpiness += abs(col_height(game_height, j, game_field) - col_height(game_height, j+1, game_field)) 
    return bumpiness

def get_line_clear(game_height, game_width, game_field):
    line_clear = 0
    for i in range(1, game_height):
        zeros = 0
        for j in range(game_width):
            if game_field[i][j] == 0:
                zeros += 1
        if zeros == 0:
            line_clear += 1
    return line_clear
                

def future_board(game_field, game_figure_x, game_figure_y, game_width, game_height, fig, gen):
    while not intersects(game_field, game_figure_x, game_figure_y, game_width, game_height, fig):
        game_figure_y += 1
    game_figure_y -= 1
    board = deepcopy(game_field)
    for i in range(game_height-1, -1, -1):
        for j in range(game_width):
            for ii in range(4):
                        for jj in range(4):
                            if ii * 4 + jj in fig:
                                if jj + game_figure_x == j and ii + game_figure_y == i:
                                    board[i][j] = 1
    score = agent.get_score(game_height, game_width, board, gen)
    return score

def decision(game_figure, x, bestrotation):
    if game_figure.rotation != bestrotation:
        e = Event(pygame.KEYDOWN, pygame.K_UP)
    elif game_figure.x > x:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    elif game_figure.x < x:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    else :
        e = Event(pygame.KEYDOWN, pygame.K_SPACE)
    return [e]

def update_pop(agent_score, pop, max_gen):
        print(agent_score)
        print(pop)
        zipped = zip(agent_score, pop)
        x = sorted(zipped, reverse=True)
        tuples = zip(*x)
        agent_score, pop = [list(tuple) for tuple in  tuples]
        print(agent_score)
        print(pop)
        best = agent_score[0]
        pop = agent.mutation(max_gen, pop)
        return pop, best




    

        



