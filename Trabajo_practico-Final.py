
#Importamos la librerias necesarias para el programa
import json
import subprocess
import sys

# Creamos una funcion para instalar el paquete "Colorama"
def install (paquete):
    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

#intentamos importar "Colorama", si este programa no esta instalado, se instala automaticamente.
try:
    import colorama
except ImportError:
    print("Instalando colorama...")
    install("colorama")

#Importamos colorama y lo inicializamos
from colorama import init, Fore
init()

#Definimos las variables que van a contener la lista y el nombre del archivo [Mas abajo se personaliza el nombre del archivo.]
archivo = "default.json"
estudiantes = []


# Creamos la funcion cargar estudiante, que se utilizara para agregar estudiantes nuevos en la lista.
def cargar_estuadiante():
    #Pedimos la matricula, y verificamos que esta ya no este en uso.
    matricula = input(Fore.RESET + "Matricula: ")
    if any(alumno['matricula'] == matricula for alumno in estudiantes):
        print(Fore.RED + "[!] Error: la matricula ya existe")
        return
    #Pedimos el resto de los datos.
    nombre = input(Fore.RESET +"Nombre: ")
    apellido = input(Fore.RESET +"Apellido: ")
    provincia = input(Fore.RESET +"Provincia: ")
    
    #Hacemos un bucle while, para pedir la edad y el promedio (Ya que estos tienen que ser numeros) por si se carga un dato erroneo, no tener que volver a poner todos los datos nuevamente
    while True:
        try:
            edad = int(input(Fore.RESET +"Edad: "))
            promedio = float(input(Fore.RESET +"Promedio: "))
            break
        except ValueError:
            print(Fore.RED + "[!] Error: La edad tiene que ser un numero entero y el promedio un numero.")
            
    #Creamos el diccionario con los datos del estudiante, poniendole mayusculas al principio a los campos "Nombre","Apellido" y "provincia"
    alumno = {
        "matricula" : matricula,
        "nombre" : nombre.capitalize(),
        "apellido" : apellido.capitalize(),
        "provincia": provincia.capitalize(),
        "edad" : edad,
        "promedio" : promedio
    }
    #Agregamos al estudiante a la lista y mostramos el mensaje de que el alumno fue cargado con exito
    estudiantes.append(alumno)
    print(Fore.GREEN + f"[+] El estudiante {nombre} {apellido} fue agregado con exito")
    
#Definimos la funcion para buscar a un estudiante por su matricula.
def buscar_estudiante_matricula(matricula):
    #Verificamos si la matricula se encuentra, si esta no esta definida en ningun estudiante, tirara un error.
    try:
        alumno = next(estudiante for estudiante in estudiantes if estudiante['matricula'] == matricula)
        print(Fore.RESET + f'''
            ----------------------- Alumno {alumno['nombre']} {alumno['apellido']} -------------------------
            
                                    Matricula: {alumno['matricula']}
                                    Provincia: {alumno['provincia']}
                                    Edad: {alumno['edad']}
                                    Promedio: {alumno['promedio']}             
              \n''')
    except StopIteration:
        print(Fore.RED + "[!] El usuario no se encuentra en la lista")
        
        
#Definimos la funcion para listar todos los estudiantes que estan en la lista
def listar_estudiantes():
    #Verificamos si la lista esta vacia, si no tiene estudiantes cargado tirara un error, sino mostrara todos los estudiantes cargados.
    if estudiantes:
        for i in estudiantes:
            print(Fore.RESET + f'''
                ----------------------- Alumno {i['nombre']} {i['apellido']} -------------------------
                
                                        Matricula: {i['matricula']}
                                        Provincia: {i['provincia']}
                                        Edad: {i['edad']}
                                        Promedio: {i['promedio']}             
                \n''')
    else:
        print(Fore.RED + "[!] No hay estudiantes en la lista")
        
#Definimos la funcion para calcular el promedio de edad y de notas de todos los estudiantes cargados.
def calcular_promedio():
    #Verificamos que la lista tenga estudiantes cargados
    if not estudiantes:
        print(Fore.RED + "[!] No hay estudiantes en la lista")
    else:
        #Tomamos y sumamos todos los promedios y las edades de los estudiantes
        total_edad = sum(alumno['edad'] for alumno in estudiantes)
        total_notas = sum(alumno['promedio'] for alumno in estudiantes)
        #Dividimos la suma anterior con la cantidad total de estudiantes en la lista y mostramos por consola el resultado.
        print(f'La edad promedio de los alumnos es de {total_edad / len(estudiantes):.2f}')
        print(f'La nota promedio de los alumnos es de {total_notas / len(estudiantes):.2f}')
    
 
 #Creamos la funcion para listar a todos los alumnos que su nota sea "6" o mayor       
def listar_estudiantes_aprobados():
    #Verificamos si hay estudiantes cargados en la lista.
    if estudiantes:
        for alumno in estudiantes:
            #Iteramos en la lista y tomamos el valor "promedio" para hacer una comparativa. 
            if alumno['promedio'] >= 6:
                print(Fore.RESET + f'''
                    ----------------------- Alumno {alumno['nombre']} {alumno['apellido']} -------------------------
                    
                                            Matricula: {alumno['matricula']}
                                            Provincia: {alumno['provincia']}
                                            Edad: {alumno['edad']}
                                            Promedio: {alumno['promedio']}             
                    \n''')
    else:
        print(Fore.RED + "[!] No hay ningun estudiante en la lista")
        
#Creamos la funcion para eliminar estudiantes por matricula.
def eliminar_estudiante(matricula):
    try:
        #Intentamos encontrar al estudiante con la matricula dada por el usuario. Una vez encontrado lo guardamos en la variable para posteriormente con el metodo .remove, sacarlo de la lista
        estudiante_encontrado = next(estudiante for estudiante in estudiantes if estudiante['matricula'] == matricula)
        estudiantes.remove(estudiante_encontrado)
        print(Fore.RED + f"[-] El estudiante {estudiante_encontrado['nombre']} {estudiante_encontrado['apellido']} se ha eliminado con éxito.")
    except StopIteration:
        print(Fore.RED + f"[!] El estudiante con la matrícula {matricula} no se ha encontrado en la lista.")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}")
   
#Creamos la funcion para guardar el archivo.     
def guardar_archivo():
    global archivo
    try:
        #Abrimos el archivo en formato escritura, para poder pasar nuestra lista.
        with open(archivo, "w") as f:
            json.dump(estudiantes, f)
        print(Fore.GREEN + f"[+] {len(estudiantes)} Estudiantes fueron guardados exitosamente.")
    except Exception as e:
        print(Fore.RED + f"[!] Error al guardar el archivo: {e}")
    
#Si bien en el trabajo no pide cargar los estudiantes guardados, me parecio correcto que si podiamos guardarlo, posteriormente si lo queremos volver a modificar lo podamos cargar.
def cargar_archivo():
    global estudiantes
    global archivo
    try:
        #Abrimos el archivo en formato lectura.
        with open(archivo, 'r') as f:
            datos = json.load(f)
            if isinstance(datos, list):
                for alumno in datos:
                    #Utilizamos la funcion de validar los datos de alumnos, por si el archivo tiene algun dato que no corresponda con lo pedido (que la edad sea entero,etc)
                    if validar_datos_alumno(alumno):
                        estudiantes.append(alumno)
                print(Fore.GREEN + f"[+] {len(datos)} alumnos cargados desde el archivo.")
            else:
                print(Fore.RED + "[!] Error: El archivo no contiene una lista de estudiantes.")
    except FileNotFoundError:
        print(Fore.RED + f"[!] Error: El archivo {archivo} no fue encontrado. Cuando guardes el archivo se creara uno nuevo")
    except json.JSONDecodeError:
        print(Fore.RED + "[!] Error: El archivo no contiene un JSON valido.")
    except Exception as e:
        print(Fore.RED + f"[!] Ocurrio un error: {e}")
        
        
#Validamos los datos del alumno
def validar_datos_alumno(alumno):
    keys_esperadas = {"matricula", "nombre", "apellido", "provincia", "edad", "promedio"}
    if not all(key in alumno for key in keys_esperadas):
        print(Fore.RED + f"[!] Error: Datos incompletos en alumno: {alumno}")
        return False
    try:
        int(alumno["edad"])
        float(alumno["promedio"])
    except ValueError:
        print(Fore.RED + f"[!] Error: Datos inválidos en alumno: {alumno}")
        return False
    return True

def menu():
    while True:
        global archivo 
        archivo = input("Nombre del archivo (sin extension): ") + ".json"
        archivo = f"./{archivo}"
        try:
            cargar_archivo()
            break
        except FileNotFoundError:
            print(Fore.RED + f"[!] El archivo {archivo} no fue encontrado. Intente de nuevo.")
        except json.JSONDecodeError:
            print(Fore.RED + "[!] El archivo no contiene un JSON valido. Intente de nuevo.")
        except Exception as e:
            print(Fore.RED + f"[!] Ocurrio un error: {e}. Intente de nuevo.")

    while True:
            print(Fore.RESET +'''
                ------------- Menu interactivo -------------
                1- Agregar estudiante
                2- Buscar estudiante por matricula
                3- Listar todos los estudiantes
                4- Eliminar estudiante
                5- Listar todos los estudiantes aprobados
                6- Promedio de notas y edad de todos los estudiantes
                7- Guardar archivo
                8- Salir
                ---------------------------------------------''')
            opcion = int(input("¿Que opcion te gustaria elegir? -> "))
            if opcion == 1:
                cargar_estuadiante()
            if opcion == 2:
                matricula = input("Matricula que deseas buscar -> ")
                buscar_estudiante_matricula(matricula)
            if opcion == 3:
                listar_estudiantes()
            if opcion == 4:
                matricula = input("Matricula que deseas eliminar -> ")
                eliminar_estudiante(matricula)
            if opcion == 5:
                listar_estudiantes_aprobados()
            if opcion == 6:
                calcular_promedio()
            if opcion == 7:
                guardar_archivo()
            if opcion == 8:
                opcion = input("Sino guardaste el archivo se perdera todo lo que has cargado. ¿Seguro quieres salir del programa? [Si/No] -> ")
                opcion.lower()
                if opcion == "si":                 
                    print(Fore.RED + "[!] Saliendo del programa....")
                    break
                if opcion == "no":
                    continue
                    


if __name__ == "__main__":
    menu()