# Genetic Algorithm Solver  

This project implements a **Genetic Algorithm (GA)** to solve various optimization problems. The core of the system is a flexible **`GAProblem`** class, which allows users to define their own problems by specifying constraints, evaluation functions, and other parameters. Once a problem is defined, it can be solved using the **GA solver**.  

## Supported Problems  

- **Mastermind Problem**: A code-breaking game modeled as an optimization problem.  
- **Traveling Salesman Problem (TSP)**: A combinatorial optimization problem where the goal is to find the shortest possible route that visits each city exactly once and returns to the starting point.  

## Project Structure  

- **`ga_solver.py`** – The main Genetic Algorithm solver. It takes a problem defined using `GAProblem` and applies GA to find a solution.  
- **`cities.py`** – Handles city data for the TSP problem.  
- **`cities.txt`** – List of cities used for testing the TSP.  
- **`mastermind.py`** – Implements the Mastermind problem using GA.  
- **`mastermind_problem.py`** – Defines the Mastermind problem structure.  
- **`tsp_problem.py`** – Defines the TSP problem structure.  

## How to Use  

1. **Define Your Problem**  
   - Create a new problem by defining a class that extends `GAProblem`.  
   - Implement necessary methods such as fitness evaluation and mutation.  

2. **Run the GA Solver**  
   - If using a predefined problem (e.g., TSP or Mastermind):  
     ```sh
     python ga_solver.py
     ```  
   - If using a custom problem, ensure it is implemented in `GAProblem` and then execute `ga_solver.py`.  
