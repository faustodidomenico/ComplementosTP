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
#Ejemplo
def randomize_positions(nodos, pos_x, pos_y):
    for node in nodos:
        pos_x[node] = random.uniform(0, rangoX)
        pos_y[node] = random.uniform(0, rangoY)

def inicializar_acumuladores():
    pass

def f_attraction(edge):
    pass

def f_repulsion(n1, n2):
    pass

def actualizo_posiciones():
    pass


def run_layout(grafo):
    '''
    Dado un grafo (en formato de listas), aplica el algoritmo de
    Fruchtermann-Reingold para obtener (y mostrar) un layout
    '''

    nodos, aristas = grafo
    pos_x =  {node:0 for node in nodos}
    pos_y =  {node:0 for node in nodos}
    randomize_positions(nodos, pos_x, pos_y)
    for i in range(100): #repeticiones (steps)
        #Inicializar acumuladores
        acum_x = {node:0 for node in nodos}
        acum_y = {node:0 for node in nodos}
        for n1,n2 in aristas:
            f = f_attraction(n1,n2)
            acum[e.origen] += f
            acum[e.dest] -= f
        for j,n1 in enumerate(nodos):
            for n2 in nodos[j+1:]:
                f = f_repulsion(n1,n2)
                acum[n1] += f
                acum[n2] += f
        actualizo_posiciones()
    pass



def ejemplo_gnuplot():
    g = Gnuplot.Gnuplot()

    # Ponerle titulo
    g('set title "TITULO"')
    # setear el intervalo a mostrar
    g('set xrange [0:100]; set yrange [0:100]')
    # Dibujar un rectangulo en 10, 20
    g('set object 1 rectangle center 10,20 size 5,5 fc rgb "black"')
    # Dibujar un circulo en 30, 40
    g('set object 2 circle center 30,40 size 3 ')
    # Dibujar una arista
    g('set arrow nohead from 10,20 to 30,40')
    # Borra leyenda
    g('unset key')
    # Dibujar
    g('plot NaN')

    # esperar 1 segundo
    time.sleep(1)

    # Borrar objeto 1
    g('unset object 1')
    # Re-dibujar
    g('replot')

    # esperar 1 segundo
    time.sleep(1)

def main():
    ejemplo_gnuplot()

if __name__ == "__main__":
    main()
