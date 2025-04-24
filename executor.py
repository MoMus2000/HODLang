from backtest import BackTest

class Executor:
    def __init__(self):
        self.capital      = 0
        self.conditionals = {}
        self.portfolio    = {}
        self.plot         = False
        self.backend      = None


    def execute(self):
        BackTest(self).run_backtest()
        print("Executing ..")

    def __str__(self):
        return f"""
*** Executor ***
Capital      = {self.capital}
Portfolio    = {self.portfolio}
Conditionals = {self.conditionals}
*** End ***
""".strip()

