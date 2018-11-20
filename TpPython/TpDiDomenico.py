#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Consigna: Implementar los siguientes metodos

# Para descargar py-gnuplot: http://sourceforge.net/projects/gnuplot-py/files/latest/download?source=files

import time
import pygame
import random

rangoX = 800
rangoY = 600

def randomize_positions(G):
    nodos, aristas = G
    pos = {}
    fuerzas = {}
    for nodo in nodos:
        pos[nodo] = (random.uniform(0, rangoX), random.uniform(0, rangoY))
        fuerzas[nodo] = (0,0)
    return nodos,aristas,pos,fuerzas

def f_atraccion(grafo):
    nodos,aristas,pos,fuerzas = grafo
    for n1,n2 in aristas:
        dist = math.sqrt((pos[n1][1]-pos[n2][1])**2 + (pos[n1][2]-pos[n2][2])**2)
        
    pass

def f_repulsion(grafo):
    pass

def reiniciar_acumuladores(grafo):
    nodos,aristas,pos,fuerzas = grafo
    for nodo in fuerzas:
        fuerzas[nodo] = (0,0)
    return nodos,aristas,pos,fuerzas
    pass

def actualizo_posiciones(grafo):
    reiniciar_acumuladores(grafo)
    nodos,aristas,pos,fuerzas = grafo
    fa = f_atraccion(grafo)
    fr = f_repulsion(grafo)
    for n in nodos:
        pos[n][1] = pos[n][1] + fuerzas[n][1]
        pos[n][2] = pos[n][2] + fuerzas[n][2]
    return nodos,aristas,pos,fuerzas
    pass


def layout(grafo):
    nodos,aristas,pos,fuerzas = grafo
    for i in range(100): # steps, despues se pasa como argumento
        for n1,n2 in aristas:
            x1,y1 = pos[n1]
            x2,y2 = pos[n2]
            pygame.draw.line(screen, BLUE, [int(round(x1)),int(round(y1))], [int(round(x2)),int(round(y2))],2)
        for n in nodos:
            x,y = pos[n]
            pygame.draw.circle(screen, RED, [int(round(x)),int(round(y))], 5)
            texto = fuente1.render(str(n), False, BLACK)
            screen.blit(texto,[int(round(x)-5),int(round(y)-20)])
    pass

pygame.init()
screen = pygame.display.set_mode([rangoX,rangoY])
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
fuente1 = pygame.font.SysFont('Serif', 15)

def main():
    BTree = ([1,2,3,4,5,6,7],[(4,2),(4,6),(2,1),(2,3),(6,5),(6,7)])
    n = 1
    BTree = randomize_positions(BTree)

    while n:
        screen.fill(WHITE)
        layout(BTree)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n=False
    pygame.quit()
    pass


if __name__ == "__main__":
    main()
