# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  Amaya Patricio
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
   
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    if len(comando) == 0:
        return False
    if 'avanzar' not in comando and 'girar' not in comando and 'detenerse' not in comando and 'saludar' not in comando:
        return False
    if ('avanzar' in comando or 'girar' in comando) and len(comando) != 3:
        return False
    if ('detenerse' in comando or 'saludar' in comando) and len(comando) != 1:
        return False 
    if len(comando) == 3:
        velocidad, tiempo = comando[1], comando[2]
        if type(velocidad) not in(int, float) or type(tiempo) not in(int, float):
            return False
        if tiempo < 0:
            return False
    pass
    return True


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # TU CODIGO ACA
    accion = comando[0]

    try:
        if accion == 'avanzar':
            velocidad, tiempo = comando[1], comando[2]
            robot.avanzar(velocidad, tiempo)
            return'Avanza', velocidad, 'por', tiempo, 'segundos'
        elif accion == 'girar':
            velocidad, tiempo = comando[1], comando[2]
            robot.girar(velocidad, tiempo)
            return'Gira', velocidad, 'por', tiempo, 'segundos'
        elif accion == 'detenerse':
            robot.detenerse()
            return 'Detenido'
        elif accion == 'saludar':
            robot.saludar()
            return 'Saludar'
    except ErrorDeSeguridad as e:
        return 'Error', e
    pass


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    # TU CODIGO ACA
    for comando in mision:
        if not comando_es_valido(comando):
            historial.append(comando, 'Error')
        else:
            resultado = ejecutar_comando(robot, comando)
            historial.append(resultado)
    pass


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    # TU CODIGO ACA
    aprobados = 0
    rechazados = 0
    print('Historial:')
    for registro in historial:
        if 'Error' in registro:
            rechazados +=1
            print("Rechazado: ", registro)
        else:
            aprobados +=1
    print("Total de aprobados: ", aprobados)
    print("Total de rechazados: ", rechazados)
    pass


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
