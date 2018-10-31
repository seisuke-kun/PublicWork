from sympy import *
import pandas as pd
import numpy as np
t = Symbol('t')

# 以下，二分法を用いて方程式の解を探すプログラム
def findplusvalue(function,value):
    n = 1
    while n<10:
        if function(n) > value:
            return n
        else:
            n=n+1
    return 100
            
def findvalue(function,value):
    if findplusvalue(function,value) == 100:
        return 'error'
    else:
        plus = findplusvalue(function,value) 
        minus = 0
        n = 1
        while n<30:
            if function((plus+minus)/2)-value<0:
                minus = (plus+minus)/2
                n += 1
            else:
                plus = (plus+minus)/2
                n += 1
        return minus

# 以下，a,b,vを推測するプログラム
def fvinfty(t,v):                         #f_{V_\invty}の定義
    return exp(1)**(-t**2/(2*v))/sqrt(2*pi*v)

def phi(v):                               #確率
    return integrate(exp(1)**(-t**2/(2*v))/sqrt(2*pi*v),(t,1,oo)).evalf()

def dfbool(v):                            #データの取得およびbool表の作成
    df = pd.read_csv('8951-8952.csv')
    df_diff = df['8951 Equity']-df['8952 Equity']
    return df_diff/v >1

def OTS(x):                               #Occupation time statistic
    df_bool = dfbool(x)
    return df_bool.sum()/len(df_bool)

def cyukanchi(x):                         #V_\inftyを見つけるための関数
    return x-findvalue(phi,OTS(x))

def countdiff(listobject):                #listobjectの中から変化の数をカウント
    counter = 0
    for i in range(len(listobject)-1):
        if listobject[i] != listobject[i+1]:
            counter += 1
    return counter

def CS(listobject):                       #crossing statistic
    return countdiff(listobject)/len(listobject)

def beta(listobject,v):                   #betaの推定
    return sqrt(2*pi)*CS(listobject)/(2*fvinfty(1,v))

def alpha(beta,v):                        #alphaの推定
    return beta**2/(2*v)

vinfty=findvalue(cyukanchi,0)
b=beta(dfbool(vinfty),vinfty).evalf()
a=alpha(b,vinfty).evalf()

print(a,b,vinfty)
