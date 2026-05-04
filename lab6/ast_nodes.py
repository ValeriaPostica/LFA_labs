from dataclasses import dataclass
from typing import List, Optional, Any, Union
from abc import ABC, abstractmethod

class ASTNode(ABC):
    """Base class for all AST nodes."""
    @abstractmethod
    def __repr__(self) -> str:
        pass

@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List['Statement']
    def __repr__(self) -> str:
        return f"Program(statements={self.statements})"

# Statements
class Statement(ASTNode):
    """Base class for all statement nodes."""
    pass


@dataclass
class ExpressionStatement(Statement):
    """A statement consisting of a single expression."""
    expression: 'Expression'
    
    def __repr__(self) -> str:
        return f"ExpressionStatement({self.expression})"


@dataclass
class AssignmentStatement(Statement):
    """An assignment statement: identifier = expression."""
    identifier: str
    value: 'Expression'
    
    def __repr__(self) -> str:
        return f"AssignmentStatement({self.identifier} = {self.value})"


@dataclass
class IfStatement(Statement):
    """An if statement with optional else block."""
    condition: 'Expression'
    then_branch: List[Statement]
    else_branch: Optional[List[Statement]] = None
    
    def __repr__(self) -> str:
        return f"IfStatement(condition={self.condition}, then={self.then_branch}, else={self.else_branch})"


@dataclass
class WhileStatement(Statement):
    """A while loop statement."""
    condition: 'Expression'
    body: List[Statement]
    
    def __repr__(self) -> str:
        return f"WhileStatement({self.condition}, {self.body})"


@dataclass
class ForStatement(Statement):
    """A for loop statement."""
    variable: str
    start: 'Expression'
    end: 'Expression'
    step: Optional['Expression'] = None
    body: Optional[List[Statement]] = None
    
    def __repr__(self) -> str:
        return f"ForStatement({self.variable} from {self.start} to {self.end})"


# Expressions
class Expression(ASTNode):
    """Base class for all expression nodes."""
    pass


@dataclass
class BinaryOp(Expression):
    """A binary operation: left op right."""
    left: Expression
    operator: str
    right: Expression
    
    def __repr__(self) -> str:
        return f"BinaryOp({self.left} {self.operator} {self.right})"


@dataclass
class UnaryOp(Expression):
    """A unary operation: op operand."""
    operator: str
    operand: Expression
    
    def __repr__(self) -> str:
        return f"UnaryOp({self.operator} {self.operand})"


@dataclass
class FunctionCall(Expression):
    """A function call: func_name(arg1, arg2, ...)."""
    function_name: str
    arguments: List[Expression]
    
    def __repr__(self) -> str:
        return f"FunctionCall({self.function_name}({', '.join(map(str, self.arguments))}))"


@dataclass
class Identifier(Expression):
    """An identifier (variable name)."""
    name: str
    
    def __repr__(self) -> str:
        return f"Identifier({self.name})"


@dataclass
class NumberLiteral(Expression):
    """A numeric literal (integer or float)."""
    value: Union[int, float]
    
    def __repr__(self) -> str:
        return f"NumberLiteral({self.value})"


@dataclass
class PiLiteral(Expression):
    """The constant pi."""
    
    def __repr__(self) -> str:
        return "PiLiteral(π)"


@dataclass
class EulerLiteral(Expression):
    """The constant e (Euler's number)."""
    
    def __repr__(self) -> str:
        return "EulerLiteral(e)"


def print_ast(node: ASTNode, indent: int = 0) -> str:
    """Pretty-print an AST with indentation."""
    prefix = "  " * indent
    
    if isinstance(node, Program):
        result = f"{prefix}Program:\n"
        for stmt in node.statements:
            result += print_ast(stmt, indent + 1)
        return result
    
    elif isinstance(node, AssignmentStatement):
        result = f"{prefix}Assignment: {node.identifier}\n"
        result += print_ast(node.value, indent + 1)
        return result
    
    elif isinstance(node, ExpressionStatement):
        return print_ast(node.expression, indent)
    
    elif isinstance(node, IfStatement):
        result = f"{prefix}If:\n"
        result += f"{prefix}  Condition:\n"
        result += print_ast(node.condition, indent + 2)
        result += f"{prefix}  Then:\n"
        for stmt in node.then_branch:
            result += print_ast(stmt, indent + 2)
        if node.else_branch:
            result += f"{prefix}  Else:\n"
            for stmt in node.else_branch:
                result += print_ast(stmt, indent + 2)
        return result
    
    elif isinstance(node, WhileStatement):
        result = f"{prefix}While:\n"
        result += f"{prefix}  Condition:\n"
        result += print_ast(node.condition, indent + 2)
        result += f"{prefix}  Body:\n"
        for stmt in node.body:
            result += print_ast(stmt, indent + 2)
        return result
    
    elif isinstance(node, BinaryOp):
        result = f"{prefix}BinaryOp: {node.operator}\n"
        result += print_ast(node.left, indent + 1)
        result += print_ast(node.right, indent + 1)
        return result
    
    elif isinstance(node, UnaryOp):
        result = f"{prefix}UnaryOp: {node.operator}\n"
        result += print_ast(node.operand, indent + 1)
        return result
    
    elif isinstance(node, FunctionCall):
        result = f"{prefix}FunctionCall: {node.function_name}\n"
        for arg in node.arguments:
            result += print_ast(arg, indent + 1)
        return result
    
    elif isinstance(node, (NumberLiteral, Identifier, PiLiteral, EulerLiteral)):
        return f"{prefix}{node}\n"
    
    return f"{prefix}{node}\n"
