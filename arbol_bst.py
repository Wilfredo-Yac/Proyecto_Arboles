from nodo import Nodo

class ArbolBST:
    def __init__(self):
        self.raiz = None  # Al principio el árbol está vacío

    def insertar(self, valor):
        # Método público que interactúa con el usuario/interfaz
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        # Si encontramos el lugar vacío, creamos y retornamos el nuevo nodo
        if nodo_actual is None:
            return Nodo(valor)

        # Si el valor es menor, nos movemos recursivamente a la izquierda
        if valor < nodo_actual.valor:
            nodo_actual.izquierdo = self._insertar_recursivo(nodo_actual.izquierdo, valor)
        # Si el valor es mayor, nos movemos recursivamente a la derecha
        elif valor > nodo_actual.valor:
            nodo_actual.derecho = self._insertar_recursivo(nodo_actual.derecho, valor)
        
        # Retornamos el nodo (sin cambios si el valor ya existía)
        return nodo_actual

    # ==========================================
    #             RECORRIDOS RECURSIVOS
    # ==========================================

    def obtener_preorden(self):
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            resultado.append(nodo_actual.valor)  # 1. Raíz
            self._preorden_recursivo(nodo_actual.izquierdo, resultado)  # 2. Izquierda
            self._preorden_recursivo(nodo_actual.derecho, resultado)  # 3. Derecha

    def obtener_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            self._inorden_recursivo(nodo_actual.izquierdo, resultado)  # 1. Izquierda
            resultado.append(nodo_actual.valor)  # 2. Raíz
            self._inorden_recursivo(nodo_actual.derecho, resultado)  # 3. Derecha

    def obtener_postorden(self):
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            self._postorden_recursivo(nodo_actual.izquierdo, resultado)  # 1. Izquierda
            self._postorden_recursivo(nodo_actual.derecho, resultado)  # 2. Derecha
            resultado.append(nodo_actual.valor)  # 3. Raíz

# ==========================================
    #             BÚSQUEDA RECURSIVA
    # ==========================================
    def buscar(self, valor):
        # Devuelve: (True/False si existe, lista con el camino recorrido)
        camino = []
        encontrado = self._buscar_recursivo(self.raiz, valor, camino)
        return encontrado, camino

    def _buscar_recursivo(self, nodo_actual, valor, camino):
        if nodo_actual is None:
            return False
        
        # Registramos el nodo actual en el camino de visitas
        camino.append(nodo_actual.valor)
        
        if valor == nodo_actual.valor:
            return True
        
        if valor < nodo_actual.valor:
            return self._buscar_recursivo(nodo_actual.izquierdo, valor, camino)
        
        return self._buscar_recursivo(nodo_actual.derecho, valor, camino)