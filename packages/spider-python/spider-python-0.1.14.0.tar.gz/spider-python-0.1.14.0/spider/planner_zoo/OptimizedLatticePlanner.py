import spider
from spider.planner_zoo.LatticePlanner import LatticePlanner
from spider.optimize.TrajectoryOptimizer import FrenetTrajectoryOptimizer


class OptimizedLatticePlanner(LatticePlanner):
    def __init__(self, config=None):
        super(LatticePlanner, self).__init__(config)
        self.optimizer = FrenetTrajectoryOptimizer(self.steps, self.dt)


    @classmethod
    def default_config(cls) -> dict:
        """
        :return: a configuration dict
        """
        config = super().default_config()
        config.update({

            # 'optimizer': 'spider.feasible_planners.Optimizer',
            # 'optimizer_config': {
            #     'optimizer': 'spider.feasible_planners.optimizers.SimulatedAnnealing',
            #     'optimizer_config': {
            #         'initial_temp': 10000,
            #         'cooling_rate': 0.9999,
            #         'min_temp': 0.0001,
            #         'max_iterations': 100000
            #     }
            # }
        })
        return config


    def plan(self, goal, start=None):
        if start is None:
            start = self.agent.state

        self.set_goal(goal)
        self.set_start(start)

        self.initialize_lattice()
        self.expand_lattice()
        self.find_solution()

        return self.path

    def set_goal(self, goal):
        self.goal = goal

    def set_start(self, start):
        self.start = start

    def initialize_lattice(self):
        pass

    def expand_lattice(self):
        pass

    def find_solution(self):
        pass