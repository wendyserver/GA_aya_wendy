# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(generic genetic algorithm module)
"""
from abc import ABC, abstractmethod
import random

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome (list[]): a list representing the individual's
            chromosome
            fitness (float): the individual's fitness (the higher the value,
            the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GAProblem:
    """Abstract interface defining the operations needed to solve a problem with a genetic algorithm"""
    @abstractmethod
    def create_individual(self):
        """Creates a valid random individual for the problem.

            Returns:
            Individual: A new individual with a random chromosome and its fitness.
            """
        pass
    
    @abstractmethod
    def select_parents(self, population):
        """Selects parents for reproduction from the population.

            Args:
            population (list): List of individuals from which to choose parents.

            Returns:
            list: The selected parents.
            """
        pass
    
    @abstractmethod
    def crossover(self, parents):
        """Performs a cross between parents to create a new individual.

            Args:
            parents (list): List of parent individuals.

            Returns:
            Individual: The new individual created by the cross.
        """
        pass
    
    @abstractmethod
    def mutate(self, individual, mutation_rate):
        """Applies a mutation to an individual with a certain probability.

            Args:
            individual: The individual to potentially mutate.
            mutation_rate (float): Probability of mutation.

            Returns:
            Individual: The individual after mutation (or the original if no mutation).
        """
        pass
    
    @abstractmethod
    def is_solution_found(self, best_individual, generation):
        """Determines if a satisfactory solution has been found.

            Args:
            best_individual (Individual): The best individual of the current generation.
            generation (int): The number of the current generation.

            Returns:
            bool: True if the search can stop, False otherwise.
        """
        pass



class GASolver:
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1,pop_size=50):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            problem (GAProblem): GAProblem to be solved by this ga_solver
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._problem = problem
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []
        self._population_size= pop_size

    def reset_population(self):
        """Initialise the population with random  individu"""
        self._population = []
        for _ in range(self._population_size):
            self._population.append(self._problem.create_individual())

    def evolve_for_one_generation(self):
        """Apply the process for one generation:
- Sort the population (descending order)
- Selection: Keep the best individuals
- Reproduction: Recreate the same number by crossing the survivors
- Mutation: For each new individual, apply a mutation according to the rate
        """
        # sort the population by fitness (descending order)
        self._population.sort(reverse=True)
        
        # Sélection of best  individu
        num_selected = int(len(self._population) * self._selection_rate)
        selected = self._population[:num_selected]
        
        # Creation of the new population while retaining the best
        new_population = selected.copy()
        
        # Reproduction until reaching the initial population size
        while len(new_population) < self._population_size:
            # Selection of parents and creation of a new individual by crossing
            parents = self._problem.select_parents(selected)
            new_individual = self._problem.crossover(parents)
            
            # Mutation 
            new_individual = self._problem.mutate(new_individual, self._mutation_rate)
            
            # Add to the new population the individu
            new_population.append(new_individual)
        
        self._population = new_population
    

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        best_individual = self.get_best_individual()  # to obtain the best individu
        worst_individual = min(self._population, key=lambda ind: ind.fitness)  # to obtain the worst individu

        
        print(f" Current Generation Summary")
        print(f" Population size: {len(self._population)}")
        print(f" Best Individual: {best_individual}")
        print(f" Worst Individual: {worst_individual}")
        

    def get_best_individual(self):
        """ Return the best Individual of the population """
        if not self._population:  # Vérify if the population is not empty
            print(" La population est vide !")
            return None
        return max(self._population, key=lambda indiv: indiv.fitness)
    
    

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        for generation in range(max_nb_of_generations):
            
            self.evolve_for_one_generation()
            best_individual = self.get_best_individual()  # find the best guy
            if best_individual is None:  # if the population is empty we stop the loop
                print(" Arrêt prématuré : La population est vide.")
                break
            if threshold_fitness is not None and best_individual.fitness >= threshold_fitness:
                print(f"Stopping at generation {generation} - Best fitness reached: {best_individual.fitness}")
                break  # we stop the loop is the threshold is reached Arrête 
