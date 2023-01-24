from scipy.integrate import quad
from numpy.linalg import solve
import matplotlib.pyplot as plt
import time
import numpy as np

def Er(x):
    if 0 <= x <=1 : return 10
    if 1 < x <= 2: return 5
    if 2 < x <= 3: return 1


def get_e(i,x):
    x_i1 = get_xi(i-1)
    x_i2 = get_xi(i)
    x_i3 = get_xi(i+1)
    if x_i1 < x <=x_i2 : return (x - x_i1)/ (x_i2-x_i1)
    if x_i2 < x <x_i3 : return (x_i3 - x) / (x_i3-x_i2)
    return 0
def get_xi(i):
    return h*i
def get_e_derivative(i,x):
    x_i1 = get_xi(i-1)
    x_i2 = get_xi(i)
    x_i3 = get_xi(i+1)
    if x_i1 < x <=x_i2: return 1/(x_i2-x_i1)
    if x_i2 < x <x_i3: return -1/(x_i3-x_i2)
    return 0
def get_B(i,j):
    left = max(a,get_xi(i-1),get_xi(j-1))
    right = min(b,get_xi(i+1),get_xi(j+1))
    def func_to_integrate(x):
        return get_e_derivative(i,x) * get_e_derivative(j,x)
    return  (get_e(i,0) * get_e(j,0)) - quad(func_to_integrate,left,right)[0]
def get_L(i):
    left = max(a, get_xi(i-1))
    right = min(get_xi(i+1), b)
    def func_to_integrate(x):
        return get_e(i, x) / Er(x)
    return 5 * get_e(i, 0) - (quad(func_to_integrate, left,right)[0]) - 2*get_B(n,i)

if __name__ == '__main__':
    start_time = time.time()
    a = 0
    b = 3
    n = 5000
    h = 3 / n
    Bmatrix = [[get_B(i,j) if abs(i-j)<=1 else 0  for i in range(n)] for j in range(n)]
    Lmatrix = [get_L(i) for i in range(n)]
    resMatrix = solve(Bmatrix,Lmatrix).tolist()
    resMatrix.append(2)
    plt.plot([i*h for i in range(n+1)],resMatrix,marker='o')
    plt.show()
    print(resMatrix)
    print("--- %s seconds ---" % round(time.time() - start_time, 2))
