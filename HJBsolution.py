import numpy as np
import sympy as sym

def z(q1, q2, k, a):
    return sym.Matrix(q1 - q2 + 1, 1, lambda i, j : sym.exp(-a * k * (i + q2) ** 2))

def f(i, j, k, e1, e2, l1, l2, p, q1, q2):
    if i == j:
        return j * k * (e1 * l1 - e2 * l2) - p * k * (j + q2)**2
    elif i == j - 1:
        return l1 * sym.exp(-1 - k * e1)
    elif i == j + 1:
        return l2 * sym.exp(-1 - k * e2)
    else:
        return 0
    
def A(q1, q2, k, e1, e2, l1, l2, p):
    return sym.Matrix(q1 - q2 + 1, q1 - q2 + 1, lambda i, j : f(i, j, k, e1, e2, l1, l2, p, q1, q2))

def exponential(A, n):
    result = A ** 0
    B = A**0
    for i in range(1,n):
        B *= A * (1 / i)
        result += B
    return(result.applyfunc(lambda x : float(x)))

#exponentialを真面目に計算
#def omega(T, t, A, z):
#    return exponential((T-t) * A, 100) * z

#pade近似
def omega(T, t, A, z):
    return (A ** 0 - 1 / 2 * (T-t) * A + 1 / 10 * A**2 * (T-t) **2 - 1 / 120 * A ** 3 * (T-t)**3).inv() * (A ** 0 + 1 / 2 * (T-t) * A + 1 / 10 * A**2 * (T-t) **2 + 1 / 120 * A ** 3 * (T-t)**3) * z

def h(k, q, omega, q1):
    return 1 / k * sym.log(omega[q + q1])

def delta(T, t, k, l1, l2, p, q1, q2, e1, e2, a, q):
    Omega = omega(T, t, A(q1, q2, k, e1, e2, l1, l2, p), z(q1, q2, k, a))
    h0 =  h(k, q, Omega, q1)
    h1 =  h(k, q - 1, Omega, q1)
    h2 =  h(k, q + 1, Omega, q1)
    return (1 / k + e1 - h1 + h0, 1 / k + e2 - h2 + h0)
