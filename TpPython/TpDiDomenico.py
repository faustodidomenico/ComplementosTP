#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Consigna: Implementar los siguientes metodos

# Para descargar py-gnuplot: http://sourceforge.net/projects/gnuplot-py/files/latest/download?source=files

import time
import Gnuplot
import random

rangoX = 100
rangoY = 100

def randomize_positions(G):
    nodos, aristas = G
    pos = {}
    fuerzas = {}
    for node in nodos:
        pos[node] = (random.uniform(0, rangoX), random.uniform(0, rangoY))
        fuerzas[node] = (0,0)
    return nodos,aristas,pos,fuerzas

def f_attraction(edge):
    pass

def f_repulsion(n1, n2):
    pass

def actualizo_posiciones():
    pass


def layout(grafo):
    nodos,aristas,pos,fuerzas = grafo
    for i in range(100): # steps, despues se pasa como argumento
        for n1,n2 in aristas:
            x1,y1 = pos[n1]
            x2,y2 = pos[n2]
            #dibujar las aristas
        for n in nodos:
            x,y = n
            #dibujar los nodos
    pass


def main():
    pass


if __name__ == "__main__":
    main()
