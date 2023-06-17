import pygad
import numpy as np
from planner.parsing.parse_json import load_from_json
from planner.models.groups import Group
from typing import List

file_name = '../../data/courses.json'
courses = load_from_json(file_name)


def get_group(course_id, group_id):
    return courses[course_id].groups[group_id]


def translate_solution(gen_solution):
    return sorted([get_group(gene_id, gene) for gene_id, gene in enumerate(gen_solution)])


def is_possible(groups: List[Group]) -> bool:
    for index in range(len(groups) - 1):
        curr_group = groups[index]
        next_group = groups[index + 1]
        if curr_group.day == next_group.day and curr_group.end_time > next_group.start_time:
            return False
    return True


def fitness_func(ga_instance, solution, solution_idx):
    sol_groups = translate_solution(solution)
    if is_possible(sol_groups):
        return 1000
    else:
        return 0

num_generations = 1  # Number of generations.
num_parents_mating = 1  # Number of solutions to be selected as parents in the mating pool.
sol_per_pop = 10  # Number of solutions in the population.
num_genes = len(courses)
last_fitness = 0
gene_space = [range(len(course.groups)) for course in courses]
def on_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(
        fitness=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]))
    print("Change     = {change}".format(
        change=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness))
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       fitness_func=fitness_func,
                       on_generation=None,
                       gene_type=int,
                       gene_space=gene_space,
                       random_seed=1)

# Running the GA to optimize the parameters of the function.
ga_instance.run()

# ga_instance.plot_fitness()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
"""print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))"""
for group in translate_solution(solution):
    print(group)
print('fitness = ', solution_fitness)
print('solution idx = ', solution_idx)
#prediction = np.sum(np.array(function_inputs) * solution)
#print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

"""if ga_instance.best_solution_generation != -1:
    print("Best fitness value reached after {best_solution_generation} generations.".format(
        best_solution_generation=ga_instance.best_solution_generation))"""

# Saving the GA instance.
filename = 'genetic'  # The filename to which the instance is saved. The name is without extension.
ga_instance.save(filename=filename)

# Loading the saved GA instance.
loaded_ga_instance = pygad.load(filename=filename)
"""loaded_ga_instance.plot_fitness()"""
