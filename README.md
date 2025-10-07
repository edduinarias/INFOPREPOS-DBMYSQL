# Autor: Cristian Perea
# Fecha: 2025-05-07


# Prerequisitos

1. Este Playbook utiliza las etiquetas primera / segunda para segmentar las ejecuciones del InfoPrePos y de esta forma 
poder obtener la recoleccion de informacion inicial para la primera ejecucion y sus datos comparativos en la segunda
ejecucion es por esto que se requiere estar muy atento a la etiqueta que se escoja para su ejecucion.

2. Este Playbook utiliza el numero de la orden de cambio para generar una estructura de directorios dentro del servidor
Ruster el cual fue programado para almacenar dicha informacion de los InfoPrePos. esto quiere decir que en una ejecucion
de cambio continuo lo que enlaza y configura los archivos y comparativos es el numero de Cambio este debe ser igual para 
ambas ejecuciones.

3. Este Playbook requiere que para su ejecucion sea ejecutado con los privilegios elevados debido a la informacion que 
recolecta de las maquinas

4. Este playbook requiere la existencia del servidor Ruster ya que en el se delegan tareas de almacenamiento y ejecucion 
de scripts para generacion de los reportes.

5. Este playbook requiere la ruta /transfer dentro del servidor bastion.local.com


# Posibles Errores:

1. Que se ejecute la etiqueta "segunda" sin haber ejecutado la etiqueta "primera" anteriormente.

   Esto generar error ya que para poder ejecutar la etiqueta "segunda" deben existir los archivos previos generados 
   por la etiqueta "primera" y asi tener un punto de coparacion.

2. Ejecutar las dos etiquetas al mismo tiempo:

   Esto generaria un reporte inconsistente ya que cuando se ejecutan las dos etiquetas al mismo tiempo los datos 
   recopilados por ambas etiquetas seran sobreescritos en la misma linea de tiempo haciendo que el reporte evidencie
   diferencias muy minimas o tal vez ninguna.

3. Ejecutar la etiqueta "segunda" con un numero de Cambio distinto a la "primera"

   Esto generara un error debido a que el Playbook esta diseñado para utilizar el numero de cambio como destino de
   alamcenamiento de la informacion del InfoPrePos si este dato es diferente seran dos estructuras de archivos diferentes 
   y por ende fallara el playbook al no encontrar los archivos de comparacion.


# Informacion.

1. Estructura de carpetas a generar en cada ejecucion.

Ruster
├── InfoPrePos
    └── "Numero del Cambio"
       └── backup
       └── reporte_inicial
       └── reporte_final
       └── diff

Backup: Aqui se almacena por lo pronto la copia de seguridad de la ruta /etc/ de todos los servidores donde se ejecute
para la primera ejecucion tendra en su nombre inicial.tar.gz y para la segunda ejecucion entra final.tar.gz en su nombre.

reporte_incial: Aqui se almacena la informacion recolectada en archivos separados por hosts con el siguiente formato:
data_"nombre de servidor" siendo data cualquier dato recolectado.

reporte_final: Aqui se almacena la informacion recolectada en archivos separados por hosts con el siguiente formato:
data_"nombre de servidor" siendo data cualquier dato recolectado.

diff: Aqui se almacena la informacion comparativa de los  archivos guardaos en reporte_inicial y reporte_final  con el 
siguiente formato: data_"nombre de servidor".diff siendo data cualquier dato recolectado.


