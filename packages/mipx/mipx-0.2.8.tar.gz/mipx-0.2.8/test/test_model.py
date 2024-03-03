import mipx
if __name__ == '__main__':
    model = mipx.Model(solver_id='SCIP')
    x = model.addVars(2, name='x', vtype=mipx.Vtype.BINARY)
    z = model.addVar(name='x')
    m = model.addVars(1, (3, 4), name='hello')
    y = model.addVar(name='x', ub=3000)
    model.addConstrMultiply(z, (x[0], y))
    model.setObjective(z)

    status = model.optimize()
    if status == mipx.OptimizationStatus.OPTIMAL:
        print("success")
