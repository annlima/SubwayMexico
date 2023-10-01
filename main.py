from InterfazMetro import *
import geopy.distance
import pandas as pd

DistanciaEntreNodos = []

### Obteniendo las aristas con sus pesos
with open('Aristas.txt', 'r', encoding='UTF-8') as aristasMetro:
    data = aristasMetro.read()

d = data.split("\n")
a = [x.split(",") for x in d]

#Cambiando de String a Integer
i = 0
while i < len(a):
    a[i][2] = int(a[i][2])
    i += 1

### Obteniendo los Vértices del Metro
with open('Vertices.txt', 'r', encoding='UTF-8') as vertices:
    data1 = vertices.read()
vertices = data1.split("\n")

with open('lineas.txt', 'r', encoding='UTF-8') as lineas:
    data2 = lineas.read()
origenLinea = data2.split("\n")
linea = [y.split(",") for y in origenLinea]


### Creando un arreglo o matriz de adyacencias para cada estación
grafo = {}
for i in vertices:
    grafo[i] = {}
grafo1 = {}

### Realizando la unión de las aristas con sus pesos
i = 0
j = 0
for key in grafo:
    i = 0
    while i < len(a):
        if key == a[i][0]:
            grafo[key].update({a[i][1]: a[i][2]})
        i += 1
print(grafo)

##Usando el algoritmo de Dijkstra para encontrar la distancia menor entre nodos
def Dijkstra_MenorCamino(grafo, partida, llegada):
    PrimerMomento = {}
    DijkstraActual = {}
    NuevoMomento = partida
    control = {}
    NoVisitado = []
    PrimerMomento[NuevoMomento] = 0

    for vertice in grafo.keys():
        NoVisitado.append(vertice)
        DijkstraActual[vertice] = float('inf')

    DijkstraActual[NuevoMomento] = [0, partida]
    NoVisitado.remove(NuevoMomento)

    while NoVisitado:
        for nombre, peso in grafo[NuevoMomento].items():
            SumaPeso = peso + PrimerMomento[NuevoMomento]
            if DijkstraActual[nombre] == float("inf") or DijkstraActual[nombre][0] > SumaPeso:
                DijkstraActual[nombre] = [SumaPeso, NuevoMomento]
                control[nombre] = SumaPeso

        if control == {}: break
        TrayectoMinimo = min(control.items(), key=lambda x: x[1])
        NuevoMomento = TrayectoMinimo[0]
        PrimerMomento[NuevoMomento] = TrayectoMinimo[1]
        NoVisitado.remove(NuevoMomento)
        del control[NuevoMomento]
# Variables para imprimir el camino mínimo
    Respuesta1 = "La menor distancia es: ", (partida, llegada, DijkstraActual[llegada][0])
    Respuesta2 = "El mejor camino es: ", ImprimirElCamino(DijkstraActual, partida, llegada)
    RespuestaDistancia = str(Respuesta1)
    RespuestaCamino = str(Respuesta2)
    RespuestaCompleta = RespuestaDistancia + "\n" + RespuestaCamino
    print(RespuestaCompleta)
    DistanciaEntreNodos.append(RespuestaCompleta)
    ImprimirDistancia = DistanciaEntreNodos[0]
    ui.RespInterfaz.setText(ImprimirDistancia)
    del(DistanciaEntreNodos[0])

# Imprimir el camino mínimo
def ImprimirElCamino(distancia, partida, Llegada):
    if Llegada != partida:
        return "%s>%s" % (ImprimirElCamino(distancia, partida, distancia[Llegada][1]), Llegada)
    else:
        return partida

# Uso de la interfaz
def main(ui):
    def a():
        Origen = ui.OrigenlineEdit.text()
        Destino = ui.DestinolineEdit.text()
        origen = str(Origen)
        destino = str(Destino)
        Dijkstra_MenorCamino(grafo, origen, destino)

    ui.BotonBusqueda.clicked.connect(a)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    main(ui)
    sys.exit(app.exec_())