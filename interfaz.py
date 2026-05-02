import tkinter as tk
from tkinter import messagebox
from arbol_bst import ArbolBST

class InterfazArbol:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Visualizador de Árbol BST")
        self.ventana.geometry("1000x700")
        self.ventana.configure(bg="#f0f2f5")

        # Instancia de nuestro árbol binario de búsqueda
        self.arbol = ArbolBST()

        #       PANEL SUPERIOR (CONTROLES)
        panel_controles = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief=tk.SOLID)
        panel_controles.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Etiqueta y Entrada de texto para el número
        tk.Label(panel_controles, text="Valor:", font=("Arial", 12, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=10, pady=10)
        
        self.txt_valor = tk.Entry(panel_controles, font=("Arial", 12), width=10, bd=2, relief=tk.GROOVE)
        self.txt_valor.pack(side=tk.LEFT, padx=5, pady=10)
        self.txt_valor.focus()

        # Botones de Acción
        btn_insertar = tk.Button(panel_controles, text="Insertar", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", width=10, command=self.accion_insertar)
        btn_insertar.pack(side=tk.LEFT, padx=5, pady=10)

        btn_buscar = tk.Button(panel_controles, text="Buscar", font=("Arial", 10, "bold"), bg="#3498db", fg="white", width=10, command=self.accion_buscar)
        btn_buscar.pack(side=tk.LEFT, padx=5, pady=10)

        btn_limpiar = tk.Button(panel_controles, text="Reiniciar", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", width=10, command=self.accion_reiniciar)
        btn_limpiar.pack(side=tk.LEFT, padx=5, pady=10)

        #       ÁREA DE DIBUJO (CANVAS)
        self.canvas = tk.Canvas(self.ventana, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def accion_insertar(self):
        # Por ahora solo atrapa el valor y manda un mensaje
        valor_str = self.txt_valor.get()
        if valor_str.isdigit():
            valor = int(valor_str)
            self.arbol.insertar(valor)
            messagebox.showinfo("Éxito", f"Valor {valor} insertado (Lógica interna).")
            self.txt_valor.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Por favor ingresa un número entero válido.")

    def accion_buscar(self):
        valor_str = self.txt_valor.get()
        if valor_str.isdigit():
            valor = int(valor_str)
            existe, camino = self.arbol.buscar(valor)
            messagebox.showinfo("Búsqueda", f"¿Existe {valor}?: {existe}\nCamino: {camino}")
            self.txt_valor.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Por favor ingresa un número entero válido.")

    def accion_reiniciar(self):
        self.arbol = ArbolBST()
        self.canvas.delete("all")
        messagebox.showinfo("Reiniciar", "El árbol ha sido vaciado.")

# Bloque principal para arrancar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazArbol(root)
    root.mainloop()