
class Memoize:
    """
    Memoization se refiere efectivamente a recordar los resultados de las
    llamadas de método basadas en las entradas del método y luego devolver
    el resultado recordado en lugar de calcular el resultado de nuevo.
    Se puede pensar en ello como un caché para los resultados del método.
    """
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]