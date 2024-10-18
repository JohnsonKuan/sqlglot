from sqlglot import exp
from sqlglot.optimizer.scope import traverse_scope


def deduplicate_projections(expression: exp.Expression) -> exp.Expression:
    """
    Rewrite sqlglot AST to remove duplicate column projections while preserving the original order.

    Example:
        >>> import sqlglot
        >>> sql = "SELECT a, b, a FROM x"
        >>> expression = sqlglot.parse_one(sql)
        >>> deduplicate_projections(expression).sql()
        'SELECT a, b FROM x'

    Args:
        expression (exp.Expression): expression to optimize
    Returns:
        exp.Expression: optimized expression with duplicates removed while maintaining original order
    """

    for scope in traverse_scope(expression):
        if isinstance(scope.expression, exp.Select):
            # Remove duplicates while preserving order
            scope.expression.set(
                "expressions",
                list(dict.fromkeys(scope.expression.selects)),
            )

    return expression
