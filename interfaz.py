import tkinter as tk
from tkinter import messagebox
from arbol_bst import ArbolBST

class InterfazArbol:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Simulador Educativo AVL/ABB con Flujo de Flechas")
        self.ventana.geometry("1150x780")
        self.ventana.configure(bg="#f0f2f5")

        self.arbol = ArbolBST()
        self.modo_actual = "avl"  # 'avl' o 'bst'

        self.radio_nodo = 20
        self.espacio_vertical = 60
        self.velocidad_animacion = 900  # Un pelito más lento para apreciar el flujo de las flechas

        # Diccionario para almacenar las coordenadas X, Y de cada nodo de forma dinámica
        self.coordenadas_nodos = {}

        # ==========================================
        #       PANEL SUPERIOR (CONTROLES)
        # ==========================================
        panel_controles = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief=tk.SOLID)
        panel_controles.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(panel_controles, text="Valor:", font=("Arial", 12, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=10, pady=10)
        self.txt_valor = tk.Entry(panel_controles, font=("Arial", 12), width=8, bd=2, relief=tk.GROOVE)
        self.txt_valor.pack(side=tk.LEFT, padx=5, pady=10)
        self.txt_valor.focus()

        tk.Button(panel_controles, text="Insertar", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", width=9, command=self.accion_insertar).pack(side=tk.LEFT, padx=3)
        tk.Button(panel_controles, text="Buscar", font=("Arial", 10, "bold"), bg="#3498db", fg="white", width=9, command=self.accion_buscar).pack(side=tk.LEFT, padx=3)
        tk.Button(panel_controles, text="Reiniciar", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", width=9, command=self.accion_reiniciar).pack(side=tk.LEFT, padx=3)

        # ==========================================
        #    PANEL INTERACTIVO: SELECCIÓN DE ÁRBOL
        # ==========================================
        panel_modos = tk.LabelFrame(panel_controles, text=" Modo de Visualización ", font=("Arial", 9, "bold"), bg="#ffffff", fg="#2c3e50")
        panel_modos.pack(side=tk.RIGHT, padx=15, pady=5)

        self.btn_ver_bst = tk.Button(panel_modos, text="Ver como ABB (Normal)", font=("Arial", 9, "bold"), bg="#95a5a6", fg="white", command=lambda: self.cambiar_modo("bst"))
        self.btn_ver_bst.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_ver_avl = tk.Button(panel_modos, text="Ver como AVL (Equilibrado)", font=("Arial", 9, "bold"), bg="#2c3e50", fg="white", command=lambda: self.cambiar_modo("avl"))
        self.btn_ver_avl.pack(side=tk.LEFT, padx=5, pady=5)

        # ==========================================
        #       MONITOR DE NOTIFICACIÓN AVL
        # ==========================================
        self.panel_status = tk.Frame(self.ventana, bg="#34495e")
        self.panel_status.pack(side=tk.TOP, fill=tk.X, padx=10, pady=2)
        
        self.lbl_rotacion = tk.Label(self.panel_status, text="Estado de Rotaciones AVL: Ninguna rotación requerida aún.", font=("Arial", 11, "bold"), bg="#34495e", fg="#f1c40f")
        self.lbl_rotacion.pack(pady=5)

        # ==========================================
        #       PANEL INFERIOR (RECORRIDOS)
        # ==========================================
        panel_recorridos = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief=tk.SOLID)
        panel_recorridos.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        tk.Button(panel_recorridos, text="Simular Preorden", font=("Arial", 9, "bold"), bg="#9b59b6", fg="white", width=14, command=self.animar_preorden).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(panel_recorridos, text="Simular Inorden", font=("Arial", 9, "bold"), bg="#1abc9c", fg="white", width=14, command=self.animar_inorden).pack(side=tk.LEFT, padx=5, pady=10)
        tk.Button(panel_recorridos, text="Simular Postorden", font=("Arial", 9, "bold"), bg="#16a085", fg="white", width=14, command=self.animar_postorden).pack(side=tk.LEFT, padx=5, pady=10)

        self.lbl_resultado_recorrido = tk.Label(panel_recorridos, text="Flujo del recorrido paso a paso: []", font=("Arial", 11, "italic"), bg="#ffffff", fg="#2c3e50")
        self.lbl_resultado_recorrido.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=10, anchor="w")

        # ==========================================
        #       ÁREA DE DIBUJO (CANVAS)
        # ==========================================
        self.canvas = tk.Canvas(self.ventana, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(5, 0))

    def cambiar_modo(self, nuevo_modo):
        self.modo_actual = nuevo_modo
        if nuevo_modo == "bst":
            self.btn_ver_bst.configure(bg="#d35400")
            self.btn_ver_avl.configure(bg="#95a5a6")
        else:
            self.btn_ver_avl.configure(bg="#2c3e50")
            self.btn_ver_bst.configure(bg="#95a5a6")
        self.actualizar_pantalla()

    def actualizar_pantalla(self, camino_secuencia=[], nodo_actual_recorrido=None):
        self.canvas.delete("all")
        self.coordenadas_nodos.clear()  # Limpiamos el mapa de coordenadas antes de redibujar
        
        raiz_a_pintar = self.arbol.raiz_avl if self.modo_actual == "avl" else self.arbol.raiz_bst
        
        if raiz_a_pintar is not None:
            ancho_pantalla = self.canvas.winfo_width()
            if ancho_pantalla <= 1: ancho_pantalla = 1150
            
            # Primero: Dibujamos la estructura estática del árbol y mapeamos las coordenadas
            self._mapear_y_dibujar_estructura(raiz_a_pintar, ancho_pantalla / 2, 40, ancho_pantalla / 4)
            
            # Segundo: Dibujamos las flechas direccionales si hay una secuencia activa de animación/búsqueda
            self._dibujar_flechas_flujo(camino_secuencia, nodo_actual_recorrido)

    def _mapear_y_dibujar_estructura(self, nodo_actual, x, y, espacio_horizontal):
        if nodo_actual is None: return

        # Guardar las coordenadas del nodo para el motor de flechas externo
        self.coordenadas_nodos[nodo_actual.valor] = (x, y)

        # Dibujar líneas base de conexiones estructurales (gris claro de fondo)
        if nodo_actual.izquierdo is not None:
            x_hijo_izq = x - espacio_horizontal
            y_hijo_izq = y + self.espacio_vertical
            self.canvas.create_line(x, y, x_hijo_izq, y_hijo_izq, fill="#e2e8f0", width=2)
            self._mapear_y_dibujar_estructura(nodo_actual.izquierdo, x_hijo_izq, y_hijo_izq, espacio_horizontal / 2)

        if nodo_actual.derecho is not None:
            x_hijo_der = x + espacio_horizontal
            y_hijo_der = y + self.espacio_vertical
            self.canvas.create_line(x, y, x_hijo_der, y_hijo_der, fill="#e2e8f0", width=2)
            self._mapear_y_dibujar_estructura(nodo_actual.derecho, x_hijo_der, y_hijo_der, espacio_horizontal / 2)

        # Dibujar el círculo estático del nodo
        color_nodo = "#34495e" if self.modo_actual == "bst" else "#1abc9c"
        self.canvas.create_oval(x - self.radio_nodo, y - self.radio_nodo, x + self.radio_nodo, y + self.radio_nodo, fill=color_nodo, outline="#2c3e50", width=2)
        self.canvas.create_text(x, y, text=str(nodo_actual.valor), font=("Arial", 10, "bold"), fill="#ffffff")

    def _dibujar_flechas_flujo(self, camino_secuencia, nodo_actual_recorrido):
        # Dibujar las flechas consecutivas que conectan los nodos en el orden exacto de visita
        for i in range(len(camino_secuencia) - 1):
            val_origen = camino_secuencia[i]
            val_destino = camino_secuencia[i+1]
            
            if val_origen in self.coordenadas_nodos and val_destino in self.coordenadas_nodos:
                x_orig, y_orig = self.coordenadas_nodos[val_origen]
                x_dest, y_dest = self.coordenadas_nodos[val_destino]
                
                # Dibujamos una flecha curva o directa gruesa de color azul/púrpura indicando la traza
                self.canvas.create_line(x_orig, y_orig, x_dest, y_dest, fill="#e67e22", width=3, arrow=tk.LAST, arrowshape=(12, 14, 5))

        # Si hay un nodo que se está procesando en este instante, lo pintamos de un color de alerta
        if nodo_actual_recorrido in self.coordenadas_nodos:
            x, y = self.coordenadas_nodos[nodo_actual_recorrido]
            self.canvas.create_oval(x - self.radio_nodo, y - self.radio_nodo, x + self.radio_nodo, y + self.radio_nodo, fill="#f1c40f", outline="#d35400", width=3)
            self.canvas.create_text(x, y, text=str(nodo_actual_recorrido), font=("Arial", 10, "bold"), fill="#2c3e50")

    def accion_insertar(self):
        valor_str = self.txt_valor.get()
        if valor_str.isdigit():
            valor = int(valor_str)
            self.arbol.insertar(valor)
            self.lbl_rotacion.configure(text=f"Estado de Rotaciones AVL: {self.arbol.ultima_rotacion}")
            self.actualizar_pantalla()
            self.txt_valor.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Ingresa un número entero.")

    def accion_buscar(self):
        valor_str = self.txt_valor.get()
        if valor_str.isdigit():
            valor = int(valor_str)
            existe, camino = self.arbol.buscar(valor, modo=self.modo_actual)
            if existe:
                # La búsqueda dibuja flechas sobre el camino que recorrió el puntero
                self.actualizar_pantalla(camino_secuencia=camino, nodo_actual_recorrido=valor)
            else:
                messagebox.showwarning("Búsqueda", f"El valor {valor} no está en este modo.")
            self.txt_valor.delete(0, tk.END)

    def accion_reiniciar(self):
        self.arbol.reiniciar_estructuras()
        self.canvas.delete("all")
        self.lbl_rotacion.configure(text="Estado de Rotaciones AVL: Ninguna rotación requerida aún.")
        self.lbl_resultado_recorrido.configure(text="Flujo del recorrido paso a paso: []")

    def animar_preorden(self):
        orden_visitas = self.arbol.obtener_preorden(modo=self.modo_actual)
        self.ejecutar_paso_animacion(orden_visitas, 0, [], f"Preorden {self.modo_actual.upper()}")

    def animar_inorden(self):
        orden_visitas = self.arbol.obtener_inorden(modo=self.modo_actual)
        self.ejecutar_paso_animacion(orden_visitas, 0, [], f"Inorden {self.modo_actual.upper()}")

    def animar_postorden(self):
        orden_visitas = self.arbol.obtener_postorden(modo=self.modo_actual)
        self.ejecutar_paso_animacion(orden_visitas, 0, [], f"Postorden {self.modo_actual.upper()}")

    def ejecutar_paso_animacion(self, lista_nodos, indice, visitados, nombre_recorrido):
        if indice < len(lista_nodos):
            nodo_actual = lista_nodos[indice]
            
            # Agregamos el nodo a la secuencia temporal de la traza para pintar las flechas
            visitados.append(nodo_actual)
            
            # Actualizamos la pantalla pasando la lista completa de secuencia para las flechas
            self.actualizar_pantalla(camino_secuencia=visitados, nodo_actual_recorrido=nodo_actual)
            
            self.lbl_resultado_recorrido.configure(text=f"{nombre_recorrido}: {visitados}")
            
            self.ventana.after(self.velocidad_animacion, lambda: self.ejecutar_paso_animacion(lista_nodos, indice + 1, visitados, nombre_recorrido))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazArbol(root)
    root.update()
    app.actualizar_pantalla()
    root.mainloop()