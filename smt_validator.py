from z3 import *

inequalities = [
    "x*z - 2*x - 5*z > 0",
    "4*x + y + 5 >= 0",
    "3*x*(y*z + 5*y + 1) >= 0",
    "1 == 0",
    "y*z - 4*y + 5*z + 3 > 0",
    
]

def check_inequalities(inequalities):
    solver = Solver()

    x, y, z = Reals('x y z')

    for ineq in inequalities:
        solver.add(eval(ineq))

    if solver.check() == sat:
        print("The system is satisfiable.")
        model = solver.model()
        print("Solution:")
        for var in model:
            print(f"{var} = {model[var]}")
    else:
        print("There are contradictions, not valid.")

check_inequalities(inequalities)
