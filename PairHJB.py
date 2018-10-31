from sympy import *
import numpy as np
t = Symbol('t')

mu = 0.8
rho = 0.1
sigma = 0.5
lam = 0.07
epsilon = 0.005

def phiplus(x):
    return integrate(t**(Rational(rho/mu)-1) * exp(-(t**2)/2 + sqrt(2*mu)/sigma * t * x) , (t, 0, oo)).evalf()

def phiminus(x):
    return integrate(t**(Rational(rho/mu)-1) * exp(-(t**2)/2 - sqrt(2*mu)/sigma * t * x) , (t, 0, oo)).evalf()

def phiplusprime(x):
    return (sqrt(2*mu) / sigma * integrate(t**Rational(rho/mu) * exp(-(t**2)/2+ sqrt(2*mu)/sigma * t * x),(t,0,oo))).evalf()
            
def phiminusprime(x):
    return (-sqrt(2*mu) / sigma * integrate(t**Rational(rho/mu) * exp(-(t**2)/2- sqrt(2*mu)/sigma * t * x),(t,0,oo))).evalf()

def g1(x, e):
    return -(x + e)

def g2(x, e):
    return x -e

def evalfunction(x1, x2):
    a = complex(phiminusprime(x1))
    b = complex(-phiplusprime(x1))
    c = complex(phiminusprime(-x2))
    d = complex(-phiplusprime(-x2))
    e = complex(phiminus(x1))
    f = complex(-phiplus(x1))
    g = complex(phiminus(-x2))
    h = complex(-phiplus(-x2))
    phiprime = np.matrix([[a,b],[c,d]])
    phi = np.matrix([[e,f],[g,h]])
    return np.linalg.norm((phiprime**-1).dot(np.array([-1,-1]))-(phi**-1).dot(np.array([lam/rho - g2(x1, epsilon), lam/rho + g1(-x2, epsilon)])))

for i in range(1,10):
    for j in range(1,10):
        print(i,j,evalfunction(i*0.1,j*0.1))

#print(phiplus(0.2))
