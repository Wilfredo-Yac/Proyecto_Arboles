from arbol_bst import ArbolBST

mi_arbol = ArbolBST()
valores = [50, 30, 70, 20, 40]
for v in valores:
    mi_arbol.insertar(v)

print("¡Estructura del árbol creada con éxito!")
print(f"Recorrido Inorden: {mi_arbol.obtener_inorden()}")

# Probar la búsqueda
existe, camino = mi_arbol.buscar(40)
print(f"¿Existe el número 40?: {existe} | Camino recorrido: {camino}")