import numpy as np

def llenar_vector_no_basicas(no_basicas,matriz_restricciones,coeficientes,ubicacion_coeficientes,ZR,filas,columnas):
	for x in range(columnas-filas):
		no_basicas[x]=np.matmul(ZR,	matriz_restricciones[:,[int(ubicacion_coeficientes[x])]])-coeficientes[int(ubicacion_coeficientes[x])]

def encontrar_maximo_indice(vector):
	max=vector[0]
	indice=0
	for i in range(np.size(vector)):
		if vector[i]>max:
			indice=i
			max=vector[i]
	return indice

def encontrar_minimo_positivo_indice(vector):
	min=vector[0]
	indice=0
	for i in range(np.size(vector)):
		if vector[i]<min and vector[i]>=0 or min<0:
			indice=i
			min=vector[i]
	return indice

def tiene_negativos(vector):
	for i in range(np.size(vector)):
		if (vector[i]<0):
			return True
	return False
#ingreso de datos,solo para prueba

#Se ha llenado el tableu con todos los datos
#la matriz de restricciones solo contiene la matriz del tableu sin la Z y sin B

#Ahora se crea la matriz de simplex revisado MR (matriz reducida)

def simplexMatricial(filas, columnas, matriz_restricciones, MR, ZR, B, z_valor, C, No_basicas_ubicacion, Basicas_ubicacion):

	B=np.matmul(MR,B)
	tableau_restricciones= matriz_restricciones
	#crear vector de variables no basicas VNB,el vector Y_ai y el vector br_yj
	VNB=np.zeros(columnas-filas)
	Y_ai=np.zeros(filas)
	Y_ai_max=0 #espacio para el elemento maximo del vector VNB
	ubicacion_maximo_VNB=0#espacio para la ubicacion del elemento maximo en VNB
	br_yj=np.zeros(filas)
	ubicacion_minimo_br_yj=0
	#Comienza el ciclo
	#Valor_funcion_max es para evitar ciclos en soluciones degeneradas: se verifica que exista una mejora en la solucion
	mensaje=0
	valor_funcion_objetivo_max=0
	#Se procede a calcular Y_ai
	while(True):
		
		llenar_vector_no_basicas(VNB,tableau_restricciones,C,No_basicas_ubicacion,ZR,filas,columnas)
		Y_ai_max=np.max(VNB)
		if(Y_ai_max<=0):
			mensaje=1
			if(tiene_negativos(B)):
				mensaje=3
			break

		ubicacion_maximo_VNB=int(encontrar_maximo_indice(VNB))
		Y_ai=np.matmul(MR,tableau_restricciones[:,int(No_basicas_ubicacion[ubicacion_maximo_VNB])])

		#Se calcula br_yj
		for i in range(filas):
			if(Y_ai[i]<=0):
				br_yj[i]=-1
			else:
				br_yj[i]=B[i]/Y_ai[i]

		if(np.max(br_yj)<0):
			mensaje=4
			break

		#se cambia la matriz MR
		ubicacion_minimo_br_yj=int(encontrar_minimo_positivo_indice(br_yj))
		if(Y_ai[ubicacion_minimo_br_yj]==0):
			break
		for i in range(filas):
			MR[ubicacion_minimo_br_yj][i]=MR[ubicacion_minimo_br_yj][i]/Y_ai[ubicacion_minimo_br_yj]

		for i in range(filas):
			for j in range(filas):
				if(i!=ubicacion_minimo_br_yj):
					MR[i][j]=MR[i][j]-MR[ubicacion_minimo_br_yj][j]*Y_ai[i]
		
		
		for i in range(filas):
			ZR[i]=ZR[i]-MR[ubicacion_minimo_br_yj][i]*Y_ai_max

		B[ubicacion_minimo_br_yj]=B[ubicacion_minimo_br_yj]/Y_ai[ubicacion_minimo_br_yj]
		for i in range(filas):
			if (i!=ubicacion_minimo_br_yj):
				B[i]=B[i]-B[ubicacion_minimo_br_yj]*Y_ai[i]

		z_valor=z_valor-B[ubicacion_minimo_br_yj]*Y_ai_max

		#medida para evitar soluciones degeneradas
		if(z_valor<0):
			if(z_valor<valor_funcion_objetivo_max):
				valor_funcion_objetivo_max=z_valor
			else:
				if(valor_funcion_objetivo_max==z_valor):
					mensaje=2
					break
		#se hace el cambio de la variable no basica a basica
		aux=No_basicas_ubicacion[ubicacion_maximo_VNB]
		No_basicas_ubicacion[ubicacion_maximo_VNB]=Basicas_ubicacion[ubicacion_minimo_br_yj]
		Basicas_ubicacion[ubicacion_minimo_br_yj]=aux

	#El resultado se obtiene del vector Basicas_ubicacion y B
	#Basicas ubicacion tiene el numero de columna correspondiente a cada variable
	if(mensaje==1):
		print("Metodo simplex resuelto de manera exitosa")
	else:
		if(mensaje==2):
			print("Metodo simplex terminado, posibles soluciones degeneradas. Se muestran resultados")
		else:
			if(mensaje==3):
				print("Metodo simplex terminado, solucion no factible")
			else:
				print("Metodo simplex terminado, solucion no acotada")
	return Basicas_ubicacion,No_basicas_ubicacion,B, VNB,mensaje
