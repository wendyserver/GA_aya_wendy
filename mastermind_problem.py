"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import GAProblem, Individual
import mastermind as mm
import random


class MastermindProblem(GAProblem):
    """GAProblem Implementation for the Mastermind Problem"""
    
    def __init__(self, secret_size=4, target_fitness=None):
        """Initializes the Mastermind problem

            Args:
            secret_size (int): secret code size
            target_fitness (float): target fitness (if None, use the maximum possible value))
        """
        self.secret_size = secret_size
        self.match = mm.MastermindMatch(secret_size=secret_size)
        self.valid_colors = mm.get_possible_colors()
        
        
        if target_fitness is None:
            self.target_fitness = self.match.max_score()
        else:
            self.target_fitness = target_fitness
    
    def create_individual(self):
        """Creates an individual with a random combination of colors"""
        
        chromosome = [random.choice(self.valid_colors) for _ in range(self.secret_size)]
        
        
        fitness = self.match.rate_guess(chromosome)
        
        return Individual(chromosome, fitness)
    
    def select_parents(self, population):
        """Selects two parents for breeding"""
        return random.sample(population, 2)
    
    def crossover(self, parents):
        """Cross two parents to create a child"""
        parent_a, parent_b = parents[0].chromosome, parents[1].chromosome
        
        
        x_point = random.randint(1, self.secret_size - 1)
        
        # Creation of newchild by crossing 
        new_chrom = parent_a[:x_point] + parent_b[x_point:]
        
        # Calcululation of fitness
        fitness = self.match.rate_guess(new_chrom)
        
        return Individual(new_chrom, fitness)
    
    def mutate(self, individual, mutation_rate):
        """Applies a mutation by changing a random color with a certain probability"""
        if random.random() >= mutation_rate:
            return individual  # no mutation
        
        # Copy of  chromosome
        mutated_chrom = individual.chromosome.copy()
        
        # Selection of a random  position 
        pos = random.randint(0, self.secret_size - 1)
        
        # Changing color
        mutated_chrom[pos] = random.choice(self.valid_colors)
        
        # Calculation of the new fitness
        fitness = self.match.rate_guess(mutated_chrom)
        
        return Individual(mutated_chrom, fitness)
    
    def is_solution_found(self, best_individual, generation):
        """Determines whether a satisfactory solution has been found"""
        
        if self.match.is_correct(best_individual.chromosome):
            return True
        
        return best_individual.fitness >= self.target_fitness


if __name__ == '__main__':
    from ga_solver import GASolver
    
    # Creation of the problem with secret size
    problem = MastermindProblem(secret_size=6)
    match = problem.match
    solver = GASolver(problem)
    
    solver.reset_population()
    solver.evolve_until()
    
    best_individual = solver.get_best_individual()
    print(f"Best guess {best_individual.chromosome} with fitness {best_individual.fitness}")
    print(f"Problem solved? {match.is_correct(best_individual.chromosome)}")