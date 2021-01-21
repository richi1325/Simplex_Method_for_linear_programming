import numpy as np

def construirTableau(cB, cNB, A, B, esEstandar, ultimo_negativo,variablesB, variablesNB):
    if esEstandar:
        C = np.concatenate((cNB,cB),axis=0).reshape(1,len(cB)+len(cNB))
        A = np.concatenate((A,B),axis=1)
        tableau = np.concatenate((C,A),axis=0)
        B_inv = np.linalg.inv(B)
    
    else:
        j=97
        while('x'+chr(j) in variablesNB):
            j+=1
        
        variable_artificial = 'x'+chr(j)
        variables_tableau = variablesNB + variablesB + [variable_artificial]

        B_artificial = list()
        for i in range(len(B)):
            B_artificial.append([1.0])
        B_artificial = np.array(B_artificial)

        big_M = float(10**(len(str(int(max(cNB))))+1))
        cB_tableau = np.concatenate((cB,[big_M]),axis=0)
        B_tableau = np.concatenate((B,B_artificial),axis=1) 
        
        #modificando elementos simplex matricial
        #variables
        variable_auxiliar = variablesB[ultimo_negativo]
        variablesB[ultimo_negativo] = variable_artificial
        variablesNB.append(variable_auxiliar)

        #cB
        cB[ultimo_negativo] = big_M

        #B
        B[:,ultimo_negativo] = np.array(B_artificial).reshape(1,len(B_artificial)) 

        C = np.concatenate((cNB,cB_tableau),axis=0).reshape(1,len(cB_tableau)+len(cNB))
        A = np.concatenate((A,B_tableau),axis=1)
        tableau = np.concatenate((C,A),axis=0)
        B_inv = np.linalg.inv(B)

    return tableau, variablesB, variablesNB, cB, B_inv
