import unittest
from sympy import Symbol
from sympy import symbols, Implies, And, Not, Or, Eq, Equivalent
from sympy.logic.boolalg import to_cnf

def sympy_to_mln_literal(expr):
    """Converts a Sympy literal to a string suitable for MLN rules."""
    # Check for Eq (value equality)
    if expr.func == Eq:
        left, right = expr.args
        return f"({left} = {right})"
    # Check for Equivalent (logical equivalence)
    elif expr.func == Equivalent:
        left, right = expr.args
        # Recursively convert left and right so that Not gets formatted as desired.
        return f"({sympy_to_mln_literal(left)} <=> {sympy_to_mln_literal(right)})"
    elif expr.func == Not:
        return f"!({sympy_to_mln_literal(expr.args[0])})"
    else:
        return str(expr)

def implication_to_clause(expr):
    """
    Converts an implication of the form A => B into a clause: ¬A1 v ¬A2 v ... v B,
    assuming A is a conjunction.
    """
    premise, conclusion = expr.args
    if premise.func == And:
        negated_literals = [f"!({sympy_to_mln_literal(arg)})" for arg in premise.args]
        negated_literals.sort()  # sort for consistent ordering
    else:
        negated_literals = [f"!({sympy_to_mln_literal(premise)})"]
    conclusion_literal = sympy_to_mln_literal(conclusion)
    return ' v '.join(negated_literals + [conclusion_literal])

def sympy_to_mln(expr):
    """
    Converts a Sympy logical expression to an MLN rule string in clausal (disjunctive) form.
    For top-level Equivalent expressions, it returns the literal conversion without CNF conversion.
    """
    if expr.func == Equivalent:
        return sympy_to_mln_literal(expr)
    if expr.func == Implies:
        return implication_to_clause(expr)
    cnf_expr = to_cnf(expr, simplify=True)
    if cnf_expr.func == And:
        clauses = [sympy_to_mln(arg) for arg in cnf_expr.args]
        return ' ^ '.join(clauses)
    elif cnf_expr.func == Or:
        return ' v '.join(sympy_to_mln_literal(arg) for arg in cnf_expr.args)
    else:
        return sympy_to_mln_literal(cnf_expr)
    
def generate_candidate_predicates(rule_expr):
    """
    Given a Sympy rule expression, extract its free symbols and generate candidate
    predicate declarations. For each symbol, if an underscore is present, we take the part
    before the underscore as the base name; otherwise, we use the whole symbol name.
    The candidate declaration is in the form:
        Base(tuple, base.lower())
    For example, for symbol 'City_t1', the candidate becomes 'City(tuple, city)'.
    """
    candidate_predicates = {}
    for sym in rule_expr.free_symbols:
        var_name = str(sym)
        if "_" in var_name:
            base_name = var_name.split("_")[0]
        else:
            base_name = var_name
        # Generate a candidate predicate only if not already present.
        if base_name not in candidate_predicates:
            candidate_predicates[base_name] = f"{base_name}(tuple, {base_name.lower()})"
    return candidate_predicates

class TestMLNConversion(unittest.TestCase):

    def test_city_determines_state_using_eq(self):
        print("Data Quality Rule 1")
        # Rule: If City_t1, City_t2, State_t1, and State_t2 hold then State_t1 equals State_t2.
        City_t1, City_t2, State_t1, State_t2 = symbols('City_t1 City_t2 State_t1 State_t2')
        rule_expr = Implies(And(City_t1, City_t2, State_t1, State_t2), Eq(State_t1, State_t2))
        mln_rule = sympy_to_mln(rule_expr)
        expected = "!(" + "City_t1" + ") v !(" + "City_t2" + ") v !(" + "State_t1" + ") v !(" + "State_t2" + ") v (State_t1 = State_t2)"
        self.assertEqual(mln_rule, expected)
        print(f'mln logic rule: {expected}')
        candidates1 = generate_candidate_predicates(rule_expr)
        print("Candidate Predicate Declarations for Rule 1:")
        for base, decl in candidates1.items():
            print(f"{base}: {decl}")

    def test_lookup_rule_using_eq(self):
        print("Data Quality Rule 2")
        # Rule: If HN_t and CT_t hold then PN_t equals PhoneVal.
        HN_t, CT_t, PN_t, PhoneVal = symbols('HN_t CT_t PN_t PhoneVal')
        rule_expr = Implies(And(HN_t, CT_t), Eq(PN_t, PhoneVal))
        mln_rule = sympy_to_mln(rule_expr)
        expected = "!(" + "CT_t" + ") v !(" + "HN_t" + ") v (" + "PN_t = PhoneVal" + ")"
        self.assertEqual(mln_rule, expected)
        print(f'mln logic rule: {expected}')
        candidates2 = generate_candidate_predicates(rule_expr)
        print("Candidate Predicate Declarations for Rule 2:")
        for base, decl in candidates2.items():
            print(f"{base}: {decl}")

    def test_unique_phone_per_state_using_eq(self):
        print("Data Quality Rule 3")
        # Rule: If Phone_t1, Phone_t2, State_t1, and State_t2 hold then State_t1 equals State_t2.
        Phone_t1, Phone_t2, State_t1, State_t2 = symbols('Phone_t1 Phone_t2 State_t1 State_t2')
        rule_expr = Implies(And(Phone_t1, Phone_t2, State_t1, State_t2), Eq(State_t1, State_t2))
        mln_rule = sympy_to_mln(rule_expr)
        expected = "!(" + "Phone_t1" + ") v !(" + "Phone_t2" + ") v !(" + "State_t1" + ") v !(" + "State_t2" + ") v (State_t1 = State_t2)"
        self.assertEqual(mln_rule, expected)
        print(f'mln logic rule: {expected}')
        candidates3 = generate_candidate_predicates(rule_expr)
        print("Candidate Predicate Declarations for Rule 3:")
        for base, decl in candidates3.items():
            print(f"{base}: {decl}")

    def test_boolean_equivalence_using_equivalent(self):
        print("Data Quality Rule 4")
        # New Rule: For each record, IsActive is logically equivalent to Not(IsTerminated).
        IsActive, IsTerminated = symbols('IsActive IsTerminated')
        rule_expr = Equivalent(IsActive, Not(IsTerminated))
        mln_rule = sympy_to_mln(rule_expr)
        expected = "(IsActive <=> !((IsTerminated)))"  # note that extra parentheses might occur
        # Remove redundant parentheses from expected for easier matching:
        expected = expected.replace("!((IsTerminated))", "!(IsTerminated)")
        self.assertEqual(mln_rule, expected)
        print(f'mln logic rule: {expected}')
        candidates4 = generate_candidate_predicates(rule_expr)
        print("Candidate Predicate Declarations for Rule 4:")
        for base, decl in candidates4.items():
            print(f"{base}: {decl}")

if __name__ == '__main__':
    unittest.main()
