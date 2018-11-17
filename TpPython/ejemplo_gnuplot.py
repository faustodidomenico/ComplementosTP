#! /usr/bin/python

# Para descargar py-gnuplot: http://sourceforge.net/projects/gnuplot-py/files/latest/download?source=files

import time
import Gnuplot

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
    time.sleep(3)    

if __name__ == "__main__":
    ejemplo_gnuplot()

