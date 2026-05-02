import tkinter as tk
from tkinter import messagebox
from arbol_bst import ArbolBST

class InterfazArbol:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Visualizador de Árbol BST")
        self.ventana.geometry("1000x750")  # Le subimos un pelito al alto para que quepan los recorridos
        self.ventana.configure(bg="#f0f2f5")

        # Instancia de nuestro árbol binario de búsqueda
        self.arbol = ArbolBST()

        # Configuración para el diseño del dibujo
        self.radio_nodo = 20
        self.espacio_vertical = 60

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

        #       PANEL INFERIOR (RECORRIDOS)
        panel_recorridos = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief=tk.SOLID)
        panel_recorridos.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Botones para activar los recorridos
        btn_preorden = tk.Button(panel_recorridos, text="Preorden", font=("Arial", 9, "bold"), bg="#9b59b6", fg="white", width=10, command=self.mostrar_preorden)
        btn_preorden.pack(side=tk.LEFT, padx=10, pady=10)

        btn_inorden = tk.Button(panel_recorridos, text="Inorden", font=("Arial", 9, "bold"), bg="#34495e", fg="white", width=10, command=self.mostrar_inorden)
        btn_inorden.pack(side=tk.LEFT, padx=5, pady=10)

        btn_postorden = tk.Button(panel_recorridos, text="Postorden", font=("Arial", 9, "bold"), bg="#16a085", fg="white", width=10, command=self.mostrar_postorden)
        btn_postorden.pack(side=tk.LEFT, padx=5, pady=10)

        # Etiqueta donde se desplegará el resultado matemático
        self.lbl_resultado_recorrido = tk.Label(panel_recorridos, text="Resultado del recorrido: []", font=("Arial", 11, "italic"), bg="#ffffff", fg="#2c3e50")
        self.lbl_resultado_recorrido.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=10, anchor="w")

        #       ÁREA DE DIBUJO (CANVAS)
        self.canvas = tk.Canvas(self.ventana, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 0))

    #         LÓGICA DE DIBUJO RECURSIVO
    def actualizar_pantalla(self, camino_resaltado=[]):
        self.canvas.delete("all")
        if self.arbol.raiz is not None:
            ancho_pantalla = self.canvas.winfo_width()
            if ancho_pantalla <= 1:
                ancho_pantalla = 1000
            self._dibujar_nodo_recursivo(self.arbol.raiz, ancho_pantalla / 2, 40, ancho_pantalla / 4, camino_resaltado)

    def _dibujar_nodo_recursivo(self, nodo_actual, x, y, espacio_horizontal, camino_resaltado):
        if nodo_actual is None:
            return

        if nodo_actual.izquierdo is not None:
            x_hijo_izq = x - espacio_horizontal
            y_hijo_izq = y + self.espacio_vertical
            self.canvas.create_line(x, y, x_hijo_izq, y_hijo_izq, fill="#7f8c8d", width=2)
            self._dibujar_nodo_recursivo(nodo_actual.izquierdo, x_hijo_izq, y_hijo_izq, espacio_horizontal / 2, camino_resaltado)

        if nodo_actual.derecho is not None:
            x_hijo_der = x + espacio_horizontal
            y_hijo_der = y + self.espacio_vertical
            self.canvas.create_line(x, y, x_hijo_der, y_hijo_der, fill="#7f8c8d", width=2)
            self._dibujar_nodo_recursivo(nodo_actual.derecho, x_hijo_der, y_hijo_der, espacio_horizontal / 2, camino_resaltado)

        color_fondo = "#1abc9c"
        if nodo_actual.valor in camino_resaltado:
            color_fondo = "#f1c40f"

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
        self.lbl_resultado_recorrido.configure(text="Resultado del recorrido: []")
        messagebox.showinfo("Reiniciar", "El árbol ha sido vaciado.")

    #       FUNCIONES PARA RECORRIDOS VISUALES
    def mostrar_preorden(self):
        lista = self.arbol.obtener_preorden()
        self.lbl_resultado_recorrido.configure(text=f"Preorden (R-I-D): {lista}")

    def mostrar_inorden(self):
        lista = self.arbol.obtener_inorden()
        self.lbl_resultado_recorrido.configure(text=f"Inorden (I-R-D): {lista}")

    def mostrar_postorden(self):
        lista = self.arbol.obtener_postorden()
        self.lbl_resultado_recorrido.configure(text=f"Postorden (I-D-R): {lista}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazArbol(root)
    root.update()
    app.actualizar_pantalla()
    root.mainloop()