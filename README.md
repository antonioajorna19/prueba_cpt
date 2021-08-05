CONDICIONES PREVIAS:
Instalar un interprete de python en nuestra pc. https://www.python.org/downloads/

PASOS PARA LA EJECUCION:

1-Obtener el backup del service-center(Ej:ARBA01, MXCD02...) con el siguiente script:
https://github.com/mercadolibre/fury_lib-shipping-go/blob/master/Core/Services/Estimated%20Times/tools1.5/obtenerETs.groovy

2-Copiar la data obtenida, se copiara hasta donde dice "FINALIZO EL PROCESO." excluyendo esta parte y la parte de los SAME_DAYS
3-Una vez tenemos clonado el script en local(git clone https://github.com/antonioajorna19/prueba_cpt) en la misma ruta donde esta el archivo prueba_python.py(script a ejecutar) crear un archivo .csv llamado como queramos
4-Proceder a abrir la terminal de nuestro sistema operativo en la ruta donde tenemos el archivo ejecutable, es decir, el archivo prueba_python.py
5-Correr el comando python prueba_archivo.py(esto para empezar la ejecucion).
6-Se inicia la ejecucion y el script solicitara los datos correspondientes.
7-Al finalizar la ejecucion en la misma ruta donde tenemos el archivo prueba_python.py nos generar un archivo de extension .tsv con el nombre de:Archivo_modificado.tsv
8-Este archivo sera nuestro input a impactar real.
9-Copiamos todo tal cual como esta en este archivo y procedemos a impactar, colocando lo copiado como input para el script:
https://github.com/mercadolibre/fury_lib-shipping-go/blob/master/Core/Services/Estimated%20Times/tools1.5/impactarETs.groovy

