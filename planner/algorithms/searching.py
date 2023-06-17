import pygad
from planner.models.groups import Group, Course
from typing import List

from planner.parsing.parse_json import load_from_json





def is_possible(groups: List[Group]) -> bool:
    for index in range(len(groups) - 1):
        curr_group = groups[index]
        next_group = groups[index + 1]
        if curr_group.day == next_group.day and curr_group.end_time > next_group.start_time:
            return False
    return True


class Search:
    def __init__(self, courses: List[Course]):
        self.courses = Search.preprocess(courses)

    def get_group(self, course_id: int, group_id: int) -> Group:
        return self.courses[course_id][group_id]

    def translate_solution(self, gen_solution: List[int]) -> List[Group]:
        return sorted([self.get_group(gene_id, gene) for gene_id, gene in enumerate(gen_solution)])

    def fitness_func(self, ga_instance, solution: List[int], solution_idx) -> int:
        sol_groups = self.translate_solution(solution)
        if is_possible(sol_groups):
            return 0
        else:
            return -9999

    def find_solutions(self):
        ga_instance = pygad.GA(**self.setup_parameters())
        ga_instance.run()
        ga_instance.plot_fitness()
        solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
        for group in self.translate_solution(solution):
            print(group)
        print('fitness = ', solution_fitness)
        print('solution idx = ', solution_idx)
        filename = 'genetic'  # The filename to which the instance is saved. The name is without extension.
        ga_instance.save(filename=filename)
        return [self.translate_solution(solution)]

    def setup_parameters(self):
        return {
            'num_generations': 100,  # Number of generations.
            'num_parents_mating': 3,  # Number of solutions to be selected as parents in the mating pool.
            'sol_per_pop': 10,  # Number of solutions in the population.
            'num_genes': len(courses),
            'gene_space': [range(len(course.groups)) for course in courses],
            'fitness_func': self.fitness_func,
            'crossover_type': 'scattered',
            'gene_type': int,
            'random_seed': 1,
        }

    @staticmethod
    def delete_excluded(courses):
        return [[group_ for group_ in course.groups if not group_.is_excluded()] for course in courses]

    @staticmethod
    def preprocess(courses):
        return Search.delete_excluded(courses)


def get_best_solutions(courses: List[Course]) -> List[List[Group]]:
    search = Search(courses=courses)
    return search.find_solutions()


if __name__ == '__main__':
    courses = load_from_json('../../data/courses.json')
    print(get_best_solutions(courses))

