import numpy as np

# ======= CONTROLS ======= #
def int_function(x,y):
    return 3*x + 4*y*y     # integral to be calculated

lbx = -1                   # lower bound for x
ubx = 1                    # upper bound for x
lby = -1                   # lower bound for y
uby = 1                    # upper bound for y

strata = 10                # number of strata in the latin square
draws = 10000              # number of random draws
replications = 20          # number of replications, used for calculating confidence intervals


# ======= CALCULATIONS ======= #
mu_fin = np.zeros([replications,strata*draws])
for j in range(replications):
    mu = np.zeros(strata*draws)
    for i in range(draws):
        load = np.zeros([strata,strata])   # generate a loading matrix for a latin square
        rnd1 = np.random.uniform(0,1,strata)

        pos = np.zeros(strata)
        for row in range(strata):
            pos[row] = np.ceil(rnd1[row]*(strata-row))-1

        forbid = np.zeros(strata)
        load[0,int(pos[0])] = 1
        forbid[int(pos[0])] = 1

        for row in range(1,strata):   # calculate allowed positions within a latin square
            tick = -1
            for col in range(strata):
                if forbid[col] != 1:
                    tick = tick + 1
                if tick == pos[row]:
                    load[row,col] = 1
                    forbid[col] = 1
                    break

        rnd2 = np.random.uniform(0,1,strata)
        rnd3 = np.random.uniform(0,1,strata)

        for row in range(strata):   # assign values to allowed positions within a latin square
            x = lbx + ((load[row,:].argmax() + rnd2[row]) * (ubx-lbx)) / strata
            y = uby - ((row + rnd3[row]) * (uby-lby)) / strata
            mu[i*strata+row] = int_function(x,y)
    mu_fin[j] = (ubx-lbx)*(uby-lby)*np.sum(mu)/(strata*draws)

print('Result                  :  ',np.mean(mu_fin))
print('95 % confidence interval: [',np.mean(mu_fin)-1.96*np.std(mu_fin),',',np.mean(mu_fin)+1.96*np.std(mu_fin),']')
