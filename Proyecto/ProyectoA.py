import tkinter as tk
from tkinter import ttk, messagebox
from ProyectoB import BaseDeDatos
from datetime import datetime

class AplicacionAlbergueAnimal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Albergue Animal")
        self.root.geometry("1000x700")
        self.db = BaseDeDatos()
        
        #Como se vera la interfaz
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f0e7e7")
        self.style.configure('TButton', padding=5, font=('Arial', 10))
        self.style.configure('TLabel', background="#d9a5a5", font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        self.usuario_actual = None
        self.crear_pantalla_inicio()

    def crear_pantalla_inicio(self):
        """Pantalla de inicio de sesión/registro"""
        self.limpiar_ventana()
        
        marco = ttk.Frame(self.root)
        marco.pack(pady=50)
        
        ttk.Label(marco, text="Bienvenido al Albergue Animal", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos que se requieren del registro
        campos = [
            ("Nombre:", "nombre"),
            ("Edad:", "edad"),
            ("Género:", "genero", ["Masculino", "Femenino", "Otro"]),
            ("Rol:", "rol", ["Usuario", "Trabajador"]),
            ("Contraseña:", "contrasena")
        ]
        
        for i, campo in enumerate(campos, start=1):
            ttk.Label(marco, text=campo[0]).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            
            if len(campo) == 2:
                entrada = ttk.Entry(marco)
                if campo[1] == "contrasena":
                    entrada.config(show="*")
                setattr(self, f"entrada_{campo[1]}", entrada)
            else:
                combo = ttk.Combobox(marco, values=campo[2])
                combo.grid(row=i, column=1, padx=5, pady=5)
                setattr(self, f"combo_{campo[1]}", combo)
                
                if campo[1] == "rol":
                    combo.bind("<<ComboboxSelected>>", self.actualizar_campo_contrasena)
            
            if len(campo) == 2:
                entrada.grid(row=i, column=1, padx=5, pady=5)
        
        # Botones para registrarse o iniciar sesion
        ttk.Button(marco, text="Registrarse", 
                  command=self.registrar_usuario).grid(row=len(campos)+1, column=0, columnspan=2, pady=10)
        ttk.Button(marco, text="Iniciar Sesión", 
                  command=self.iniciar_sesion).grid(row=len(campos)+2, column=0, columnspan=2, pady=10)

    def actualizar_campo_contrasena(self, event):
        """Actualiza el campo de contraseña según el rol"""
        rol = self.combo_rol.get()
        self.entrada_contrasena.delete(0, tk.END)
        self.entrada_contrasena.insert(0, "12345" if rol == "Usuario" else "abcdefgh")

    def crear_panel_usuario(self):
        #Este es el panel principal para los usuarios
        self.limpiar_ventana()
        
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        ttk.Label(marco, text=f"Bienvenido, {self.usuario_actual['nombre']}", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        botones = [
            ("Registrar Animal", self.crear_registro_animal),
            ("Donar Dinero", self.crear_donacion_dinero),
            ("Donar Artículos", self.crear_donacion_articulos),
            ("Ver Animales", self.mostrar_animales),
            ("Adoptar Animal", self.crear_ventana_adopcion),
            ("Cerrar Sesión", self.crear_pantalla_inicio)
        ]
        
        for i, (texto, comando) in enumerate(botones, start=1):
            ttk.Button(marco, text=texto, command=comando).grid(
                row=i, column=0 if i % 2 == 1 else 1, 
                padx=10, pady=10, sticky="nsew")

    def crear_panel_trabajador(self):
        #Panel principal para trabajadores
        self.limpiar_ventana()
        
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        ttk.Label(marco, text=f"Bienvenido, Trabajador {self.usuario_actual['nombre']}", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Con esto se mostrara las estadísticas de los animales adoptados y animales sin adoptar
        stats = self.db.obtener_estadisticas()
        ttk.Label(marco, text=f"Animales: {stats['animales_disponibles']} disponibles, {stats['animales_adoptados']} adoptados",
                 style='Header.TLabel').grid(row=1, column=0, columnspan=3, pady=5)
        
        botones = [
            ("Gestión de Almacén", self.gestionar_almacen),
            ("Lista de Animales", self.mostrar_animales),
            ("Animales Adoptados", lambda: self.mostrar_animales(adoptados=True)),
            ("Gestión de Donaciones", self.gestionar_donaciones),
            ("Ver Usuarios", lambda: self.mostrar_personas(rol="usuario")),
            ("Ver Trabajadores", lambda: self.mostrar_personas(rol="trabajador")),
            ("Registrar Animal", self.crear_registro_animal),
            ("Cerrar Sesión", self.crear_pantalla_inicio)
        ]
        
        for i, (texto, comando) in enumerate(botones, start=2):
            ttk.Button(marco, text=texto, command=comando).grid(
                row=i, column=i % 3, 
                padx=5, pady=10, sticky="nsew")

    def crear_registro_animal(self):
        #Ventana para registrar animales
        self.limpiar_ventana()
        
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        ttk.Label(marco, text="Registrar Animal", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        campos = [
            ("Nombre del animal:", "nombre_animal"),
            ("Raza:", "raza_animal"),
            ("Tamaño (cm):", "tamano_animal"),
            ("Género:", "genero_animal", ["Macho", "Hembra", "Desconocido"])
        ]
        
        for i, campo in enumerate(campos, start=1):
            ttk.Label(marco, text=campo[0]).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            
            if len(campo) == 2:
                entrada = ttk.Entry(marco)
                entrada.grid(row=i, column=1, padx=5, pady=5)
                setattr(self, f"entrada_{campo[1]}", entrada)
            else:
                combo = ttk.Combobox(marco, values=campo[2])
                combo.grid(row=i, column=1, padx=5, pady=5)
                setattr(self, f"combo_{campo[1]}", combo)
        
        ttk.Button(marco, text="Registrar", 
                  command=self.registrar_animal).grid(row=len(campos)+1, column=0, pady=10)
        ttk.Button(marco, text="Cancelar", 
                  command=self.crear_panel_segun_rol).grid(row=len(campos)+1, column=1, pady=10)

    def mostrar_animales(self, adoptados=False):
        #Muestra lista de animales tanto disponibles como adoptados
        animales = self.db.obtener_animales(adoptados)
        
        self.limpiar_ventana()
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        titulo = "Animales Adoptados" if adoptados else "Animales Disponibles"
        ttk.Label(marco, text=titulo, font=('Arial', 14)).grid(row=0, column=0, columnspan=5, pady=10)
        
        if not animales:
            ttk.Label(marco, text="No hay animales registrados").grid(row=1, column=0, columnspan=5)
        else:
            # Encabezados que se mostraran por arriba
            encabezados = ["ID", "Nombre", "Raza", "Tamaño", "Género", "Fecha Registro"]
            for i, encabezado in enumerate(encabezados):
                ttk.Label(marco, text=encabezado, style='Header.TLabel').grid(row=1, column=i, padx=5)
            
            # Datos
            for i, animal in enumerate(animales, start=2):
                ttk.Label(marco, text=animal['id']).grid(row=i, column=0, padx=5, pady=2)
                ttk.Label(marco, text=animal['nombre']).grid(row=i, column=1, padx=5, pady=2)
                ttk.Label(marco, text=animal['raza']).grid(row=i, column=2, padx=5, pady=2)
                ttk.Label(marco, text=animal['tamano']).grid(row=i, column=3, padx=5, pady=2)
                ttk.Label(marco, text=animal['genero']).grid(row=i, column=4, padx=5, pady=2)
                ttk.Label(marco, text=animal['fecha_registro']).grid(row=i, column=5, padx=5, pady=2)
                
                if self.usuario_actual['rol'] == 'trabajador' and not adoptados:
                    ttk.Button(marco, text="Adoptado", 
                              command=lambda id=animal['id']: self.marcar_adoptado(id)).grid(row=i, column=6, padx=5)
                elif self.usuario_actual['rol'] == 'usuario' and not adoptados:
                    ttk.Button(marco, text="Adoptar", 
                              command=lambda id=animal['id']: self.procesar_adopcion(id)).grid(row=i, column=6, padx=5)
        
        # Botón para regresar a la ventana anterior
        ttk.Button(marco, text="Regresar", 
                  command=self.crear_panel_segun_rol).grid(
                      row=len(animales)+3 if animales else 2, 
                      column=0, columnspan=7, pady=10)

    def crear_ventana_adopcion(self):
        #Ventana especializada para adopción de animales
        self.mostrar_animales(adoptados=False)

    def crear_donacion_dinero(self):
        #Ventana para donaciones monetarias
        self.limpiar_ventana()
        
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        ttk.Label(marco, text="Donar Dinero", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        campos = [
            ("Cantidad:", "cantidad_donacion"),
            ("Método de pago:", "metodo_pago", ["Efectivo", "Tarjeta", "Transferencia"])
        ]
        
        for i, campo in enumerate(campos, start=1):
            ttk.Label(marco, text=campo[0]).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            
            if len(campo) == 2:
                entrada = ttk.Entry(marco)
                entrada.grid(row=i, column=1, padx=5, pady=5)
                setattr(self, f"entrada_{campo[1]}", entrada)
            else:
                combo = ttk.Combobox(marco, values=campo[2])
                combo.grid(row=i, column=1, padx=5, pady=5)
                setattr(self, f"combo_{campo[1]}", combo)
        
        ttk.Button(marco, text="Donar", 
                  command=self.procesar_donacion).grid(row=len(campos)+1, column=0, pady=10)
        ttk.Button(marco, text="Cancelar", 
                  command=self.crear_panel_segun_rol).grid(row=len(campo)+1, column=1, pady=10)

    def gestionar_donaciones(self):
        #Muestra el historial de donaciones solo para que los trabajadores vean
        donaciones = self.db.obtener_donaciones_dinero()
        total = sum(d['cantidad'] for d in donaciones)
        
        self.limpiar_ventana()
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        ttk.Label(marco, text="Gestión de Donaciones", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=4, pady=10)
        ttk.Label(marco, text=f"Total recaudado: ${total:,.2f}", 
                 style='Header.TLabel').grid(row=1, column=0, columnspan=4)
        
        if not donaciones:
            ttk.Label(marco, text="No hay donaciones registradas").grid(row=2, column=0, columnspan=4)
        else:
            # Encabezados que se msotraran
            encabezados = ["ID", "Cantidad", "Método", "Fecha", "Donador"]
            for i, encabezado in enumerate(encabezados):
                ttk.Label(marco, text=encabezado, style='Header.TLabel').grid(row=2, column=i, padx=5)
            
            # Datos de cantidad, nombre id
            for i, donacion in enumerate(donaciones, start=3):
                ttk.Label(marco, text=donacion['id']).grid(row=i, column=0, padx=5, pady=2)
                ttk.Label(marco, text=f"${donacion['cantidad']:,.2f}").grid(row=i, column=1, padx=5, pady=2)
                ttk.Label(marco, text=donacion['metodo_pago']).grid(row=i, column=2, padx=5, pady=2)
                ttk.Label(marco, text=donacion['fecha']).grid(row=i, column=3, padx=5, pady=2)
                ttk.Label(marco, text=donacion.get('id_donador', 'Anónimo')).grid(row=i, column=4, padx=5, pady=2)
        
        ttk.Button(marco, text="Regresar", 
                  command=self.crear_panel_trabajador).grid(
                      row=len(donaciones)+4 if donaciones else 3, 
                      column=0, columnspan=4, pady=10)

    def crear_donacion_articulos(self):
        #Ventana para donación de artículos
        self.limpiar_ventana()
        
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        ttk.Label(marco, text="Donar Artículos", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        campos = [
            ("Nombre del producto:", "nombre_articulo"),
            ("Cantidad:", "cantidad_articulo"),
            ("Tamaño:", "tamano_articulo")
        ]
        
        for i, campo in enumerate(campos, start=1):
            ttk.Label(marco, text=campo[0]).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            entrada = ttk.Entry(marco)
            entrada.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, f"entrada_{campo[1]}", entrada)
        
        ttk.Button(marco, text="Donar", 
                  command=self.procesar_donacion_articulos).grid(row=len(campos)+1, column=0, pady=10)
        ttk.Button(marco, text="Cancelar", 
                  command=self.crear_panel_segun_rol).grid(row=len(campos)+1, column=1, pady=10)

    def gestionar_almacen(self):
        #Muestra el inventario del almacén para que solo los trabajadores puedan ver
        articulos = self.db.obtener_articulos_almacen()
        
        self.limpiar_ventana()
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        ttk.Label(marco, text="Gestión de Almacén", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=6, pady=10)
        
        if not articulos:
            ttk.Label(marco, text="El almacén está vacío").grid(row=1, column=0, columnspan=6)
        else:
            # Encabezados que se veran arriba
            encabezados = ["ID", "Producto", "Cantidad", "Tamaño", "Fecha", "Donador"]
            for i, encabezado in enumerate(encabezados):
                ttk.Label(marco, text=encabezado, style='Header.TLabel').grid(row=1, column=i, padx=5)
            
            # Datos de quien dio el producto o articulo
            for i, articulo in enumerate(articulos, start=2):
                ttk.Label(marco, text=articulo['id']).grid(row=i, column=0, padx=5, pady=2)
                ttk.Label(marco, text=articulo['nombre_producto']).grid(row=i, column=1, padx=5, pady=2)
                ttk.Label(marco, text=articulo['cantidad']).grid(row=i, column=2, padx=5, pady=2)
                ttk.Label(marco, text=articulo['tamano']).grid(row=i, column=3, padx=5, pady=2)
                ttk.Label(marco, text=articulo['fecha']).grid(row=i, column=4, padx=5, pady=2)
                ttk.Label(marco, text=articulo.get('id_donador', 'Anónimo')).grid(row=i, column=5, padx=5, pady=2)
                
                if not articulo['utilizado']:
                    ttk.Button(marco, text="Marcar como usado", 
                              command=lambda id=articulo['id']: self.marcar_articulo_usado(id)).grid(row=i, column=6, padx=5)
        
        ttk.Button(marco, text="Regresar", 
                  command=self.crear_panel_trabajador).grid(
                      row=len(articulos)+3 if articulos else 2, 
                      column=0, columnspan=6, pady=10)

    def mostrar_personas(self, rol):
        #Muestra lista de usuarios o trabajadores
        personas = self.db.obtener_usuarios_por_rol(rol)
        titulo = "Usuarios" if rol == "usuario" else "Trabajadores"
        
        self.limpiar_ventana()
        marco = ttk.Frame(self.root)
        marco.pack(pady=20)
        
        ttk.Label(marco, text=f"Lista de {titulo}", 
                 font=('Arial', 14)).grid(row=0, column=0, columnspan=6, pady=10)
        
        if not personas:
            ttk.Label(marco, text=f"No hay {titulo.lower()} registrados").grid(row=1, column=0, columnspan=6)
        else:
            # Encabezados tanto trabajadores como usuarios
            encabezados = ["ID", "Nombre", "Edad", "Género", "Rol", "Fecha Registro"]
            for i, encabezado in enumerate(encabezados):
                ttk.Label(marco, text=encabezado, style='Header.TLabel').grid(row=1, column=i, padx=5)
            
            # Datos del usuario o trabajador
            for i, persona in enumerate(personas, start=2):
                ttk.Label(marco, text=persona['id']).grid(row=i, column=0, padx=5, pady=2)
                ttk.Label(marco, text=persona['nombre']).grid(row=i, column=1, padx=5, pady=2)
                ttk.Label(marco, text=persona['edad']).grid(row=i, column=2, padx=5, pady=2)
                ttk.Label(marco, text=persona['genero']).grid(row=i, column=3, padx=5, pady=2)
                ttk.Label(marco, text=persona['rol'].capitalize()).grid(row=i, column=4, padx=5, pady=2)
                ttk.Label(marco, text=persona['fecha_registro']).grid(row=i, column=5, padx=5, pady=2)
        
        ttk.Button(marco, text="Regresar", 
                  command=self.crear_panel_trabajador).grid(
                      row=len(personas)+3 if personas else 2, 
                      column=0, columnspan=6, pady=10)

    def registrar_usuario(self):
        #Registra un nuevo usuario en el sistema
        campos = {
            'nombre': self.entrada_nombre.get(),
            'edad': self.entrada_edad.get(),
            'genero': self.combo_genero.get(),
            'rol': self.combo_rol.get(),
            'contrasena': self.entrada_contrasena.get()
        }
        
        if not all(campos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            campos['edad'] = int(campos['edad'])
            
            if (campos['rol'] == "Trabajador" and len(campos['contrasena']) != 8) or \
               (campos['rol'] == "Usuario" and len(campos['contrasena']) != 5):
                raise ValueError("La contraseña no cumple con los requisitos")
            
            id_usuario = self.db.registrar_usuario(**campos)
            if id_usuario:
                messagebox.showinfo("Éxito", "Registro completado correctamente")
                self.crear_pantalla_inicio()
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {e}")

    def iniciar_sesion(self):
        #Inicia sesión con las credenciales proporcionadas
        nombre = self.entrada_nombre.get()
        contrasena = self.entrada_contrasena.get()
        
        if not nombre or not contrasena:
            messagebox.showerror("Error", "Nombre y contraseña son obligatorios")
            return
        
        usuario = self.db.autenticar_usuario(nombre, contrasena)
        if usuario:
            self.usuario_actual = usuario
            if usuario['rol'] == 'trabajador':
                self.crear_panel_trabajador()
            else:
                self.crear_panel_usuario()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def registrar_animal(self):
        #Registra un nuevo animal en el sistema
        campos = {
            'nombre': self.entrada_nombre_animal.get(),
            'raza': self.entrada_raza_animal.get(),
            'tamano': self.entrada_tamano_animal.get(),
            'genero': self.combo_genero_animal.get()
        }
        
        if not all(campos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            campos['tamano'] = float(campos['tamano'])
            id_animal = self.db.registrar_animal(**campos)
            if id_animal:
                messagebox.showinfo("Éxito", "Animal registrado correctamente")
                self.crear_panel_segun_rol()
        except ValueError:
            messagebox.showerror("Error", "El tamaño debe ser un número")

    def procesar_adopcion(self, id_animal):
        #Procesa la adopción de un animal
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea adoptar este animal?"):
            if self.db.adoptar_animal(id_animal, self.usuario_actual['id']):
                messagebox.showinfo("Éxito", "¡Felicidades por su nueva mascota!")
                self.crear_ventana_adopcion()

    def marcar_adoptado(self, id_animal):
        #Marca un animal como adoptado solo para trabajadores
        if messagebox.askyesno("Confirmar", "¿Marcar este animal como adoptado?"):
            if self.db.adoptar_animal(id_animal):
                messagebox.showinfo("Éxito", "Animal marcado como adoptado")
                self.mostrar_animales()

    def procesar_donacion(self):
        #Procesa una donación monetaria
        campos = {
            'cantidad': self.entrada_cantidad_donacion.get(),
            'metodo_pago': self.combo_metodo_pago.get(),
            'id_donador': self.usuario_actual['id']
        }
        
        if not all(campos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            campos['cantidad'] = float(campos['cantidad'])
            if campos['cantidad'] <= 0:
                raise ValueError("La cantidad debe ser positiva")
            
            id_donacion = self.db.donar_dinero(**campos)
            if id_donacion:
                messagebox.showinfo("Éxito", "¡Gracias por su donación!")
                self.crear_panel_segun_rol()
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {e}")

    def procesar_donacion_articulos(self):
        #Procesa una donación de artículos
        campos = {
            'nombre_producto': self.entrada_nombre_articulo.get(),
            'cantidad': self.entrada_cantidad_articulo.get(),
            'tamano': self.entrada_tamano_articulo.get(),
            'id_donador': self.usuario_actual['id']
        }
        
        if not all(campos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            campos['cantidad'] = int(campos['cantidad'])
            if campos['cantidad'] <= 0:
                raise ValueError("La cantidad debe ser positiva")
            
            id_articulo = self.db.donar_articulos(**campos)
            if id_articulo:
                messagebox.showinfo("Éxito", "¡Gracias por su donación!")
                self.crear_panel_segun_rol()
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {e}")

    def marcar_articulo_usado(self, id_articulo):
        #Marca un artículo como usado solo para trabajadores
        if messagebox.askyesno("Confirmar", "¿Marcar este artículo como utilizado?"):
            if self.db.marcar_articulo_utilizado(id_articulo):
                messagebox.showinfo("Éxito", "Artículo marcado como utilizado")
                self.gestionar_almacen()

    
    def crear_panel_segun_rol(self):
        #Redirige al panel según el rol del usuario
        if self.usuario_actual['rol'] == 'trabajador':
            self.crear_panel_trabajador()
        else:
            self.crear_panel_usuario()

    def limpiar_ventana(self):
        #Limpia todos los widgets de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionAlbergueAnimal(root)
    root.mainloop()