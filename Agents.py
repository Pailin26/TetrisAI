import random
import tetris_ai

MUTATION_RATE = 0.5


class GeneticAgent():
    pop = []
    def __init__(self):
        self.weight_holes = random.random()
        self.weight_bumpiness = random.random()
        self.weight_line_clear = random.random()
        self.weight_height = random.random()
            
    
    def get_score(self, game_height, game_width, game_field, gen):
        score = -(self.pop[gen][0] * tetris_ai.get_hole(game_height, game_width, game_field)) 
        + -(self.pop[gen][1] * tetris_ai.get_bumpiness(game_height, game_width, game_field)) 
        + (self.pop[gen][2] * tetris_ai.get_line_clear(game_height, game_width, game_field)) 
        + -(self.pop[gen][3] * tetris_ai.sum_col_height(game_width, game_height, game_field))
        return score

    def mutation(self, max_gen, pop):
        for i in range(1, max_gen):
            if random.random() < MUTATION_RATE:
                pop[i][0] = random.random()
            if random.random() < MUTATION_RATE:
                pop[i][1] = random.random()
            if random.random() < MUTATION_RATE:
                pop[i][2] = random.random()
            if random.random() < MUTATION_RATE:
                pop[i][3] = random.random()
        return pop
    
    def get_pop(self, max_gen):
        for i in range(max_gen):
            self.weight_holes = random.random()
            self.weight_bumpiness = random.random()
            self.weight_line_clear = random.random()
            self.weight_height = random.random()
            self.weight = [self.weight_holes, self.weight_bumpiness, self.weight_line_clear, self.weight_height]
            self.pop.append(self.weight)
        print(self.pop)
