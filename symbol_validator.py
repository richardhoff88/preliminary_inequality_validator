from sympy import symbols, sympify, simplify

def check_inequalities(inequalities):
    x, y, z = symbols('x y z')
    
    parsed_inequalities = []
    for ineq in inequalities:
        if '>=' in ineq:
            left, right = ineq.split('>=')
            operator = '>='
        elif '>' in ineq:
            left, right = ineq.split('>')
            operator = '>'
        elif '=' in ineq:
            left, right = ineq.split('=')
            operator = '='
        else:
            continue

        left = left.strip('() ').replace(' ', '')
        right = right.strip('() ').replace(' ', '')
        print (left, right)
        expr = sympify(f"({left}) - ({right})")  # Convert inequality to an expression
        simplified = simplify(expr)
        parsed_inequalities.append((simplified, operator))

    # Check for contradictions and simplify
    contradictions = []
    simplified_inequalities = []
    for expr, op in parsed_inequalities:
        if expr.is_number: 
            if (expr > 0 and op == '>') or (expr >= 0 and op == '>='):
                simplified_inequalities.append(f"{expr} {op} 0 (Always True)")
            elif (expr <= 0 and op == '>') or (expr < 0 and op == '>='):
                contradictions.append(f"Contradiction found: {expr} {op} 0")
            elif (expr != 0 and op == '='):
                contradictions.append(f"Contradiction found: {expr} {op} 0")
            else:
                simplified_inequalities.append(f"{expr} {op} 0")
        else:
            simplified_inequalities.append(f"{expr} {op} 0")

    return contradictions, simplified_inequalities

inequalities = [
    "(x*z - 2*x - 5*z) > 0",
    "(4*x + y + 5) >= 0",
    "(y*z + 5*y + 1) >= 0",
    "(1) = 0",
    "(y*z - 4*y + 5*z + 3) > 0"
]

contradictions, simplified = check_inequalities(inequalities)

print("Contradictions:")
for c in contradictions:
    print(c)

print("\nSimplified Inequalities:")
for s in simplified:
    print(s)
