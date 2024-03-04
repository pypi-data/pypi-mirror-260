import unittest
from unittest.mock import MagicMock
import numpy as np
from evolutune.tuner import Tuner
from sklearn.tree import DecisionTreeClassifier


class TestTuner(unittest.TestCase):
    def setUp(self):
        # Set up a simple model for testing
        self.model_mock = MagicMock(spec=DecisionTreeClassifier)
        self.param_grid = {'param1': [1, 2, 3], 'param2': ['a', 'b', 'c']}
        self.scoring_mock = 'accuracy'
        self.population_size = 10
        self.generations = 5
        self.mutation_rate = 0.1
        self.random_state = 42
        self.n_jobs = 2

    def test_initialize_population(self):
        tuner = Tuner(self.model_mock, self.param_grid, self.scoring_mock, self.population_size,
                      self.generations, self.mutation_rate, self.random_state, self.n_jobs)
        population = tuner.initialize_population(self.population_size)

        self.assertEqual(len(population), self.population_size)
        for individual in population:
            self.assertEqual(set(individual.keys()), set(self.param_grid.keys()))

    def test_crossover(self):
        tuner = Tuner(self.model_mock, self.param_grid, self.scoring_mock, self.population_size,
                      self.generations, self.mutation_rate, self.random_state, self.n_jobs)
        parent1 = {'param1': 1, 'param2': 'a'}
        parent2 = {'param1': 2, 'param2': 'b'}

        child1, child2 = tuner.crossover(parent1, parent2)

        self.assertIsInstance(child1, dict)
        self.assertIsInstance(child2, dict)
        self.assertEqual(set(child1.keys()), set(parent1.keys()))
        self.assertEqual(set(child2.keys()), set(parent2.keys()))

    def test_mutate(self):
        tuner = Tuner(self.model_mock, self.param_grid, self.scoring_mock, self.population_size,
                      self.generations, self.mutation_rate, self.random_state, self.n_jobs)
        individual = {'param1': 1, 'param2': 'a'}

        mutated_individual = tuner.mutate(individual, self.mutation_rate)

        self.assertIsInstance(mutated_individual, dict)
        self.assertEqual(set(mutated_individual.keys()), set(individual.keys()))

    def test_calculate_fitness(self):
        tuner = Tuner(self.model_mock, self.param_grid, self.scoring_mock, self.population_size,
                      self.generations, self.mutation_rate, self.random_state, self.n_jobs)

        train_set = [np.array([[1, 2], [3, 4]]), np.array([0, 1])]
        eval_set = [np.array([[5, 6], [7, 8]]), np.array([0, 1])]

        tuner.calculate_fitness(train_set, eval_set, {'param1': 1, 'param2': 'a'})

        # Add these lines to print the calls to set_params
        calls = tuner.model.set_params.mock_calls
        print("set_params calls:", calls)

        tuner.model.set_params.assert_called_once_with(param1=1, param2='a')

    def test_fit(self):
        tuner = Tuner(self.model_mock, self.param_grid, self.scoring_mock, self.population_size,
                      self.generations, self.mutation_rate, self.random_state, self.n_jobs)

        # Mocking the Parallel function for calculate_fitness
        with unittest.mock.patch("Tuner.Parallel") as ParallelMock:
            fitness_scores = [0.5, 0.6, 0.7, 0.8, 0.9]
            ParallelMock.return_value = fitness_scores

            train_set = (np.array([[1, 2], [3, 4]]), np.array([0, 1]))
            eval_set = (np.array([[5, 6], [7, 8]]), np.array([0, 1]))

            tuner.fit(train_set, eval_set=eval_set, direction="maximize")

            self.assertEqual(tuner.best_score_, max(fitness_scores))
            self.assertTrue(set(tuner.best_params_.keys()).issubset(set(self.param_grid.keys())))


if __name__ == '__main__':
    unittest.main()

