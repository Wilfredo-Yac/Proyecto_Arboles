import tkinter as tk
from tkinter import messagebox
from arbol_bst import ArbolBST

class InterfazArbol:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Visualizador Animado de Árbol BST")
        self.ventana.geometry("1000x750")
        self.ventana.configure(bg="#f0f2f5")

        self.arbol = ArbolBST()

        # Configuración del dibujo
        self.radio_nodo = 20
        self.espacio_vertical = 60
        self.velocidad_animacion = 800  # Tiempo en milisegundos entre cada paso (0.8 segundos)

        #       PANEL SUPERIOR (CONTROLES)
        panel_controles = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief=tk.SOLID)
        panel_controles.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(panel_controles, text="Valor:", font=("Arial", 12, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=10, pady=10)
        
        self.txt_valor = tk.Entry(panel_controles, font=("Arial", 12), width=10, bd=2, relief=tk.GROOVE)
        self.txt_valor.pack(side=tk.LEFT, padx=5, pady=10)
        self.txt_valor.focus()

        btn_insertar = tk.Button(panel_controles, text="Insertar", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", width=10, command=self.accion_insertar)
        btn_insertar.pack(side=tk.LEFT, padx=5, pady=10)

        btn_buscar = tk.Button(panel_controles, text="Buscar", font=("Arial", 10, "bold"), bg="#3498db", fg="white", width=10, command=self.accion_buscar)
        btn_buscar.pack(side=tk.LEFT, padx=5, pady=10)

        btn_limpiar = tk.Button(panel_controles, text="Reiniciar", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", width=10, command=self.accion_reiniciar)
        btn_limpiar.pack(side=tk.LEFT, padx=5, pady=10)

        # ==========================================
        #       PANEL INFERIOR (RECORRIDOS SIMULADOS)
        # ==========================================
        panel_recorridos = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief=tk.SOLID)
        panel_recorridos.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        btn_preorden = tk.Button(panel_recorridos, text="Simular Preorden", font=("Arial", 9, "bold"), bg="#9b59b6", fg="white", width=15, command=self.animar_preorden)
        btn_preorden.pack(side=tk.LEFT, padx=10, pady=10)

        btn_inorden = tk.Button(panel_recorridos, text="Simular Inorden", font=("Arial", 9, "bold"), bg="#34495e", fg="white", width=15, command=self.animar_inorden)
        btn_inorden.pack(side=tk.LEFT, padx=5, pady=10)

        btn_postorden = tk.Button(panel_recorridos, text="Simular Postorden", font=("Arial", 9, "bold"), bg="#16a085", fg="white", width=15, command=self.animar_postorden)
        btn_postorden.pack(side=tk.LEFT, padx=5, pady=10)

        self.lbl_resultado_recorrido = tk.Label(panel_recorridos, text="Explorando paso a paso: []", font=("Arial", 11, "italic"), bg="#ffffff", fg="#2c3e50")
        self.lbl_resultado_recorrido.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=10, anchor="w")

        #       ÁREA DE DIBUJO (CANVAS)
        self.canvas = tk.Canvas(self.ventana, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 0))

    #         LÓGICA DE DIBUJO RECURSIVO
    def actualizar_pantalla(self, camino_resaltado=[], nodo_actual_recorrido=None):
        self.canvas.delete("all")
        if self.arbol.raiz is not None:
            ancho_pantalla = self.canvas.winfo_width()
            if ancho_pantalla <= 1:
                ancho_pantalla = 1000
            self._dibujar_nodo_recursivo(self.arbol.raiz, ancho_pantalla / 2, 40, ancho_pantalla / 4, camino_resaltado, nodo_actual_recorrido)

    def _dibujar_nodo_recursivo(self, nodo_actual, x, y, espacio_horizontal, camino_resaltado, nodo_actual_recorrido):
        if nodo_actual is None:
            return

        # Dibujar líneas
        if nodo_actual.izquierdo is not None:
            x_hijo_izq = x - espacio_horizontal
            y_hijo_izq = y + self.espacio_vertical
            self.canvas.create_line(x, y, x_hijo_izq, y_hijo_izq, fill="#7f8c8d", width=2)
            self._dibujar_nodo_recursivo(nodo_actual.izquierdo, x_hijo_izq, y_hijo_izq, espacio_horizontal / 2, camino_resaltado, nodo_actual_recorrido)

        if nodo_actual.derecho is not None:
            x_hijo_der = x + espacio_horizontal
            y_hijo_der = y + self.espacio_vertical
            self.canvas.create_line(x, y, x_hijo_der, y_hijo_der, fill="#7f8c8d", width=2)
            self._dibujar_nodo_recursivo(nodo_actual.derecho, x_hijo_der, y_hijo_der, espacio_horizontal / 2, camino_resaltado, nodo_actual_recorrido)

        # Definir colores dinámicos
        color_fondo = "#1abc9c"  # Turquesa por defecto
        
        if nodo_actual.valor in camino_resaltado:
            color_fondo = "#2ecc71"  # Verde para los nodos ya procesados en la lista del recorrido
            
        if nodo_actual.valor == nodo_actual_recorrido:
            color_fondo = "#e67e22"  # Naranja encendido para el nodo que se está visitando JUSTO EN ESTE INSTANTE

        # Dibujar Círculo
        self.canvas.create_oval(
            x - self.radio_nodo, y - self.radio_nodo,
            x + self.radio_nodo, y + self.radio_nodo,
            fill=color_fondo, outline="#2c3e50", width=2
        )
        self.canvas.create_text(x, y, text=str(nodo_actual.valor), font=("Arial", 10, "bold"), fill="#ffffff")

    #           ACCIONES DE LOS BOTONES
    def accion_insertar(self):
        valor_str = self.txt_valor.get()
        if valor_str.isdigit():
            valor = int(valor_str)
            self.arbol.insertar(valor)
            self.actualizar_pantalla()
            self.txt_valor.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Por favor ingresa un número entero válido.")

    def accion_buscar(self):
        valor_str = self.txt_valor.get()
        if valor_str.isdigit():
            valor = int(valor_str)
            existe, camino = self.arbol.buscar(valor)
            if existe:
                self.actualizar_pantalla(camino_resaltado=camino)
                messagebox.showinfo("Búsqueda", f"¡El valor {valor} fue encontrado!\nRuta: {camino}")
            else:
                self.actualizar_pantalla()
                messagebox.showwarning("Búsqueda", f"El valor {valor} no se encuentra en el árbol.")
            self.txt_valor.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Por favor ingresa un número entero válido.")

    def accion_reiniciar(self):
        self.arbol = ArbolBST()
        self.canvas.delete("all")
        self.lbl_resultado_recorrido.configure(text="Explorando paso a paso: []")
        messagebox.showinfo("Reiniciar", "El árbol ha sido vaciado.")

    #       MOTOR DE ANIMACIÓN SECUENCIAL
    def animar_preorden(self):
        orden_visitas = self.arbol.obtener_preorden()
        self.ejecutar_paso_animacion(orden_visitas, 0, [], "Preorden (R-I-D)")

    def animar_inorden(self):
        orden_visitas = self.arbol.obtener_inorden()
        self.ejecutar_paso_animacion(orden_visitas, 0, [], "Inorden (I-R-D)")

    def animar_postorden(self):
        orden_visitas = self.arbol.obtener_postorden()
        self.ejecutar_paso_animacion(orden_visitas, 0, [], "Postorden (I-D-R)")

    def ejecutar_paso_animacion(self, lista_nodos, indice, procesados, nombre_recorrido):
        if indice < len(lista_nodos):
            nodo_actual = lista_nodos[indice]
            
            # Actualizamos la pantalla:
            # - 'procesados' se pintarán en verde (los que ya pasó)
            # - 'nodo_actual' se pintará en naranja (el que está visitando ahorita)
            self.actualizar_pantalla(camino_resaltado=procesados, nodo_actual_recorrido=nodo_actual)
            
            # Añadimos el nodo actual a la lista de completados para el siguiente frame
            procesados.append(nodo_actual)
            self.lbl_resultado_recorrido.configure(text=f"{nombre_recorrido}: {procesados}")
            
            # El truco mágico: Volver a llamar a esta función para el siguiente nodo después de X milisegundos
            self.ventana.after(self.velocidad_animacion, lambda: self.ejecutar_paso_animacion(lista_nodos, indice + 1, procesados, nombre_recorrido))
        else:
            # Al terminar la animación, dejamos todo el árbol pintado en verde de éxito
            self.actualizar_pantalla(camino_resaltado=procesados)
            messagebox.showinfo("Animación Finalizada", f"Se completó la simulación del recorrido {nombre_recorrido}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazArbol(root)
    root.update()
    app.actualizar_pantalla()
    root.mainloop()