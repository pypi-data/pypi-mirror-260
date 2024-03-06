import numpy as np

from .BaseOptimizer import BaseOptimizer


# Test
class Simplex(BaseOptimizer):
    def __init__(self, func: callable, alpha=1, gamma=2, rho=0.5, sigma=0.5) -> None:
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.rho = rho
        self.sigma = sigma
        self.func = func

    def simplex_worker(self, x: list):
        # Sorting the vertices
        x = np.array(x)
        f_x = np.array([self.func(i) for i in x])
        n = len(x)
        order = np.argsort(f_x)
        x_sorted = x[order]
        f_x_sorted = f_x[order]
        centroid = np.mean(x_sorted[:-1], axis=0)
        x_r = centroid + self.alpha * (centroid - x_sorted[-1])
        f_x_r = self.func(x_r)
        # Reflection
        if f_x_sorted[0] <= f_x_r < f_x_sorted[-2]:
            x_sorted[-1] = x_r
        # Expansion
        elif f_x_r < f_x_sorted[0]:
            x_e = centroid + self.gamma * (x_r - centroid)
            if self.func(x_e) < f_x_r:
                x_sorted[-1] = x_e
            else:
                x_sorted[-1] = x_r
        # Contraction
        elif f_x_r >= f_x_sorted[-2]:
            x_c = centroid + self.rho * (x_sorted[-1] - centroid)
            if self.func(x_c) < f_x_sorted[-1]:
                x_sorted[-1] = x_c
            # Shrink
            else:
                for i in range(1, n):
                    x_sorted[i] = x_sorted[0] + self.sigma * (x_sorted[i] - x_sorted[0])
        return x_sorted

    def optimize(self, x0: list, tol=1e-6, max_iter=1000, trace=False):
        x = x0
        if trace:
            trace = [np.array(x[0])]
        for _ in range(max_iter):
            x = self.simplex_worker(x)
            if trace:
                trace.append(x[0])
            if np.std([self.func(i) for i in x]) < tol:
                break
        if not trace:
            return x[0]
        else:
            return trace
