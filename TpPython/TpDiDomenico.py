#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Consigna: Implementar los siguientes metodos

# Para descargar py-gnuplot: http://sourceforge.net/projects/gnuplot-py/files/latest/download?source=files

import time
import pygame
import random
import math

rangoX = 800
rangoY = 600
C = 1
margen = 10
epsilon = 0.05

def randomize_positions(G):
    nodos, aristas = G
    pos = {}
    fuerzas = {}
    for nodo in nodos:
        pos[nodo] = (random.uniform(0, rangoX), random.uniform(0, rangoY))
        fuerzas[nodo] = (0,0)
    return nodos,aristas,pos,fuerzas

def f_a(x, cantNodos):
    k = C * math.sqrt(rangoX * rangoY / cantNodos)
    return x**2/k
    pass

def f_r(x, cantNodos):
    k = C * math.sqrt(rangoX * rangoY / cantNodos)
    return k**2/x
    pass

def suma(a,b):
    a1,a2 = a
    b1,b2 = a
    return (a1+b1,a2+b2)

def resta(a,b):
    a1,a2 = a
    b1,b2 = a
    return (a1-b1,a2-b2)

def f_atraccion(grafo):
    nodos,aristas,pos,fuerzas = grafo
    for n1,n2 in aristas:
        x1,y1 = pos[n1]
        x2,y2 = pos[n2]
        dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        while(dist<epsilon):
            pos[n1] = (x1+random(-5,5),y1+random(-5,5))
            pos[n2] = (x2+random(-5,5),y2+random(-5,5))
            x1,y1 = pos[n1]
            x2,y2 = pos[n2]
            dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        mod_fa = f_a(dist, len(nodos))
        fx = mod_fa * (x1-x2) / dist
        fy = mod_fa * (y1-y2) / dist
        fuerzas[n1] = suma(fuerzas[n1],(fx,fy))
        fuerzas[n2] = resta(fuerzas[n2],(fx,fy))
    return nodos,aristas,pos,fuerzas
    pass

def f_repulsion(grafo):
    nodos,aristas,pos,fuerzas = grafo
    for i,n1 in enumerate(nodos):
        x1,y1 = pos[n1]
        for n2 in nodos[0:i]+nodos[i+1:]:
            x2,y2 = pos[n2]
            dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            while(dist<epsilon):
                pos[n1] = (x1+random(-5,5),y1+random(-5,5))
                pos[n2] = (x2+random(-5,5),y2+random(-5,5))
                x1,y1 = pos[n1]
                x2,y2 = pos[n2]
                dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            mod_fr = f_r(dist, len(nodos))
            fx = mod_fr * (x1-x2) / dist
            fy = mod_fr * (y1-y2) / dist
            fuerzas[n1] = resta(fuerzas[n1],(fx,fy))
            fuerzas[n2] = suma(fuerzas[n2],(fx,fy))
    return nodos,aristas,pos,fuerzas
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
    f_atraccion(grafo)
    f_repulsion(grafo)
    for n in nodos:
        pos[n] = suma(pos[n],fuerzas[n])
        pos[n] = (min(rangoX-margen,max(margen,pos[n][0])),min(rangoY-margen,max(margen,pos[n][1])))
        #pos[n][1] = min(rangoY-margen,max(margen,pos[n][1]))
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
            #print [int(round(x)),int(round(y))]
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
        actualizo_posiciones(BTree)
    pygame.quit()
    pass


if __name__ == "__main__":
    main()
