import pandas as pd
from ortools.linear_solver import pywraplp


def solve_l_simple():

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


substrate_names = ['S1', 'S2']

df = pd.DataFrame({
    'B': [10, 10],
    'W': [40, 20],
    'C': [3, 2],
    'D': [0, 0],
}, index=substrate_names, dtype=float)


def solve_lp(df, target, error_pct):
    # ensure error_pct is a float and in the range (0, 1)
    error_pct = float(error_pct)
    if not 0 <= error_pct <= 1:
        raise ValueError("error_pct must be in the range (0, 1)")
    # ensure target is a positive number
    if target <= 0:
        raise ValueError("target must be a positive number")
    
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver("GLOP")

    # Create the variables s1, s2, ... sn
    x = {}
    for index, row in df.iterrows():
        x[index] = solver.NumVar(0, row['W'], index)

    # Objective function coefficients
    obj_coeff = df['C'] + df['D']

    # Create the objective function.
    objective = solver.Objective()
    for var_name, var in x.items():
        objective.SetCoefficient(var, obj_coeff[var_name])
    objective.SetMinimization()

    # Create a linear constraint. Σ((Bi-T-e) * Xi) <= 0
    deviation = target * error_pct
    ct1 = solver.Constraint(target - deviation, target + deviation, "ct1")
    for var_name, var in x.items():
        # print(df.loc[var_name, 'B'])
        ct1.SetCoefficient(var, df.loc[var_name, 'B'])

    # Create a linear constraint. Σ((Bi-T+e) * Xi) >= 0
    # ct2 = solver.Constraint(target + error_pct, solver.infinity(), "ct2")
    # for var_name, var in x.items():
    #     ct2.SetCoefficient(var, df.loc[var_name, 'B'])

    
    # print(solver.constraints())
    # print(solver.variables())

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return {
            'objective (cost)': objective.Value(),
            'solution': {var_name: var.solution_value() for var_name, var in x.items()},
        }
    else:
        return None


# print(solve_lp2(df, 500, 10))
