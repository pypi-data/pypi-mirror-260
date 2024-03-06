from abc import ABC, abstractmethod


class BaseOptimizer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def optimize(self, x0: list, tol=1e-6, max_iter=1000, trace=False):
        pass
