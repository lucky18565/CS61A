import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        proc = scheme_eval(first, env)
        # 参数求值改为循环实现，避免递归
        args = nil
        curr = rest
        while curr is not nil:
            # 一次处理一个参数，避免递归栈积累
            operand = curr.first
            evaluated_operand = scheme_eval(operand, env)
            args = Pair(evaluated_operand, args)
            curr = curr.rest
        # 反转参数顺序（因为我们是从前往后构建的）
        reversed_args = nil
        while args is not nil:
            reversed_args = Pair(args.first, reversed_args)
            args = args.rest
        return scheme_apply(proc, reversed_args, env, True)
        # END PROBLEM 3

def scheme_apply(procedure, args, env, tail=False):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        py_args = []
        while args is not nil:
            py_args.append(args.first)
            args = args.rest
        if procedure.need_env:
            py_args.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            "*** YOUR CODE HERE ***"
            return procedure.py_func(*py_args)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        return eval_all(procedure.body, procedure.env.make_child_frame(procedure.formals, args), True)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        return eval_all(procedure.body, env.make_child_frame(procedure.formals, args), True)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env , tail=False):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    if expressions is nil:
        return None
    if expressions.rest is nil:
        return scheme_eval(expressions.first, env, True)
    scheme_eval(expressions.first, env)
    return eval_all(expressions.rest, env, tail)
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not Unevaluated.
    This is only needed for apply and apply-primitive-procedure,
    as eval will have already evaluated the expressions."""
    val = scheme_apply(procedure, args, env, True)
    while isinstance(val, Unevaluated):
        val = scheme_eval(val.expr, val.env, True)
    return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # Evaluate until we get a value (not an Unevaluated)
        while isinstance(result, Unevaluated):
            # 使用带有优化版本的scheme_eval引用的unoptimized_scheme_eval
            result = unoptimized_scheme_eval(result.expr, result.env)
        return result

    # 保存原始引用，更新全局引用指向优化版本
    unoptimized_scheme_eval.__globals__['scheme_eval'] = optimized_eval
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# 保存原始版本并应用优化
_original_scheme_eval = scheme_eval
scheme_eval = optimize_tail_calls(scheme_eval)
