import json
import os
from datetime import datetime
from typing import List, Dict, Union

class BaseDeDatos:
    def __init__(self):
        #Inicializamos el sistema de archivos JSON
        self.directorio_datos = 'data'
        self.archivo_usuarios = os.path.join(self.directorio_datos, 'usuarios.json')
        self.archivo_animales = os.path.join(self.directorio_datos, 'animales.json')
        self.archivo_donaciones = os.path.join(self.directorio_datos, 'donaciones.json')
        self.archivo_articulos = os.path.join(self.directorio_datos, 'articulos.json')
        
        self._crear_directorio_si_no_existe()
        self._inicializar_archivos()

        for archivo in[self.archivo_usuarios, self.archivo_animales, self.archivo_donaciones, self.archivo_articulos]:
            if not os.path.exists(archivo):
                raise FileNotFoundError(f"El archivo {archivo} no existe. Por favor crea los archivos Json necesarios")

    def _crear_directorio_si_no_existe(self):
        #Creamos el directorio de datos si es que no existe
        if not os.path.exists(self.directorio_datos):
            os.makedirs(self.directorio_datos)

    def _inicializar_archivos(self):
        #Creamos los archivos JSON con estructura básica si no lleguaran a existir
        archivos = {
            self.archivo_usuarios: [],
            self.archivo_animales: [],
            self.archivo_donaciones: [],
            self.archivo_articulos: []
        }
        
        for archivo, datos_iniciales in archivos.items():
            if not os.path.exists(archivo):
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos_iniciales, f, indent=4)

    def _guardar_datos(self, archivo: str, datos: List[Dict]) -> bool:
        #Guardamos los datos en un archivo JSON
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar en {archivo}: {e}")
            return False

    def _cargar_datos(self, archivo: str) -> List[Dict]:
        #Carga datos desde un archivo JSON
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        except Exception as e:
            print(f"Error al cargar {archivo}: {e}")
            return []

    def _generar_id(self, datos_existentes: List[Dict]) -> int:
        #Generamos un nuevo ID basado en los datos existentes
        if not datos_existentes:
            return 1
        return max(item.get('id', 0) for item in datos_existentes) + 1

    def _obtener_fecha_actual(self) -> str:
        """Devuelve la fecha y hora actual formateada"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def registrar_usuario(self, nombre: str, edad: int, genero: str, rol: str, contrasena: str) -> Union[int, None]:
        #Hacemos Registrar un nuevo usuario o trabajador
        usuarios = self._cargar_datos(self.archivo_usuarios)
        
        nuevo_usuario = {
            'id': self._generar_id(usuarios),
            'nombre': nombre,
            'edad': edad,
            'genero': genero,
            'rol': rol.lower(),
            'contrasena': contrasena,
            'fecha_registro': self._obtener_fecha_actual(),
            'activo': True
        }
        
        usuarios.append(nuevo_usuario)
        if self._guardar_datos(self.archivo_usuarios, usuarios):
            return nuevo_usuario['id']
        return None

    def autenticar_usuario(self, nombre: str, contrasena: str) -> Union[Dict, None]:
        #Con esto Autentificara a un usuario y devuelve sus datos si los datos son correctas
        usuarios = self._cargar_datos(self.archivo_usuarios)
        
        for usuario in usuarios:
            if (usuario['nombre'].lower() == nombre.lower() and 
                usuario['contrasena'] == contrasena and 
                usuario.get('activo', True)):
                return usuario
        return None

    def obtener_usuarios_por_rol(self, rol: str) -> List[Dict]:
        #Obtiene todos los usuarios o trabajadores según su rol
        usuarios = self._cargar_datos(self.archivo_usuarios)
        return [u for u in usuarios if u['rol'] == rol.lower() and u.get('activo', True)]

    def obtener_todos_usuarios(self) -> List[Dict]:
        #Obtiene todos los usuarios incluyendo a los trabajadores
        return self._cargar_datos(self.archivo_usuarios)

    def registrar_animal(self, nombre: str, raza: str, tamano: float, genero: str) -> Union[int, None]:
        #Registra un nuevo animal en el sistema
        animales = self._cargar_datos(self.archivo_animales)
        
        nuevo_animal = {
            'id': self._generar_id(animales),
            'nombre': nombre,
            'raza': raza,
            'tamano': tamano,
            'genero': genero,
            'adoptado': False,
            'fecha_registro': self._obtener_fecha_actual(),
            'fecha_adopcion': None,
            'id_adoptante': None
        }
        
        animales.append(nuevo_animal)
        if self._guardar_datos(self.archivo_animales, animales):
            return nuevo_animal['id']
        return None

    def obtener_animales(self, adoptados: bool = False) -> List[Dict]:
        #Obtiene la lista de animales que son adoptados y los que estan en el albergue
        animales = self._cargar_datos(self.archivo_animales)
        return [a for a in animales if a['adoptado'] == adoptados]

    def adoptar_animal(self, id_animal: int, id_usuario: Union[int, None] = None) -> bool:
        #Marca un animal como adoptado
        animales = self._cargar_datos(self.archivo_animales)
        
        for animal in animales:
            if animal['id'] == id_animal and not animal['adoptado']:
                animal['adoptado'] = True
                animal['fecha_adopcion'] = self._obtener_fecha_actual()
                animal['id_adoptante'] = id_usuario
                return self._guardar_datos(self.archivo_animales, animales)
        return False

    def donar_dinero(self, cantidad: float, metodo_pago: str, id_donador: Union[int, None] = None) -> Union[int, None]:
        #Registra la donación de dinero que el usuario de
        donaciones = self._cargar_datos(self.archivo_donaciones)
        
        nueva_donacion = {
            'id': self._generar_id(donaciones),
            'cantidad': cantidad,
            'metodo_pago': metodo_pago,
            'fecha': self._obtener_fecha_actual(),
            'id_donador': id_donador
        }
        
        donaciones.append(nueva_donacion)
        if self._guardar_datos(self.archivo_donaciones, donaciones):
            return nueva_donacion['id']
        return None

    def obtener_donaciones_dinero(self) -> List[Dict]:
        #Obtiene todas las donaciones de dinero en resultado
        return self._cargar_datos(self.archivo_donaciones)

    def donar_articulos(self, nombre_producto: str, cantidad: int, tamano: str, id_donador: Union[int, None] = None) -> Union[int, None]:
        #Registra una donación de artículos
        articulos = self._cargar_datos(self.archivo_articulos)
        
        nuevo_articulo = {
            'id': self._generar_id(articulos),
            'nombre_producto': nombre_producto,
            'cantidad': cantidad,
            'tamano': tamano,
            'fecha': self._obtener_fecha_actual(),
            'id_donador': id_donador,
            'utilizado': False
        }
        
        articulos.append(nuevo_articulo)
        if self._guardar_datos(self.archivo_articulos, articulos):
            return nuevo_articulo['id']
        return None

    def obtener_articulos_almacen(self, utilizados: bool = False) -> List[Dict]:
        #Obtiene todos los artículos en el almacén
        articulos = self._cargar_datos(self.archivo_articulos)
        return [a for a in articulos if a['utilizado'] == utilizados]

    def marcar_articulo_utilizado(self, id_articulo: int) -> bool:
        #Marca un artículo como utilizado
        articulos = self._cargar_datos(self.archivo_articulos)
        
        for articulo in articulos:
            if articulo['id'] == id_articulo and not articulo['utilizado']:
                articulo['utilizado'] = True
                return self._guardar_datos(self.archivo_articulos, articulos)
        return False

    def obtener_estadisticas(self) -> Dict:
        #Devuelve estadísticas generales del sistema
        return {
            'total_usuarios': len([u for u in self._cargar_datos(self.archivo_usuarios) if u.get('activo', True)]),
            'total_trabajadores': len(self.obtener_usuarios_por_rol('trabajador')),
            'total_animales': len(self._cargar_datos(self.archivo_animales)),
            'animales_disponibles': len(self.obtener_animales(adoptados=False)),
            'animales_adoptados': len(self.obtener_animales(adoptados=True)),
            'total_donaciones': len(self._cargar_datos(self.archivo_donaciones)),
            'total_articulos': len(self._cargar_datos(self.archivo_articulos))
        }