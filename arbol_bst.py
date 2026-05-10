from nodo import Nodo

class ArbolBST:  # Mantenemos el nombre de la clase para no romper la interfaz
    def __init__(self):
        self.raiz = None

    #            MÉTODOS DE ALTURA Y BALANCE
    # ==========================================
    def _obtener_altura(self, nodo):
        if nodo is None:
            return 0
        # Buscamos de forma recursiva cuál de sus dos ramas es más profunda
        return 1 + max(self._obtener_altura(nodo.izquierdo), self._obtener_altura(nodo.derecho))

    def _obtener_balance(self, nodo):
        if nodo is None:
            return 0
        # Factor de Balance = Altura Izquierda - Altura Derecho
        return self._obtener_altura(nodo.izquierdo) - self._obtener_altura(nodo.derecho)

    #          ROTACIONES AVL (MÁGICA)
    # ==========================================
    def _rotar_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho

        # Ejecutar la rotación
        x.derecho = y
        y.izquierdo = T2

        # Retornar la nueva raíz de este subárbol
        return x

    def _rotar_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo

        # Ejecutar la rotación
        y.izquierdo = x
        x.derecho = T2

        # Retornar la nueva raíz de este subárbol
        return y

    #            INSERCIÓN AUTOBALANCEADA
    # ==========================================
    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        # 1. Inserción normal de un BST
        if nodo_actual is None:
            return Nodo(valor)
        
        if valor < nodo_actual.valor:
            nodo_actual.izquierdo = self._insertar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecho = self._insertar_recursivo(nodo_actual.derecho, valor)
        else:
            return nodo_actual  # No se permiten duplicados en AVL

        # 2. Calcular el factor de balance del nodo padre
        balance = self._obtener_balance(nodo_actual)

        # 3. Si el nodo se desbalanceó, aplicamos uno de los 4 casos de rotación:

        # Caso Izquierda - Izquierda (Rotación Simple a la Derecha)
        if balance > 1 and valor < nodo_actual.izquierdo.valor:
            return self._rotar_derecha(nodo_actual)

        # Caso Derecha - Derecha (Rotación Simple a la Izquierda)
        if balance < -1 and valor > nodo_actual.derecho.valor:
            return self._rotar_izquierda(nodo_actual)

        # Caso Izquierda - Derecha (Rotación Doble)
        if balance > 1 and valor > nodo_actual.izquierdo.valor:
            nodo_actual.izquierdo = self._rotar_izquierda(nodo_actual.izquierdo)
            return self._rotar_derecha(nodo_actual)

        # Caso Derecha - Izquierda (Rotación Doble)
        if balance < -1 and valor < nodo_actual.derecho.valor:
            nodo_actual.derecho = self._rotar_derecha(nodo_actual.derecho)
            return self._rotar_izquierda(nodo_actual)

        return nodo_actual

    #            ELIMINACIÓN AVL
    # ==========================================
    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return nodo_actual

        if valor < nodo_actual.valor:
            nodo_actual.izquierdo = self._eliminar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecho = self._eliminar_recursivo(nodo_actual.derecho, valor)
        else:
            # Encontramos el nodo (Casos de eliminación)
            if nodo_actual.izquierdo is None:
                return nodo_actual.derecho
            elif nodo_actual.derecho is None:
                return nodo_actual.izquierdo

            sucesor = self._encontrar_minimo(nodo_actual.derecho)
            nodo_actual.valor = sucesor.valor
            nodo_actual.derecho = self._eliminar_recursivo(nodo_actual.derecho, sucesor.valor)

        if nodo_actual is None:
            return nodo_actual

        # Re-balancear el árbol tras la eliminación
        balance = self._obtener_balance(nodo_actual)

        if balance > 1 and self._obtener_balance(nodo_actual.izquierdo) >= 0:
            return self._rotar_derecha(nodo_actual)

        if balance > 1 and self._obtener_balance(nodo_actual.izquierdo) < 0:
            nodo_actual.izquierdo = self._rotar_izquierda(nodo_actual.izquierdo)
            return self._rotar_derecha(nodo_actual)

        if balance < -1 and self._obtener_balance(nodo_actual.derecho) <= 0:
            return self._rotar_izquierda(nodo_actual)

        if balance < -1 and self._obtener_balance(nodo_actual.derecho) > 0:
            nodo_actual.derecho = self._rotar_derecha(nodo_actual.derecho)
            return self._rotar_izquierda(nodo_actual)

        return nodo_actual

    def _encontrar_minimo(self, nodo):
        nodo_actual = nodo
        while nodo_actual.izquierdo is not None:
            nodo_actual = nodo_actual.izquierdo
        return nodo_actual

    #      RECORRIDOS Y BÚSQUEDA (SE QUEDAN IGUAL)
    # ==========================================
    def obtener_preorden(self):
        res = []
        self._preorden_rec(self.raiz, res)
        return res
    def _preorden_rec(self, n, res):
        if n: res.append(n.valor); self._preorden_rec(n.izquierdo, res); self._preorden_rec(n.derecho, res)

    def obtener_inorden(self):
        res = []
        self._inorden_rec(self.raiz, res)
        return res
    def _inorden_rec(self, n, res):
        if n: self._inorden_rec(n.izquierdo, res); res.append(n.valor); self._inorden_rec(n.derecho, res)

    def obtener_postorden(self):
        res = []
        self._postorden_rec(self.raiz, res)
        return res
    def _postorden_rec(self, n, res):
        if n: self._postorden_rec(n.izquierdo, res); self._postorden_rec(n.derecho, res); res.append(n.valor)

    def buscar(self, valor):
        camino = []
        encontrado = self._buscar_recursivo(self.raiz, valor, camino)
        return encontrado, camino
    def _buscar_recursivo(self, nodo_actual, valor, camino):
        if nodo_actual is None: return False
        camino.append(nodo_actual.valor)
        if valor == nodo_actual.valor: return True
        if valor < nodo_actual.valor: return self._buscar_recursivo(nodo_actual.izquierdo, valor, camino)
        return self._buscar_recursivo(nodo_actual.derecho, valor, camino)