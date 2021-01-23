import numpy as np

def llenar_vector_no_basicas(no_basicas,matriz_restricciones,coeficientes,ubicacion_coeficientes,ZR,filas,columnas):
	for x in range(columnas-filas):
		no_basicas[x]=np.matmul(ZR,	matriz_restricciones[:,[int(ubicacion_coeficientes[x])]])-coeficientes[int(ubicacion_coeficientes[x])]
	return no_basicas

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
		if vector[i]<min and vector[i]>=0:
			indice=i
			min=vector[i]
	return indice

#ingreso de datos,solo para prueba

#Se ha llenado el tableu con todos los datos
#la matriz de restricciones solo contiene la matriz del tableu sin la Z y sin B

#Ahora se crea la matriz de simplex revisado MR (matriz reducida)

def simplexMatricial(filas, columnas, matriz_restricciones, MR, ZR, B, z_valor, C, No_basicas_ubicacion, Basicas_ubicacion):

	#B=np.matmul(MR,B)
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
	z_valor = np.dot(ZR,B)
	B = np.dot(MR,B)
	iteracion=-1
	#Se procede a calcular Y_ai
	while(True):
		iteracion+=1
		if iteracion==11:
			break
		print('-----testeo------')
		print(B)
		VNB = llenar_vector_no_basicas(VNB,tableau_restricciones,C,No_basicas_ubicacion,ZR,filas,columnas)
		print(VNB)
		Y_ai_max=np.max(VNB)

		ubicacion_maximo_VNB=int(encontrar_maximo_indice(VNB))

		Y_ai=np.matmul(MR,tableau_restricciones[:,int(No_basicas_ubicacion[ubicacion_maximo_VNB])])
		print(Y_ai)
		#Se calcula br_yj
		for i in range(filas):
			if(Y_ai[i]<=0):
				br_yj[i]=-1
			else:
				br_yj[i]=B[i]/Y_ai[i]

		#if(np.max(br_yj)<0):
		#	mensaje=4
		#	break

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

	
		if(np.max(Y_ai)<=0):
			mensaje=1
			if (tiene_negativos(B) and Y_ai_max<0):
				mensaje=3
			else:
				if(Y_ai_max==0):
					mensaje=2
			break
			mensaje=2
			break
		
		#se hace el cambio de la variable no basica a basica
		aux=No_basicas_ubicacion[ubicacion_maximo_VNB]
		No_basicas_ubicacion[ubicacion_maximo_VNB]=Basicas_ubicacion[ubicacion_minimo_br_yj]
		Basicas_ubicacion[ubicacion_minimo_br_yj]=aux
		

	#El resultado se obtiene del vector Basicas_ubicacion y B
	#Basicas ubicacion tiene el numero de columna correspondiente a cada variable
	if(mensaje==1):
		mensaje="Metodo simplex resuelto de manera exitosa"
	else:
		if(mensaje==2):
			mensaje = "Metodo simplex terminado, posibles soluciones degeneradas. Se muestran resultados"
		else:
			if(mensaje==3):
				mensaje = "Metodo simplex terminado, solucion no factible"
			else:
				mensaje = "Metodo simplex terminado, solucion no acotada"
	return Basicas_ubicacion,No_basicas_ubicacion,B, VNB, mensaje, z_valor

def obtenerIndiceMinimo(br_yj,y_i):
	min=np.inf
	indice=0
	for i in range(np.size(br_yj)):
		if br_yj[i]<min and y_i[i]>=0:
			indice=i
			min=br_yj[i]
	return indice

def tiene_negativos(LD):
	pos=False
	for i in range(len(LD)):
		if (LD[i][0]<0.0):
			pos=True
	return pos

def simplexTesteo(A, B_inv, cB, LD, C, No_basicas_ubicacion, Basicas_ubicacion, esEstandar):
	mensaje=''
	z_valor = np.dot(cB,LD)
	LD = np.dot(B_inv,LD)
	iteraciones=0
	if not esEstandar:
		variable_artificial = max(Basicas_ubicacion)
	else:
		variable_artificial = None 
	while True:
		VNB_valor = list()
		for i in No_basicas_ubicacion:
			VNB_valor.append(np.dot(cB,A[:,i])-C[i])
		VNB_valor_max = max(VNB_valor)

		if round(VNB_valor_max,4)<=0.0:
			mensaje="Metodo simplex resuelto de manera exitosa"
			if round(VNB_valor_max,4)==0.0:
				mensaje="Metodo simplex resuelto de manera exitosa, solución degenerada"
			elif variable_artificial is not None:
				if variable_artificial in Basicas_ubicacion or tiene_negativos(LD):
					mensaje = "Metodo simplex terminado, solucion infactible"
			break

		indice_VNB_valor = VNB_valor.index(VNB_valor_max)

		y_i = np.dot(B_inv,A[:,No_basicas_ubicacion[indice_VNB_valor]]).reshape(1,len(A))[0]

		noAcotado = list(filter(lambda x: round(x,4)>=0.0,y_i))
		if not noAcotado:
			mensaje = "Metodo simplex terminado, solucion no acotada"
			break

		br_yj = list()

		for i in range(len(LD)):
			if round(y_i[i],4)>0.0:
				br_yj.append(LD[i][0]/y_i[i])
			else:
				br_yj.append(np.inf)
		br_yj = np.array(br_yj)

		indice_min_br_yj = obtenerIndiceMinimo(br_yj,y_i)

		B_inv[indice_min_br_yj,:] = B_inv[indice_min_br_yj,:]/y_i[indice_min_br_yj]
		LD[indice_min_br_yj][0] = LD[indice_min_br_yj][0]/y_i[indice_min_br_yj]

		for i in [i for i in range(len(y_i)) if i!=indice_min_br_yj]:
			B_inv[i,:] = B_inv[i,:] - B_inv[indice_min_br_yj,:]*y_i[i]
			LD[i][0] = LD[i][0]-LD[indice_min_br_yj][0]*y_i[i]
		cB = cB-B_inv[indice_min_br_yj]*VNB_valor_max
		z_valor = z_valor-LD[indice_min_br_yj][0]*VNB_valor_max

		auxiliar_var = No_basicas_ubicacion[indice_VNB_valor]
		No_basicas_ubicacion[indice_VNB_valor] = Basicas_ubicacion[indice_min_br_yj]
		Basicas_ubicacion[indice_min_br_yj] = auxiliar_var 

		iteraciones+=1
	return Basicas_ubicacion,No_basicas_ubicacion,VNB_valor, mensaje, z_valor, LD,iteraciones
