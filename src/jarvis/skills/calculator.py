"""Calculator skill — evaluate math expressions safely."""

import ast
import operator
from .registry import Skill, SkillResult

# Supported operators
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value}")
    elif isinstance(node, ast.BinOp):
        op_func = _OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op_func(_safe_eval(node.left), _safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        op_func = _OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_func(_safe_eval(node.operand))
    else:
        raise ValueError(f"Unsupported expression: {type(node).__name__}")


class CalculatorSkill(Skill):
    name = "calculator"
    description = "Perform math calculations"
    triggers = ["calculate", "what is", "what's", "compute", "solve", "math", "equals"]

    # Common math functions
    _FUNCS = {
        "sqrt": "math.sqrt",
        "abs": "abs",
        "round": "round",
        "ceil": "math.ceil",
        "floor": "math.floor",
    }

    def matches(self, query: str) -> bool:
        """Check if this skill should handle the given query.
        Only matches if there's a number in the query."""
        import re
        if not any(trigger in query.lower().strip() for trigger in self.triggers):
            return False
        # Require at least one number to avoid matching 'what is my ip'
        return bool(re.search(r'\d', query))

    def execute(self, query: str, context: dict) -> SkillResult:
        expr = self._extract_expression(query)

        if not expr:
            return SkillResult(success=False, message="What calculation would you like me to perform?")

        try:
            # Replace common math function names
            import math
            safe_expr = expr
            for alias, func in self._FUNCS.items():
                safe_expr = safe_expr.replace(alias, func)

            # Parse and evaluate safely
            tree = ast.parse(safe_expr, mode="eval")
            result = _safe_eval(tree.body)

            # Format result nicely
            if isinstance(result, float):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)

            return SkillResult(
                success=True,
                message=f"{expr} = {result}",
                data={"expression": expr, "result": result}
            )
        except ZeroDivisionError:
            return SkillResult(success=False, message="I can't divide by zero.")
        except Exception as e:
            return SkillResult(success=False, message=f"I couldn't evaluate that expression: {e}")

    def _extract_expression(self, query: str) -> str:
        """Extract the math expression from the query."""
        lower = query.lower()
        for trigger in self.triggers:
            if lower.startswith(trigger):
                expr = query[len(trigger):].strip()
                # Remove trailing question mark
                expr = expr.rstrip("?").strip()
                return expr
        return query.strip()
