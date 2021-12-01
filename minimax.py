import numpy as np
from scipy.optimize import linprog

# a function for calculating nash equilibrium and as a result minmax strategy for player 2 
def minmax_strategies(n1, n2, U):
    c = np.concatenate((np.array([[1,-1]]), np.zeros((1, n2))), axis = 1)
    A_eq = np.concatenate((np.array([[0,0]]), np.ones((1, n2))), axis = 1)
    b_eq = 1
    A_ub = np.concatenate((np.concatenate(((-1)*np.ones((1,n1)).T, np.ones((1,n1)).T), axis = 1), U), axis = 1)
    b_ub = np.zeros((n1, 1))
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='simplex')
    return res.x

# a function for calculating Utility of player i with S = (s1, s2)
def Utility_calc(U,i,S1,S2):
    if i == 1:
        return np.matmul(np.matmul(S1, U),S2.T)
    if i == 2:
        return np.matmul(np.matmul(S2, U),S1.T)

# function for checking if a strategy Si for player i is dominated or not
def domination(U1, U2, i, Si): # i = 1,2
    if i==1:
        U = U1
    elif i==2:
        U = U2
    num_strategies = U.shape
    for index in range(num_strategies[i-1]):
        Ai = np.zeros((1, num_strategies[i-1]))
        Ai[0][index] = 1
        if not np.array_equal(Ai, Si):
            dom = True
            for ind in range(num_strategies[2-i]): # if i = 2 then -i = 1 and vice versa 
                Ai_minus = np.zeros((1,num_strategies[2-i]))
                Ai_minus[0][ind] = 1
                if Utility_calc(U,i,Si,Ai_minus) >= Utility_calc(U,i,Ai,Ai_minus):
                    dom = False
                    break
            if dom == True:
                return True
    return False

# a function for getting the values from user 
def input_payoff():
    n1 = int(input("Enter number of P1's actions: ")) 
    n2 = int(input("Enter number of P2's actions: ")) 

    U1 = np.zeros((n1,n2))
    U2 = np.zeros((n1,n2))

    #P1's Utility
    for i in range(n1):
        U1[i] = np.array(list(map(int, input("Enter {}th row of P1's utilities: ".format(i+1)).split())))[0:n2]

    #P2's Utility
    for i in range(n1):
        U2[i] = np.array(list(map(int, input("Enter {}th row of P2's utilities: ".format(i+1)).split())))[0:n2]

    return [n1, n2, U1, U2]


# code starts here -----------------------------------------------------------------------
[n1, n2, U1, U2] = input_payoff()

x = minmax_strategies(n1, n2, U1)
minmax_strategy_S2 = x[2:]
minmax_value_2 = x[0] - x[1]

x = minmax_strategies(n2, n1, U2.T)
minmax_strategy_S1 = x[2:]
minmax_value_1 = x[0] - x[1]

print('minmax_strategy_S1 & minmax_value_1:')
print(minmax_strategy_S1, minmax_value_1)
print('minmax_strategy_S1 & minmax_value_1:')
print(minmax_strategy_S2, minmax_value_2)


print('dominated strategies for ROW player')
for index in range(n1):
    Ai = np.zeros((1, n1))
    Ai[0][index] = 1
    if domination(U1, U2, 1, Ai) == True:
        print(index+1)

print('dominated strategies for COl player')
for index in range(n2):
    Ai = np.zeros((1, n2))
    Ai[0][index] = 1
    if domination(U1, U2, 2, Ai) == True:
        print(index+1)
