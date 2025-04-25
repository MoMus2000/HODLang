from backends import (
    yf_backend
)

class Executor:
    def __init__(self):
        self.capital      = 0
        self.conditionals = {}
        self.portfolio    = {}
        self.plot         = False
        self.backend      = None
        self.benchmarks   = None
        self.debug        = False

    def execute(self):
        if self.backend is None:
            yf_backend.YFBackTest(self).run_backtest()
        elif self.backend == "yf":
            yf_backend.YFBackTest(self).run_backtest()
        else:
            raise Exception("Backend not Defined")

    def __str__(self):
        return f"""
*** Executor ***
Capital      = {self.capital}
Portfolio    = {self.portfolio}
Conditionals = {self.conditionals}
*** End ***
""".strip()

