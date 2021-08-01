import csv

PROCESING_TIME = 7
TYPE = 5
CPT = 6
FROM_CANALIZACION_SERVICEID = 0


def extraer_lineas_archivo() ->list:

    #PRE:No recibimos ningun parametro.
    #POST: Retornamos una lista de lista que cada indice es cada linea del archivo .csv.
    
    lineas_archivo_csv = list()
    nombre_archivo = input("Por favor indica el nombre del archivo .csv descargado sin su extension ")+".csv"

    try:
        with open(nombre_archivo, "r") as archivo_csv:
            leyendo_archivo = csv.reader(archivo_csv, delimiter=",")

            for linea in leyendo_archivo:
                lineas_archivo_csv.append(linea)
    except FileNotFoundError:
        print("El archivo descrito no existe en esta ruta, marque 1 para volver a intentar")
    return lineas_archivo_csv


def escribiendo_archivo_modificado(lineas_archivo_csv_modificado:list) -> None:

    #PRE:Recibimos las lineas del archivo modificadas como listas de listas.
    #POST:Se retorna un None debido al ser un procedimiento.

    with open("Archivo_modificado.tsv", "a", newline='') as archivo_nuevo:

        escribir = csv.writer(archivo_nuevo, delimiter="\t")
        
        for a,b,c,d,e,f,g,h,i,l in lineas_archivo_csv_modificado:
            escribir.writerow((a,b,c,d,e,f,g,h,i,l))


def cambiando_pt(lineas_archivo_csv:list, ptime:str) -> None:

    #PRE:Se recibe la lista de las lineas a modificar y el valor a setear.
    #POST:Al ser un procedimiento se retorna un None.

    for id_linea in range(len(lineas_archivo_csv)):
        if lineas_archivo_csv[id_linea][TYPE] == "cpt":
            lineas_archivo_csv[id_linea][PROCESING_TIME] = ptime

    print("Cambio realizado")


def validando_decision(decision:int) ->int:

    #PRE: Recibimos la decision del usuario como entero.
    #POST: Retornamos como entero la decision del usuario validada.

    error_decision = True
    while error_decision:
        if decision < 1 or decision > 3:
            decision = int(input("Estas introduciendo un numero fuera de rango, intenta nuevamente "))
        else:
            error_decision = False

    return decision


def menu() -> int:

    #PRE:No recibimos ningun argumento.
    #POST:Retornarmos como entero la decision del usuario.

    decision = None
    procedimientos = ["Cambiar un PT para todos los CPT", 
                    "Cambiar el PT para un CPT o Varios en particular", "Cambiar horarios de CPT"]

    for opcion in range(len(procedimientos)):
        print(f"{opcion+1}){procedimientos[opcion]}")

    try:
        decision = int(input("Introduce por favor la decision deseada "))
        decision_validada = validando_decision(decision)

    except ValueError:
        print("Estas introduciendo un tipo de valor no numerico, marque 1 para reintentar nuevamente. ")

    return decision


def cambiar_horarios_cpts(lineas_archivos_csv:list) -> None:

    #PRE:Recibimos las lineas del archivo .csv a cambiar su cpt.
    #POST:Se retorna un None al ser un procedimiento.

    cpt_modificado = input("Por favor indica el valor nuevo del cpt ")
    while len(cpt_modificado) != 4:
        cpt_modificado = input("Estas introduciendo un valor invalido, intenta nuevamente introducir el valor nuevo del CPT. ")

    for id_linea in range(len(lineas_archivos_csv)):
        if lineas_archivos_csv[id_linea][TYPE] == "cpt":
            lineas_archivos_csv[id_linea][CPT] = cpt_modificado

    return lineas_archivos_csv


def cambiar_pt_cpts_particulares(lineas_archivos_csv:list) ->list:

    #PRE: Se reciben las lineas del archivo.csv a modificar.
    #POST: Se retorna en una lista el from_canalizacion_serviceid de los cpts afectados por el cambio de PT.

    canalizaciones_pt_actualizados = list()
    decision = True
    while decision:
        
        cpt_actual = input("Introduce el cpt al que quieres cambiar el PT. ej: 0200 ")
        pt_time_nuevo = input("Introduce el PT deseado. Ej: 0800 ")

        while len(pt_time_nuevo) != 4 :
            pt_time_nuevo = input("Estas introduciendo un valor invalido, marca nuevamente el PT deseado ")

        for id_linea in range(len(lineas_archivos_csv)):
            if lineas_archivos_csv[id_linea][TYPE] == "cpt" and lineas_archivos_csv[id_linea][CPT] == cpt_actual:
                lineas_archivos_csv[id_linea][PROCESING_TIME] = pt_time_nuevo
     
                if canalizaciones_pt_actualizados.count(lineas_archivos_csv[id_linea][FROM_CANALIZACION_SERVICEID]) < 1:
                    canalizaciones_pt_actualizados.append(lineas_archivos_csv[id_linea][FROM_CANALIZACION_SERVICEID])

    #agregar la posibilidad de modificar etds, para modificar ambas o uno solo

        impacto_pt = agregando_etds(lineas_archivos_csv, canalizaciones_pt_actualizados, cpt_actual)
        escribiendo_archivo_modificado(impacto_pt)
        canalizaciones_pt_actualizados.clear()
        seguir = int(input("1 para continuar cambiando PT a otros cpts, 2 para salir "))

        if seguir == 1:
            print("Sigamos")
        else:
            decision = False
  

def agregando_etds(lineas_archivos_csv:list, canalizaciones_afectadas:list, cpt_actual:str):

    #PRE:Recibimos las canalizaciones afectadas y las lineas del archivo csv descargado como listas.
    #POST:Retornamos como lista todos los cpts modificados con sus etds.

    impacto_pt = list()
    for canalizacion_serviceid in canalizaciones_afectadas:
        for id_de_linea in range(len(lineas_archivos_csv)):
            if lineas_archivos_csv[id_de_linea][FROM_CANALIZACION_SERVICEID] == canalizacion_serviceid:
                impacto_pt.append(lineas_archivos_csv[id_de_linea])

    return impacto_pt


def main():

     
    continuar = True
    while continuar:
        decision = menu()
        if decision != None:
            lineas_archivo_csv = extraer_lineas_archivo()

            if len(lineas_archivo_csv) != 0:

                if decision == 1:
                    pt = input("A cuanto deseas cambiar el Processing time?. ej: 0800 ")
                    cambiando_pt(lineas_archivo_csv, pt)
                    escribiendo_archivo_modificado(lineas_archivo_csv)
                
                elif decision ==2:
                    cambiar_pt_cpts_particulares(lineas_archivo_csv)

                else:
                    cambiar_horarios_cpts(lineas_archivo_csv)
                    escribiendo_archivo_modificado(lineas_archivo_csv)

        continuar_decision = int(input("\nMarque 1 si quiere hacer mas cambios o 2 para salir "))

        if continuar_decision == 1:
            print("\nSigamos")#deberia ir la funcion de limpiar pantalla
        else:
            continuar = False

    print("Chao")


main()
