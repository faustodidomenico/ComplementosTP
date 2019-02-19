#! /usr/bin/python

#Tp de Fausto Di Domenico


# 6ta Practica Laboratorio
# Complementos Matematicos I


import time
import pygame
import random
import math
import argparse

rangoX = 800 #Ancho de la pantalla
rangoY = 800 #Alto de la pantalla
epsilon = 0.05 # Coeficiente tenido en cuenta cuando la distancia entre dos nodos es muy chica.
margen = 10 #Margen de la pantalla
screen = pygame.display.set_mode([rangoX,rangoY])

pygame.init()
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
fuente1 = pygame.font.SysFont('Serif', 15)

# Dado un grafo en forma de nodos y aristas, le asigna posiciones al azar a los nodos,
# e inicializa sus fuerzas en 0.
def randomize_positions(grafo):
    nodos, aristas = grafo
    pos = {}
    fuerzas = {}
    m = margen*2
    for nodo in nodos:
        pos[nodo] = (random.uniform(m, rangoX-m), random.uniform(m, rangoY-m))
        fuerzas[nodo] = (0,0)
    return pos,fuerzas

# Suma de vectores
def suma(a,b):
    a1,a2 = a
    b1,b2 = b
    return (a1+b1,a2+b2)

# Resta de vectores
def resta(a,b):
    a1,a2 = a
    b1,b2 = b
    return (a1-b1,a2-b2)

# Dado un archivo txt, lee el grafo que contiene y devuelve el grafo en
# formato de tupla de nodos y aristas.
def leer_grafo(nombre):
    nodos = []
    aristas = []
    grafo = nombre.read()
    grafo = grafo.split()
    n = int(grafo[0])
    for i in range(1,n+1):
        nodos.append(grafo[i])
    for i in range(n+1,len(grafo),2):
        aristas.append([grafo[i],grafo[i+1]])
    return nodos,aristas

# Dado los nodos de un grafo, sus posiciones actuales y las de la iteracion anterior
# devuelve False si la distancia entre la posicion actual de un nodo y su anterior
# es mayor a una constante. Devuelve True en caso contrario
def done(posAnterior, posActual, nodos, cteDist):
    for n in nodos:
        x0,y0 = posAnterior[n]
        x1,y1 = posActual[n]
        dist = math.sqrt((x1-x0)**2 + (y1-y0)**2)
        #print "dist "+str(dist)
        if dist > cteDist:
            return False
    return True

class LayoutGraph:

    def __init__(self, grafo, iters, refresh, verbose=False):
        '''
        Parametros de layout:
        grafo: es el grafo en formato de tupla de nodos y aristas
        iters: cantidad de iteraciones a realizar
        0 -> modo automatico
        refresh: Numero de iteraciones entre actualizaciones de pantalla.
        0 -> se grafica solo al final.
        '''

        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado, con las posiciones aleatorias
        inicial = randomize_positions(grafo)
        self.posiciones = inicial[0]
        self.fuerzas = inicial[1]

        self.iters = iters
        self.verbose = verbose
        self.refresh = refresh
        # k es el coeficiente utilizado para calcular las fuerzas de atraccion y repulsion.
        self.k = math.sqrt(rangoX * rangoY / len(grafo[0]))

    def layout(self):
        '''
        Muestra en la pantalla el grafo, con los nodos en las posiciones actualizaciones
        y las respectivas aristas.
        '''
        nodos,aristas = self.grafo
        pos = self.posiciones
        fuerzas = self.fuerzas

        for n1,n2 in aristas:
            x1,y1 = pos[n1]
            x2,y2 = pos[n2]
            pygame.draw.line(screen, BLUE, [int(round(x1)),int(round(y1))], [int(round(x2)),int(round(y2))],2)
        for n in nodos:
            x,y = pos[n]
            pygame.draw.circle(screen, RED, [int(round(x)),int(round(y))], 5)
            texto = fuente1.render(str(n), False, BLACK)
            screen.blit(texto,[int(round(x)-5),int(round(y)-20)])

    def updatePos(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para calcular las fuerzas
        de repulsion, atraccion y gravedad hacia el centro, y actualiza las posiciones.
        '''
        nodos,aristas = self.grafo
        for n in nodos:
            self.fuerzas[n] = (0,0)
        k = self.k
        #Repulsion
        for i,n0 in enumerate(nodos):
            x0,y0 = self.posiciones[n0]
            for n1 in nodos[0:i]+nodos[i+1:]:
                x1,y1 = self.posiciones[n1]
                dist = math.sqrt((x1-x0)**2 + (y1-y0)**2)
                while dist < epsilon:
                    self.posiciones[n1] = (x1 + random.uniform(-10,10),y1 + random.uniform(-10,10))
                    x1,y1 = self.posiciones[n1]
                    dist = math.sqrt((x1-x0)**2 + (y1-y0)**2)
                mod_fr = k / dist
                fx = mod_fr * (x1-x0) / dist
                fy = mod_fr * (y1-y0) / dist
                self.fuerzas[n0] = resta(self.fuerzas[n0],(fx,fy))
                self.fuerzas[n1] = suma(self.fuerzas[n1],(fx,fy))

        #Gravedad
        x0,y0 = (rangoX/2, rangoY/2)
        for n1 in nodos:
            x1,y1 = self.posiciones[n1]
            dist = math.sqrt((x0-x1)**2 + (y0-y1)**2)
            mod_fr = dist / k
            fx = mod_fr * (x1-x0) / dist
            fy = mod_fr * (y1-y0) / dist
            self.fuerzas[n0] = resta(self.fuerzas[n0],(fx,fy))

        #Atraccion
        for n0,n1 in aristas:
            x0,y0 = self.posiciones[n0]
            x1,y1 = self.posiciones[n1]
            dist = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            if dist < epsilon:
                dist = epsilon
            mod_fa = dist / k
            fx = mod_fa * (x1-x0) / dist
            fy = mod_fa * (y1-y0) / dist
            self.fuerzas[n0] = suma(self.fuerzas[n0],(fx,fy))
            self.fuerzas[n1] = resta(self.fuerzas[n1],(fx,fy))

        for n in nodos:
            self.posiciones[n] = suma(self.posiciones[n],self.fuerzas[n])
            #Corrijo la posicion en caso de que se vaya de la pantalla
            self.posiciones[n] = (min(rangoX-margen,max(margen,self.posiciones[n][0])),min(rangoY-margen,max(margen,self.posiciones[n][1])))

    def actualizoK(self):
        '''
        En caso de que algunos de los nodos este sobre algun margen, se achica el k.
        Si el k es menor o igual a 25, queda en 25.
        Esto es porque en muchos casos el k inicial no es el adecuado y los nodos tienden
        a irse de la pantalla, achicando el k se puede solucionar esto.
        '''
        if self.k <= 25:
            self.k = 25
        else:
            for n in self.grafo[0]:
                x,y = self.posiciones[n]
                if x <= margen or x >= rangoX-margen or y <= margen or y >= rangoY-margen:
                    self.k = self.k * 0.99

    def modoVerbose(self, iter):
        '''
        Para el modo verbose, imprime una tabla de datos en la consola,
        la iteracion, el k, las posiciones y las fuerzas de cada nodo actuales.
        '''
        print "Iteracion numero: "+str(iter)
        print "k = "+str(self.k)
        print("Nodo    posX\t\tposY\t\tfuerzaX\t\tfuerzaY")
        for n in self.grafo[0]:
            x,y = self.posiciones[n]
            fx,fy = self.fuerzas[n]
            print "  "+str(n)+"    "+str(x)+"\t"+str(y)+"\t"+str(fx)+"\t"+str(fy)
        print "\n"

    def layout_iters(self, cteVerbose):
        '''
        Aplica el algoritmo e itera la cantidad de veces que se le paso como argumento
        En este caso segun la cantidad que se le pase, en ocasiones el grafo no
        queda de forma adecuada.
        '''
        for iter in range(self.iters):
            if self.refresh != 0 and iter % self.refresh == 0:
                screen.fill(WHITE)
                self.layout()
                pygame.display.flip()
            if self.verbose and iter % cteVerbose == 0:
                self.modoVerbose(iter)
            self.updatePos()
            self.actualizoK()

        if self.refresh == 0:
            screen.fill(WHITE)
            self.layout()
            pygame.display.flip()


    def layout_auto(self, cteVerbose, cteDist):
        '''
        Aplica el algoritmo e itera hasta que la distancia de todos los nodos
        respecto de su posicion anterior sea menor a una constante.
        La mayoria de los casos el grafo queda de forma adecuada.
        '''
        iter = 0
        n = 1
        while n:
            if self.refresh != 0 and iter % self.refresh == 0:
                screen.fill(WHITE)
                self.layout()
                pygame.display.flip()
            if self.verbose and iter % cteVerbose == 0:
                self.modoVerbose(iter)
            pos = {}
            for n in self.grafo[0]:
                pos[n] = self.posiciones[n]
            self.updatePos()
            self.actualizoK()
            iter += 1
            if done(pos, self.posiciones, self.grafo[0], cteDist):
                n = 0

        if self.refresh == 0:
            screen.fill(WHITE)
            self.layout()
            pygame.display.flip()




def main():
    # Definimos los argumentos de lina de comando que aceptamos
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'), help='Especificar archivo de donde leer el grafo', default=None)
    parser.add_argument('-v', action='store_true', help='Muestra mas informacion al correr el programa')
    parser.add_argument('-iters', type=int,help='Cantidad de iteraciones a efectuar',default=0)
    parser.add_argument('-refresh', type=int,help='Cantidad de iteraciones entre actualizacions de pantalla',default=0)
    args = vars(parser.parse_args())
    '''
    refresh = 0, se grafica solo al final.
    iters = 0, itera en modo automatico. Esto quiere decir que itera hasta que la distancia
    de todos los nodos respecto a su posicion anterior sea menor a una constante de distancia.
    En modo default, las iters = 0, refresh = 0.
    '''
    #Leemos el grafo
    grafo = leer_grafo(args["file"])
    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo,
        iters=args["iters"],
        refresh=args["refresh"],
        verbose=args["v"]
        )

    screen.fill(WHITE)
    cteVerbose = 30 #Representa la cantidad de iteraciones entre las que muestra los
    # datos en el modo verbose.
    cteDist = 0.05 #Constante para el modo automatico, si todos la distancia de todos
    # los nodos respecto a su posicion anterior es menor a la constante, deja de iterar.
    if layout_gr.iters == 0:
        layout_gr.layout_auto(cteVerbose, cteDist)
    else:
        layout_gr.layout_iters(cteVerbose)
    n = 1
    while n: #Para seguir con la ventana abierta y cerrarla manualmente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n=0
    pygame.quit()
    return


if __name__ == '__main__':
    main()
