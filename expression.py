from abc import ABC, abstractmethod

class Expression(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def accept(self, visitor):
        pass

class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expression(self)

