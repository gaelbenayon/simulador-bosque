import random

#N tamaño del bosque
#di densidad inicial
#tq tiempo en minutos que tarda el árbol en quemarse
#px probabilidad de que un árbol se queme en un minuto dado si x vecinos se queman 

# N=30
# di=0.6
# tq=3
# px=[0,0.2,0.4,0.6,0.8,1,1,1,1]

tamanoBosque = 30
densidadesIniciales = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
tiempoQuemado = 3
probabilidadQuemado = [0,0.2,0.4,0.6,0.8,1,1,1,1]
matriz = [[""] * tamanoBosque for _ in range(tamanoBosque)]

def obtenerNumeroAleatorio():
    return random.random()

def definirEstadoInicial():
    numeroAleatorio = obtenerNumeroAleatorio()
    if numeroAleatorio <= densidadActual:
        #la celda va a comenzar con un árbol vivo
        estadoInicial = -1
    else:
        #la celda va a comenzar vacía
        estadoInicial = -2
    return estadoInicial

def iniciarCentroEnLlamas():
    for fila in range(-1,2):  # [-1,0,1]
        for celda in range(-1,2):# [-1,0,1]
            #le asigno el tq por defecto, para que comience quemándose
            matriz[int((tamanoBosque/2))+fila][int((tamanoBosque/2))+celda] = tiempoQuemado

def contarVecinosQuemandose(iFilaProp,iColumnaProp):
    cantVecinosQuemandose = 0
    #el máx de vecinos totales es 8; puede haber de 0 a 8 quemándose

    for fila in range(iFilaProp - 1, iFilaProp +2):
        for col in range(iColumnaProp - 1, iColumnaProp + 2):
            #hay que verificar que la fila y la columna sean mayores de 0, y menores de 30
            if (0 < fila < len(matriz)) and (0 < col < len(matriz)):
                #si la fila y columna son iguales a los de la celda que vino por props, lo salteamos (no es un vecino)
                if (fila,col) != (iFilaProp,iColumnaProp):
                    #si el estado del vecino es >0 es porque se está quemando
                    if matriz[fila][col] > 0:
                        cantVecinosQuemandose += 1          
    return cantVecinosQuemandose

def crearBosque():
    #modificamos la matriz, que se definió con cada celda vacía [""]
    for fila in matriz:
        for i in range(len(matriz)):
            #se le va a asignar el valor según lo que reciba del return de la función definirEstadoInicial
            fila[i] = definirEstadoInicial()   
    #Queremos que las 9 celdas centrales empiecen quemándose, reemplazando el valor que se le asignó en el for de arriba
    iniciarCentroEnLlamas()
    
def obtenerInformacionBosque(solicitudProp):
    cantArbolesVivos = 0
    cantArbolesQuemados = 0 
    cantArbolesQuemandose = 0
    cantCeldasVacias = 0

    for fila in matriz:
        for i in range(len(matriz)):
            if fila[i] > 0:
                #árboles quemándose
                cantArbolesQuemandose += 1
            elif fila[i] == -1:
                #árboles vivos
                cantArbolesVivos += 1
            elif fila[i] == 0:
                #árboles quemados
                cantArbolesQuemados += 1
            elif fila[i] == -2:
                #celdas vacías
                cantCeldasVacias += 1
            #se podría agregar para calcular celdas vacías

    if solicitudProp == "vivos":
        return cantArbolesVivos
    elif solicitudProp == "quemados":
        return cantArbolesQuemados
    elif solicitudProp == "quemandose":
        return cantArbolesQuemandose
    elif solicitudProp == "vacias":
        return cantCeldasVacias

def definirNuevoEstado(estadoProp,iFilaProp,iColumnaProp):
    if estadoProp > 0:
        #si hay un árbol quemándose, debe restarse 1
        return estadoProp - 1
    elif estadoProp == -2:
            #si está vacía, queda así
        return -2
    elif estadoProp == -1:
        #ARBOLES VIVOS:
        #pasa a estado Tq con una probabilidad Px, siendo x la cantidad de vecinos quemandose. Si el árbol no se quema, se mantiene vivo.

        cantVecinosQuemandose = contarVecinosQuemandose(iFilaProp,iColumnaProp)

        probArbolQuemado = probabilidadQuemado[cantVecinosQuemandose]

        numeroAleatorio = obtenerNumeroAleatorio()
        if numeroAleatorio <= probArbolQuemado:
            return tiempoQuemado
        else:
            return -1
    elif estadoProp == 0:
        #continúa quemado
        return 0          

def imprimirBosque(tiempo):
    if tiempo == 0:
        #la primera vez que se inicia, crea el bosque
        crearBosque()
    else:
        #el tiempo ya no es cero, el bosque ya está creado
        
        #Creo una nueva matriz para guardarle los nuevos valores y cambiarlos todos de una.
        matriz_nuevo_estado = []
        for fila in range(len(matriz)):
            matriz_nuevo_estado += [[]]
            for columna in range(len(matriz)):
                matriz_nuevo_estado[fila] += [[]]

        for fila in range(len(matriz)):
            for columna in range(len(matriz)):
                #se le asigna a cada celda el valor que obtenga del return de definirNuevoEstado
                matriz_nuevo_estado[fila][columna] = definirNuevoEstado( matriz[fila][columna],fila,columna)

        for fila in range(len(matriz)):
            for columna in range(len(matriz)):
                #se reemplazan los valores de la matriz original por los valores que obtuvo la nueva matriz
                matriz[fila][columna] = matriz_nuevo_estado[fila][columna]
                
simulacionesDeseadas = 100
#se definen como lista porque son mutables
arbolesQuemadosAcumulados = [0]
arbolesVivos = [0]

def calcularPromedioArbolesQuemados():
    return (arbolesQuemadosAcumulados[0] * 100) / arbolesVivos[0]

def iniciarSimulacion():
    tiempo = 0
    #PRIMER PASO!: imprimo el bosque
    imprimirBosque(tiempo)

    #obtengo la cantidad de árboles quemándose
    cantArbolesQuemandose = obtenerInformacionBosque("quemandose")
    #acumulo la cantidad de árboles vivos
    arbolesVivos[0] += obtenerInformacionBosque("vivos")

    #mientras haya árboles quemándose, sumo un minuto, vuelvo a imprimir el bosque, y calculo otra vez los árboles que quedaron quemándose
    while cantArbolesQuemandose > 0:
        tiempo += 1
        imprimirBosque(tiempo)
        cantArbolesQuemandose = obtenerInformacionBosque("quemandose")

    arbolesQuemadosAcumulados[0] += obtenerInformacionBosque("quemados")

#esta densidad va a ser reemplazada desde el for con el valor de cada di
densidadActual = 0

print("+----------+----------------+")
print("| Densidad | Bosque quemado |")

for i in range(len(densidadesIniciales)):
    #en cada iteración, le asigno a la densidadActual, un valor de la lista de densidades
    densidadActual = densidadesIniciales[i]

    #se hacen 100 simulaciones por cada di
    for _ in range(simulacionesDeseadas):
        iniciarSimulacion()
        #al finalizar cada simulación, acumulo los árboles quemados
        # arbolesQuemadosAcumulados[0] += obtenerInformacionBosque("quemados")
    
    print("+----------+----------------+")
    print(f"| {densidadActual: < 8} | {round(calcularPromedioArbolesQuemados(),2): < 12} % |")

    #una vez finalizada las 100 simul. de la densidadActual, reseteo los valores para que con las otras di empiecen en 0
    arbolesQuemadosAcumulados[0] = 0
    arbolesVivos[0] = 0

print("+----------+----------------+")