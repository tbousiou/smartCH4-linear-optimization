from ortools.linear_solver import pywraplp

def solve_lp():

    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver("GLOP")

    # Create the variables a, b and c.
    x1 = solver.NumVar(0, 300, "X1")
    x2 = solver.NumVar(0, 450, "X2")
    x3 = solver.NumVar(0, 220, "X3")

    # Create a linear constraint, 0 <= a + b + c <= 10.
    ct = solver.Constraint(0, 10, "ct")
    ct.SetCoefficient(x1, 1)
    ct.SetCoefficient(x2, 1)
    ct.SetCoefficient(x3, 100)

    # Create the objective function, 3 * a + 4 * b + 2 * c.
    objective = solver.Objective()
    objective.SetCoefficient(x1, 3)
    objective.SetCoefficient(x2, 4)
    objective.SetCoefficient(x3, 2)
    objective.SetMaximization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return {
            'objective (cost)': objective.Value(),
            'x1': x1.solution_value(),
            'x2': x2.solution_value(),
            'x3': x3.solution_value(),
        }
    else:
        return None