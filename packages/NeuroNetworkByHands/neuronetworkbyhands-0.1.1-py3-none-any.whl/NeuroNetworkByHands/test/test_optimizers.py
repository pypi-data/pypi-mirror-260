import benchmark_functions as bf
import numpy as np

from ..Optimizers.simplex import Simplex


def test_simplex():
    x0 = np.random.rand(3, 2)
    f = bf.Ackley(n_dimensions=2)
    f1 = bf.Hypersphere(n_dimensions=2)
    f2 = bf.Rastrigin(n_dimensions=2)
    f3 = bf.Rosenbrock(n_dimensions=2)
    s = [Simplex(i) for i in [f, f1, f2, f3]]
    result = [i.optimize(x0) for i in s]
    answer = [i.minima()[0] for i in [f, f1, f2, f3]]
    print(result, answer)
    assert np.allclose(result, answer, atol=1e-2)
