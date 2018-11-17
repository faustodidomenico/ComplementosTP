'''
Algoritmo Fruchterman-Reingold (Para dibujar grafos)
Se recomienda la libreria gnuplot (pero hubo gente que uso pygame o algunas otras)
pip install PyGnuplot
Tools:
- pip: te permite instalar librerias muy facilmente (package manager)
 pip install <paquete>
 - virtualenv: para evitar conflictos e instalar las cosas globalmente(para cada proyecto)
 source tp_final_env/bin/activate
 (ahora cada vez que instalo algo con pip se instala para este proyecto)
 - pdb: debugger
   import pdb; pdb.set_trace()
            L -> imprime codigo
            n -> sig linea
            s -> sep "into"
            c -> continue

layout (dar posicion a las cosas)
layout (G):
    N,E = G
    randomize_positions(N)
    #Los nodos se repelen, y las aristas son como resortes que se atraen y
    # hay que hacer la suma de las fuerzas correspondientes a cada nodos
    for i in range(R): # R = 100, (repeticiones)
        reiniciamos_acumuladores()
        #se puede guardar los acumuladores en diccionarios (1 o 2)
        for e in E:
            # Las fuerzas en cada extremo de una arista tienen igual modulo
            # igual sentido pero direccion opuesta
            f = f_attraction(e)
            acum[e.origen] += f
            acum[e.dest] -= f
        Para cada par n1, n2 de nodos:
            f = f_repulsion(n1,n2)
            acum[n1] += f
            acum[n2] += f
        - calcular fuerzas de gravedad
        actualizo_posiciones() #se hace un dibujito



def inicanilizar_acumuladores():
    # acum_x = {'nodo1':0, 'nodo2':0,...}
    # para saber la fuerza de un nodo acum_x['nodoZ']
    acum_x = {node:0 for node in N}
    acum_y = { "" }

def f_a(x):
    k = C * sqrt(area/#nodos) # area de trabajo
    return x**2/k

def f_r(x):
    k**2/x # En el paper hay un - pero de esta forma es para calcular le modulo

def f_attraction():
    for n1, n2 in aristas:
        dist = sqrt((pos_x[n1] - pos_x[n2]) ** 2 + (pos_y[n1] - pos_y[n2]) ** 2)
        mod_fa = f_a(dist)
        #f = mod_fa * d/|d| (versor asociado a la distancia de los vectores)
        fx = mod_fa(pos_x[n2]-pos_x[n1]) / dist
        fy = "" # Lo mismo
        acum_x[n1] = acum_x[n1] + fx
        acum_y[n1] = acum_y[n1] + fy
        acum_x[n2] = acum_x[n2] - fx
        acum_y[n2] = acum_y[n2] - fy

def f_repulsion():
    parecido cambian algunos + por -

def actualizo_posiciones():
    for node in nodos: #Formula en el caso que no se va de la pantalla (intervalo)
    pos_x[node] = pos_x[node] + acum_x[node]
    pos_y[node] = pos_y[node] + acum_y[node]
    #Tener en cuenta los bordes


'''
'''
incializamos posiciones
inicializar temperatura (t = t0)

step():
reiniciamos_acumuladores
calcular fuerzas de atraccion
calcular fuerzas de repulsion
calcular fuerzas de gravedad
actualizar pocisiones
Si el modulo de la fuerza |f|>t movemos el nodo con la misma direccion y sentido
que f pero con el modulo de t
if |f| > t:
    f = (f/|f|) * t
actualizar temperatura():
    t = ce*t # ce = cte enfriamiento = 0.95 ó 0.9




- Leer grafo de archivo, path del archivo por linea de comando
- Iteraciones: parametro opcional (linea de comando)
- Modo "verbose"
- Puede ser modo fullscreen o tamaño de la pantalla

Caso que la distancia entre dos nodos es muy chica (d < E) E = 0,05:
Le sumo x e y al azar en [-10,10]

Mejoras:
elegir el punto del medio y que todos los nodos tienen
fuerza de atraccion hacia el centro, y g constante
(como si fuera la gravedad)

Tecnica para forzar la convergencia en casos que queda oscilando:


'''







'''
import pygame
import math
import random

def gManta(n):
    V = [i for i in range(1,n*n + 1)]
    E = []
    for v in V:
        if (v%n)!=0:
            E.append((v,v+1))
        if v<=(n*n - n):
            E.append((v,v+n))
    return (V,E)

def graphK(n):
    V = [i for i in range(1,n+1)]
    E = []
    for i,v0 in enumerate(V):
        for v1 in V[0:i]+V[i+1:]:
            E.append((v0,v1))
    return (V,E)

def randomPos(G):
    V,E = G
    pos = {}
    force = {}

    for v in V:
        pos[v] = (random.randrange(400,600),random.randrange(300,500))
        force[v] = (0,0)
    return (V,E,pos,force)

def plotGraph(G, show_more):
    V,E,pos,force = G
    for e in E:
        v0,v1 = e
        x0,y0 = pos[v0]
        x1,y1 = pos[v1]
        pygame.draw.line(screen, BLACK, [int(round(x0)), int(round(y0))], [int(round(x1)), int(round(y1))], 2)
    for v in V:
        x,y = pos[v]
        pygame.draw.circle(screen, RED, [int(round(x)), int(round(y))], 5)
        if show_more:
            fx,fy = force[v]
            pygame.draw.line(screen, GREEN, [int(round(x)), int(round(y))], [int(round(x+(fx*20))), int(round(y+(fy*20)))], 2)
            text = myfont2.render(str(math.sqrt(fx**2 + fy**2)), False, GREEN)
            screen.blit(text,[int(round(x+(fx*20)))+5, int(round(y+(fy*20)))-5])
        text = myfont.render(str(v), False, BLUE)
        screen.blit(text,(int(round(x))+5, int(round(y))+5))
    pass

def sum(u,v):
    x0,y0 = u
    x1,y1 = v
    return (x0+x1,y0+y1)

def sub(u,v):
    x0,y0 = u
    x1,y1 = v
    return (x0-x1,y0-y1)

def updatePos(G,k):
    V,E,pos,force = G

    for v in V:
        force[v] = (0,0)

    for i,v0 in enumerate(V):
        x0,y0 = pos[v0]
        for v1 in V[0:i]+V[i+1:]:
            x1,y1 = pos[v1]
            dist = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            f = k/dist
            s = (y1-y0)/dist
            c = (x1-x0)/dist
            force[v0] = sub(force[v0],(c*f,s*f))
            force[v1] = sum(force[v1],(c*f,s*f))

    for v0,v1 in E:
        x0,y0 = pos[v0]
        x1,y1 = pos[v1]
        dist = math.sqrt((x1-x0)**2 + (y1-y0)**2)
        f = dist/k
        s = (y1-y0)/dist
        c = (x1-x0)/dist
        force[v0] = sum(force[v0],(c*f,s*f))
        force[v1] = sub(force[v1],(c*f,s*f))

    for v in V:
        pos[v] = sum(pos[v],force[v])

    return (V,E,pos,force)

def updateK(G,k,width,height):
    V,E,pos,force = G

    for v in V:
        x,y = pos[v]
        if x>=width-5 or y>=height-5 or x<=5 or y<=5:
            return k*0.99
    return k

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 25)
myfont2 = pygame.font.SysFont('Arial', 15)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

width = 1000
height = 800
screen = pygame.display.set_mode([width,height])

pygame.display.set_caption("FRUCHTERMAN - REINGOLD")

done = False
clock = pygame.time.Clock()

Petersen = randomPos(([1,2,3,4,5,6,7,8,9,10],
    [(1,2),(2,3),(3,4),(4,5),(5,1),(1,7),(2,8),(3,9),(4,10),(5,6),(7,10),(10,8),(8,6),(6,9),(9,7)]))

BTree = ([1,2,3,4,5,6,7],
    [(4,2),(4,6),(2,1),(2,3),(6,5),(6,7)])

G = randomPos(gManta(4))
k = 100

while not done:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    screen.fill(WHITE)
    plotGraph(G, False)
    G = updatePos(G,k)
    k = updateK(G,k,width,height)
    pygame.display.flip()

pygame.quit()
'''
