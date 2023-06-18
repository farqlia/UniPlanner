import pygad
from planner.models.groups import Group, Course
from typing import List

from planner.parsing.parse_json import load_from_json
from planner.models.groups import DayOfWeek

IMPOSSIBLE_VALUE = -99999999

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

    def translate_solution(self, gen_solution: List[int]) -> tuple[list[Group], list[Group]]:
        return sorted([self.get_group(gene_id, gene) for gene_id, gene in enumerate(gen_solution)
                       if self.get_group(gene_id, gene).occurs_odd()]), \
            sorted([self.get_group(gene_id, gene) for gene_id, gene in enumerate(gen_solution)
                    if self.get_group(gene_id, gene).occurs_even()])

    def get_all_courses(self, gen_solution: List[int]) -> list[Group]:
        return sorted([self.get_group(gene_id, gene) for gene_id, gene in enumerate(gen_solution)])

    def fitness_func(self, ga_instance, solution: List[int], solution_idx) -> int:
        odd_groups, even_groups = self.translate_solution(solution)
        if not is_possible(odd_groups) or not is_possible(even_groups):
            return IMPOSSIBLE_VALUE
        fitness = 0
        fitness += Search.rate_shape(odd_groups)
        fitness += Search.rate_shape(even_groups)
        fitness += Search.rate_category(odd_groups)
        fitness += Search.rate_category(even_groups)
        return fitness

    @staticmethod
    def rate_shape(groups, punish_many_days: bool = True):
        punishment = 0
        week_days: List[List[Group]] = [[group for group in groups if group.day == day] for day in DayOfWeek]
        punishment += sum(
            [(day_groups[-1].end_time - day_groups[0].start_time).seconds / 1000 for day_groups in week_days
             if len(day_groups) > 0])
        if punish_many_days:
            days_num = len([day for day in week_days if len(day) > 0])
            punishment += days_num * 1000
        return -punishment

    @staticmethod
    def rate_category(sol_groups):
        reward = 0
        reward += sum([100 for group in sol_groups if group.is_preferred()])
        return reward

    def select_solutions(self, solutions) -> List:
        unique_solutions = set(tuple(solution) for solution in solutions
                               if self.fitness_func(None,solution,None) > -99999999)
        return reversed(list(unique_solutions)) \
            if len(unique_solutions) > 0 else []

    def find_solutions(self):
        ga_instance = pygad.GA(**self.setup_parameters())
        ga_instance.run()
        ga_instance.plot_fitness()
        solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
        for group in self.get_all_courses(solution):
            print(group)
        print('fitness = ', solution_fitness)
        print('solution idx = ', solution_idx)
        selected_solutions = self.select_solutions(ga_instance.best_solutions)
        print(selected_solutions)
        return [(self.get_all_courses(list(solution))) for solution in selected_solutions]

    def setup_parameters(self):
        return {
            'num_generations': 20,
            'num_parents_mating': 8,
            'sol_per_pop': 1000,
            'num_genes': len(self.courses),
            'gene_space': [range(len(course)) for course in self.courses],
            'fitness_func': self.fitness_func,
            'keep_elitism': 5,
            'parent_selection_type': 'tournament',
            'K_tournament': 10,
            'crossover_type': 'scattered',
            'gene_type': int,
            'crossover_probability': 0.75,
            'mutation_probability': 0.1,
            'save_best_solutions': True,
            'suppress_warnings': True,
        }

    @staticmethod
    def delete_excluded_groups(courses_: List[Course]) -> List[List[Group]]:
        return [[group_ for group_ in course.groups if not group_.is_excluded()] for course in courses_]

    @staticmethod
    def delete_excluded_courses(courses_: List[List[Group]]):
        return [course_groups for course_groups in courses_ if len(course_groups) > 0]

    @staticmethod
    def preprocess(cour):
        without_excluded_groups = Search.delete_excluded_groups(cour)
        without_excluded_courses = Search.delete_excluded_courses(without_excluded_groups)
        return without_excluded_courses


def get_best_solutions(cour: List[Course]) -> List[List[Group]]:
    search = Search(courses=cour)
    return search.find_solutions()


if __name__ == '__main__':
    courses = load_from_json('../../data/courses.json')
    best_sol = get_best_solutions(courses)
    print(best_sol)
