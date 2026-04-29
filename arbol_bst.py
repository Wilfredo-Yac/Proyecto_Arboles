from nodo import Nodo

class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return Nodo(valor)
        if valor < nodo_actual.valor:
            nodo_actual.izquierdo = self._insertar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecho = self._insertar_recursivo(nodo_actual.derecho, valor)
        return nodo_actual
    # ==========================================
    #            RECORRIDOS RECURSIVOS
    # ==========================================
    def obtener_preorden(self):
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            resultado.append(nodo_actual.valor)  # Raíz
            self._preorden_recursivo(nodo_actual.izquierdo, resultado)  # Izquierda
            self._preorden_recursivo(nodo_actual.derecho, resultado)  # Derecha

    def obtener_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            self._inorden_recursivo(nodo_actual.izquierdo, resultado)  # Izquierda
            resultado.append(nodo_actual.valor)  # Raíz
            self._inorden_recursivo(nodo_actual.derecho, resultado)  # Derecha

    def obtener_postorden(self):
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            self._postorden_recursivo(nodo_actual.izquierdo, resultado)  # Izquierda
            self._postorden_recursivo(nodo_actual.derecho, resultado)  # Derecha
            resultado.append(nodo_actual.valor)  # Raíz

    # ==========================================
    #             BÚSQUEDA RECURSIVA
    # ==========================================
    def buscar(self, valor):
        camino = []
        encontrado = self._buscar_recursivo(self.raiz, valor, camino)
        return encontrado, camino

    def _buscar_recursivo(self, nodo_actual, valor, camino):
        if nodo_actual is None:
            return False
        
        camino.append(nodo_actual.valor)  # Registrar nodo visitado
        
        if valor == nodo_actual.valor:
            return True
        if valor < nodo_actual.valor:
            return self._buscar_recursivo(nodo_actual.izquierdo, valor, camino)
        return self._buscar_recursivo(nodo_actual.derecho, valor, camino)