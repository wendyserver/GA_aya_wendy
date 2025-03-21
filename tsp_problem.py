# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem, Individual
import cities
import random

class TSProblem(GAProblem):
    """Implémentation of GAProblem (TSP)"""
    
    def __init__(self, city_dict, num_cities=12, target_fitness=None, max_generations=1000):
        """Initializes the TSP problem

            Args:
            city_dict (dict): Dictionary of cities with their coordinates
            num_cities (int): Number of cities to visit
            target_fitness (float, optional): Target fitness to stop the algorithm
            max_generations (int): Maximum number of generations
        """
        self.city_dict = city_dict
        self.num_cities = num_cities
        self.possible_cities = cities.default_road(city_dict)
        self.target_fitness = target_fitness
        self.max_generations = max_generations
    
    def create_individual(self):
        """Creation of an  individu with random road """
        # Génération d'un chemin aléatoire (permutation de villes)
        chromosome = random.sample(self.possible_cities, self.num_cities)
        
        # Calcul de la fitness (négatif de la longueur du chemin)
        fitness = -cities.road_length(self.city_dict, chromosome)
        
        return Individual(chromosome, fitness)
    
    def select_parents(self, population):
        """Select two  parents for the reproduction"""
        return random.sample(population, 2)
    
    def crossover(self, parents):
        """Crossing of two parents to create a child
        
        Uses order-preserving crossover to maintain a valid path
        """
        parent_a, parent_b = parents[0].chromosome, parents[1].chromosome
        
        # Croissing of ordered road 
        cutpoint = len(parent_a) // 2
        child_chrom = parent_a[:cutpoint]
        
        # Add  parent_b' s cities that are not yet in  child
        for city in parent_b:
            if city not in child_chrom:
                child_chrom.append(city)
        
        # Vérify if all the cities are present 
        if len(child_chrom) < self.num_cities:
            for city in self.possible_cities:
                if city not in child_chrom:
                    child_chrom.append(city)
                    if len(child_chrom) == self.num_cities:
                        break
        
        # Calculation of  fitness
        fitness = -cities.road_length(self.city_dict, child_chrom)
        
        return Individual(child_chrom, fitness)
    
    def mutate(self, individual, mutation_rate):
        """Applies a mutation by swapping two cities with a certain probability"""
        if random.random() >= mutation_rate:
            return individual  # no mutation
        
        # Copie du chromosome
        mutated_chrom = individual.chromosome.copy()
        
        # Selection of two random positions 
        pos1 = random.randint(0, self.num_cities - 1)
        pos2 = random.randint(0, self.num_cities - 1)
        
        # exchange of the two cities 
        mutated_chrom[pos1], mutated_chrom[pos2] = mutated_chrom[pos2], mutated_chrom[pos1]
        
        # Calculate the new fitness
        fitness = -cities.road_length(self.city_dict, mutated_chrom)
        
        return Individual(mutated_chrom, fitness)
    
    def is_solution_found(self, best_individual, generation):
        """Détermine si une solution satisfaisante a été trouvée"""
        # if the target fitness  is spécified, vérify if she is reached
        if self.target_fitness is not None and best_individual.fitness >= self.target_fitness:
            return True
        
        # continue until the maximum of génération is reached
        return False

if __name__ == '__main__':

    from ga_solver import GASolver

    city_dict = cities.load_cities("cities.txt")
    problem = TSProblem(city_dict)
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until()
    cities.draw_cities(city_dict, solver.get_best_individual().chromosome)
