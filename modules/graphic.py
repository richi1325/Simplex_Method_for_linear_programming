import re

def restriccionesGrafico(z,variablesNB):
    while(True):
        numero_restricciones = input('¿Cuántas restricciones contiene tu problema?:')
        x = numero_restricciones.isdigit()
        if x:
            numero_restricciones = int(numero_restricciones)
            if numero_restricciones>0:
                break
            elif numero_restricciones<=0:
                print('La cantidad no puede ser negativa o 0, intentalo de nuevo')
        else:
            print('¡Inserte una cantidad válida!')
    restricciones = list()
    LD=list()
    Op=list()
    z = re.sub(r'(-*[0-9]+\.*[0-9]*)([a-zA-Z]+[0-9]*)',r'\1*\2',z)
    for i in range(numero_restricciones):
        restricciones.append(re.sub(r'\s+','',input(f'Inserte la restriccion #{i+1}:')))

        x=re.search(r'-*[0-9]+\.*[0-9]*$',restricciones[i])
        LD.append(restricciones[i][x.start():x.end()])
        x=re.search(r'<=|=|>=',restricciones[i])
        Op.append(restricciones[i][x.start():x.end()])
        restricciones[i]=re.sub(r'(-*[0-9]+\.*[0-9]*)([a-zA-Z]+[0-9]*)',r'\1*\2',restricciones[i])
        x=re.search(r'<=|=|>=',restricciones[i])
        restricciones[i]=restricciones[i][0:x.start()]

        
    
    return z, restricciones,LD,Op


def intersectarRestricciones(restricciones):
    
        
    restriccionesFactibles=list()
    restriccionesInFactibles=list()
    
    contador=0
    while(True):
        if contador == len(restricciones):
            break
        else:
            resp=list()
            for restriccion in restricciones:
                if restricciones[contador] == restriccion:
                    resp=[]
                    pass
                else:
                    
                    f1= sympify(restriccion)
                    
                    resp=sympy.solve([sympify(restricciones[contador]), sympify(restriccion)], dict=True)
                if len(resp)==0:
                    pass
                else:
                    restriccionesFactibles.append(restriccion)
        contador+=1

    return restriccionesFactibles







