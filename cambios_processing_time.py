import csv
import os


PROCESING_TIME = 7
TYPE = 5
CPT = 6
FROM_CANALIZACION_SERVICEID = 0
DAY = 4
POSICION_DE_SOBRA = 9
ETD = 6


def extraer_lineas_archivo() ->list:

    #PRE:No recibimos ningun parametro.
    #POST: Retornamos una lista de lista que cada indice es cada linea del archivo .csv.
    
    lineas_archivo_csv = list()

    archivo_encontrado = False
    while not archivo_encontrado:
        nombre_archivo = input("Por favor indica el nombre del archivo .csv descargado sin su extension ")+".csv"

        try:
            with open(nombre_archivo, "r") as archivo_csv:
                leyendo_archivo = csv.reader(archivo_csv, delimiter=",")
                for linea in leyendo_archivo:
                    lineas_archivo_csv.append(linea)
            archivo_encontrado = True
        except FileNotFoundError:
            print("El archivo descrito no existe en esta ruta, indique nuevamente el nombre del archivo")
    
    return lineas_archivo_csv


def validando_campos_de_lineas(lineas_archiv_csv:list) ->None:

    #Pre: Recibimos la lista con las lineas del archivo csv.
    #POST:No se retorna nada debido a ser un procedimiento.
    '''Lo que hace esta funcion es quitar los espacios que estan de mas en base a la planilla.'''

    for id_linea in range(len(lineas_archiv_csv)):
        if len(lineas_archiv_csv[id_linea]) > 8:
            lineas_archiv_csv[id_linea].pop(POSICION_DE_SOBRA)


def escribiendo_archivo_modificado(lineas_archivo_csv_modificado:list) ->None:

    #PRE:Recibimos las lineas del archivo modificadas como listas de listas.
    #POST:Se retorna un None debido al ser un procedimiento.

    with open("Archivo_modificado.tsv", "w", newline='') as archivo_nuevo:
        escribir = csv.writer(archivo_nuevo, delimiter="\t")
        for key,warehouse,canalizacion,servicio,dia,tipo,hora,pt,tt in lineas_archivo_csv_modificado:
            escribir.writerow((key,warehouse,canalizacion,servicio,dia,tipo,hora,pt,tt))


def cambiando_pt(lineas_archivo_csv:list, ptime:str) ->None:

    #PRE:Se recibe la lista de las lineas a modificar y el valor a setear.
    #POST:Al ser un procedimiento se retorna un None.

    canalizaciones_afectadas = list()
    impacto_final = list()

    opciones = ["cpt","etd","cpt y etd"]
    print("DESEAS CAMBIAR TODOS LOS PROCESSING TIMES DE TODOS LOS:")

    for opcion in  range(len(opciones)):
        print(f"{opcion+1}){opciones[opcion]}")
    
    valor = int(input("Marque el numero de la opcion deseada "))-1
    
    if valor == 0:
        for id_linea in range(len(lineas_archivo_csv)):
            if lineas_archivo_csv[id_linea][TYPE] == opciones[valor]:
                lineas_archivo_csv[id_linea][PROCESING_TIME] = ptime
        escribiendo_archivo_modificado(lineas_archivo_csv)
    
    elif valor == 1:
        for id_linea in range(len(lineas_archivo_csv)):
            if lineas_archivo_csv[id_linea][TYPE] == opciones[valor]:
                lineas_archivo_csv[id_linea][PROCESING_TIME] = ptime
                if lineas_archivo_csv[id_linea][FROM_CANALIZACION_SERVICEID] not in canalizaciones_afectadas:
                    canalizaciones_afectadas.append(lineas_archivo_csv[id_linea][FROM_CANALIZACION_SERVICEID])
        agregando_etds(lineas_archivo_csv,canalizaciones_afectadas,impacto_final)
        escribiendo_archivo_modificado(impacto_final)


    else:
        for id_linea in range(len(lineas_archivo_csv)):
            if lineas_archivo_csv[id_linea][TYPE] == opciones[0] or lineas_archivo_csv[id_linea][TYPE] == opciones[1]:
                lineas_archivo_csv[id_linea][PROCESING_TIME] = ptime
        escribiendo_archivo_modificado(lineas_archivo_csv)

    print("Cambio realizado!")


def validando_decision(decision:int) ->int:

    #PRE: Recibimos la decision del usuario como entero.
    #POST: Retornamos como entero la decision del usuario validada.

    error_decision = False
    while not error_decision:
        if decision < 1 or decision > 3:
            decision = int(input("Estas introduciendo un numero fuera de rango, intenta nuevamente "))
        else:
            error_decision = True

    return decision


def menu() ->int:

    #PRE:No recibimos ningun argumento.
    #POST:Retornarmos como entero la decision del usuario.

    procedimientos = ["CAMBIAR UN PT PARA TODOS LOS CPTS", 
                    "CAMBIAR EL PT PARA UN CPT O VARIOS EN PARTICULAR", "CAMBIAR HORARIOS DE CPT"]

    for opcion in range(len(procedimientos)):
        print(f"{opcion+1}){procedimientos[opcion]}")

    error_decision = False
    while not error_decision:

        try:
            decision_a_validar = int(input("\nINTRODUCE LA OPCION DESEADA "))
            decision = validando_decision(decision_a_validar)
            error_decision = True
        except ValueError:
            print("ESTAS INTRODUCIENDO UN TIPO DE VALOR NO NUMERICO, MARQUE 1 PARA REINTENTAR.")

    return decision


def cambiar_horarios_cpts(lineas_archivos_csv:list) ->None:

    #PRE:Recibimos las lineas del archivo .csv a cambiar su cpt.
    #POST:Se retorna un None al ser un procedimiento.

    cpt_modificado = input("Por favor indica el valor nuevo del cpt ")
    while len(cpt_modificado) != 4:
        cpt_modificado = input("Estas introduciendo un valor invalido, intenta nuevamente introducir el valor nuevo del CPT. ")

    for id_linea in range(len(lineas_archivos_csv)):
        if lineas_archivos_csv[id_linea][TYPE] == "cpt":
            lineas_archivos_csv[id_linea][CPT] = cpt_modificado


def cambiar_pt_a_etd(impacto_pt_final:list) ->None:

    #PRE:Recibimos la lista con las canalizaciones a impactar.
    #POST:Al ser un procedimiento, se retorna un valor de tipo None.

    valor_etd = input("Introduce por favor el el valor del etd a cambiar el valor. Ej: 0800 ")
    valor_pt = input("Introduce por favor el valor el PT a cambiar ")
    cambiar_dias = int(input("Marque 1 si desea cambiarlo a dias en particular o 2 para todos "))

    if cambiar_dias ==1:
        dias_a_cambiar = input("Por favor ingrese los dias a cambiar separados por espacios ")
        dias_en_particular = dias_a_cambiar.split()
    
    for id_linea in range(len(impacto_pt_final)):
        if cambiar_dias == 1:
            for dia in dias_en_particular:
                if impacto_pt_final[id_linea][TYPE]=="etd" and impacto_pt_final[id_linea][ETD]==valor_etd and impacto_pt_final[id_linea][DAY]==dia:
                    impacto_pt_final[id_linea][PROCESING_TIME]=valor_pt
        else:
            if impacto_pt_final[id_linea][TYPE]=="etd" and impacto_pt_final[id_linea][ETD]==valor_etd:
                impacto_pt_final[id_linea][PROCESING_TIME]=valor_pt

    print("Cambio agregado!")


def cambiar_pt_cpts_particulares(lineas_archivos_csv:list) ->None:

    #PRE: Se reciben las lineas del archivo.csv a modificar.
    #POST: Al ser un procedimiento retorna un tipo de valor None.

    impacto_pt_final = list()
    canalizaciones_pt_actualizados = list()

    decision = False
    while not decision:
        cpt_actual = input("Introduce el cpt al que quieres cambiar el PT. ej: 0200 ")
        pt_time_nuevo = input("Introduce el PT deseado. Ej: 0800 ")
        cambiar_dias_en_particular = int(input("Marque 1 si desea cambiarlo para un dia en particular o 2 si cambiaras para todos los dias "))

        if cambiar_dias_en_particular == 1:
            dia_en_particular = input("Escribe los dias en particular que deseas cambiar separados por espacios. ej: monday wednesday ")
            dias_a_modificar = dia_en_particular.split()

        while len(pt_time_nuevo) != 4 :
            pt_time_nuevo = input("Estas introduciendo un valor invalido, marca nuevamente el PT deseado ")

        for id_linea in range(len(lineas_archivos_csv)):
            if cambiar_dias_en_particular == 1:
                for dia in dias_a_modificar:
                    if lineas_archivos_csv[id_linea][TYPE] == "cpt" and lineas_archivos_csv[id_linea][CPT] == cpt_actual and lineas_archivos_csv[id_linea][DAY] == dia:
                        lineas_archivos_csv[id_linea][PROCESING_TIME] = pt_time_nuevo
                        if lineas_archivos_csv[id_linea][FROM_CANALIZACION_SERVICEID] not in canalizaciones_pt_actualizados:
                            canalizaciones_pt_actualizados.append(lineas_archivos_csv[id_linea][FROM_CANALIZACION_SERVICEID])
            else:
                if lineas_archivos_csv[id_linea][TYPE] == "cpt" and lineas_archivos_csv[id_linea][CPT] == cpt_actual:
                    lineas_archivos_csv[id_linea][PROCESING_TIME] = pt_time_nuevo
                    if lineas_archivos_csv[id_linea][FROM_CANALIZACION_SERVICEID] not in canalizaciones_pt_actualizados:
                            canalizaciones_pt_actualizados.append(lineas_archivos_csv[id_linea][FROM_CANALIZACION_SERVICEID])

        #decision_cambiar_pt_a_etd = int(input("MARCA 1 SI DESEAS CAMBIAR EL PT A LOS ETDS O 2 SI NO LO DESEA ASI "))
        #if decision_cambiar_pt_a_etd == 1:
         #   cambiar_pt_a_etd(impacto_pt_final)

        seguir = int(input("MARQUE 1 PARA CONTINUAR CAMBIANDO PT A OTROS CPTS O 2 PARA FINALIZAR TODOS LOS CAMBIOS  "))

        if seguir == 1:
            print("Sigamos")
        else:
            decision = True
            agregando_etds(lineas_archivos_csv, canalizaciones_pt_actualizados, impacto_pt_final)
            escribiendo_archivo_modificado(impacto_pt_final)
            canalizaciones_pt_actualizados.clear()
            print("CAMBIO REALIZADO!")

        os.system('cls')


def agregando_etds(lineas_archivos_csv:list, canalizaciones_afectadas:list, impacto_pt_final:list) ->list:

    #PRE:Recibimos las canalizaciones afectadas y las lineas del archivo csv descargado como listas.
    #POST:Retornamos como lista todos los cpts modificados con sus etds.

    for canalizacion_serviceid in canalizaciones_afectadas:
        for id_de_linea in range(len(lineas_archivos_csv)):
            if lineas_archivos_csv[id_de_linea][FROM_CANALIZACION_SERVICEID] == canalizacion_serviceid:
                impacto_pt_final.append(lineas_archivos_csv[id_de_linea])


def main() ->None:

     
    continuar = False
    while not continuar:

        decision = menu()
        
        lineas_archivo_csv = extraer_lineas_archivo()
        validando_campos_de_lineas(lineas_archivo_csv)

        if decision == 1:
            pt = input("A cuanto deseas cambiar el Processing time?. ej: 0800 ")
            cambiando_pt(lineas_archivo_csv, pt)
            #escribiendo_archivo_modificado(lineas_archivo_csv)
                
        elif decision ==2:
            cambiar_pt_cpts_particulares(lineas_archivo_csv)

        else:
            cambiar_horarios_cpts(lineas_archivo_csv)
            escribiendo_archivo_modificado(lineas_archivo_csv)

        continuar_decision = int(input("\nMarque 1 si quieres corregir algun cambio o 2 para finalizar "))

        if continuar_decision == 1:
            continuar = False
            os.system("cls")

        else:
            continuar = True

    print("Chao")


main()
