import numpy as np

from entities.selfAdaptiveController import SAC

class Resource:

    def __init__(self, id, max_capacity, env, seed):
        self.id = id
        self.env = env

        # Feature
        self.current_capacity = 0
        self.maximum_capacity = max_capacity

        self.rnd = np.random.RandomState(seed)
        self.SAC = SAC(id)
        self.state = False

    def update_state(self):
        """
        In this prototype. we simplify the computational features of a resource using only a feature

        A resource will be saturated when the random value be minor than the current capacity / max. capacity

        :return: boolean
        """
        self.state = self.rnd.random() < self.current_capacity / float(self.maximum_capacity)

    def has_capacity(self):
        return self.current_capacity<self.maximum_capacity

    def add_container(self):
        self.current_capacity += 1

    def remove_container(self):
        self.current_capacity -= 1

    def __str__(self):
        return "Resource_%i with %i of %i (State:%s)"%(self.id,self.current_capacity,self.maximum_capacity,self.state)