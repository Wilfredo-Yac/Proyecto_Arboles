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
    #            RECORRIDOS RECURSIVOS
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
    #             BÚSQUEDA RECURSIVA
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

    #            ELIMINACIÓN RECURSIVA
    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return nodo_actual

        # 1. Buscar el nodo a eliminar
        if valor < nodo_actual.valor:
            nodo_actual.izquierdo = self._eliminar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecho = self._eliminar_recursivo(nodo_actual.derecho, valor)
        else:

            # CASO 1 y 2: Nodo hoja o con un solo hijo
            if nodo_actual.izquierdo is None:
                return nodo_actual.derecho
            elif nodo_actual.derecho is None:
                return nodo_actual.izquierdo

            # CASO 3: Nodo con dos hijos
            # Buscamos el sucesor en inorden (el menor del subárbol derecho)
            sucesor = self._encontrar_minimo(nodo_actual.derecho)
            # Reemplazamos el valor por el del sucesor
            nodo_actual.valor = sucesor.valor
            # Eliminamos recursivamente el sucesor en el subárbol derecho
            nodo_actual.derecho = self._eliminar_recursivo(nodo_actual.derecho, sucesor.valor)

        return nodo_actual

    def _encontrar_minimo(self, nodo):
        nodo_actual = nodo
        while nodo_actual.izquierdo is not None:
            nodo_actual = nodo_actual.izquierdo
        return nodo_actual