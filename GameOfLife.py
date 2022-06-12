import pygame
import numpy as np
import time
import random as rm

"""
Este es el Juego de la Vida de John Conway
Más información:  https://twitter.com/pablogilah/status/1249296043612737536/
Nuevas versiones:  https://github.com/pablogila/GameOfLife/

Ayuda de teclas:
- CLIC:      cambiar estado de la celda
- ESPACIO:   Pausa
- T:         Cambiar velocidad

########   VARIABLES QUE PUEDES CAMBIAR:   ########"""
# Tamaño del tablero, en celdas
nxC, nyC = 70, 70
# Alto y ancho de la pantalla, en píxeles
height, width= 650, 650
# Color de fondo, en RGB (0-255)
bg = 0, 51, 160
# Tiempo entre ciclos, en segundos (pulsar la tecla T alterna entre este t y máxima velocidad)
t = 0.1
"""#################################################"""


# Creamos la pantalla del juego con pygame
pygame.init()
# Titulo de la pantalla
pygame.display.set_caption("El Juego de la Vida")
# Creamos la pantalla
screen = pygame.display.set_mode((width, height))
# Pintamos el fondo
screen.fill(bg)
# Se calcula el tamaño de cada celda
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1, Muertas = 0
# En el estado inicial, las celdas están vivas o muertas aleatoriamente
gameState = np.zeros((nxC, nyC))
for x in range(nxC):  # Loop over every possible column.
    for y in range(nyC):  # Loop over every possible row.
    # 50/50 chance for starting cells being alive or dead.
        if rm.randint(0, 1) == 1:
            gameState[x][y] = 1
        else:
            gameState[x][y] = 0

# Control de la ejecución
pause = False

# Bucle de ejecución
while True:

    # Hacemos una copia del estado anterior del juego
    newGameState = np.copy(gameState)
    # Limpiamos la pantalla
    screen.fill(bg)
    # Velocidad
    time.sleep(t)

    # Registramos eventos de teclado
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            # Detectamos si se pulsa espacio para pausar el juego
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_t:
                if t == 0.1:
                    t = 0
                else: t = 0.1
    # Detectamos si se cierra la pestaña para cerrar el juego
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    # Detectamos si pulsa el ratón
    mouseClick = pygame.mouse.get_pressed()
    if sum(mouseClick) > 0:
        posX, posY = pygame.mouse.get_pos()
        celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
        # Cambiamos el estado de la celda
        newGameState[celX, celY] = not newGameState[celX, celY]

    # Recorremos todas las celdas
    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pause:
                # Calculamos el número de vecinos cercanos, con una estructura toroidal
                # (Toroidal significa que los bordes se conectan unos con otros)
                n_neigh =   gameState[(x-1) % nxC, (y-1) % nyC] + \
                            gameState[  (x) % nxC, (y-1) % nyC] + \
                            gameState[(x+1) % nxC, (y-1) % nyC] + \
                            gameState[(x-1) % nxC,   (y) % nyC] + \
                            gameState[(x+1) % nxC,   (y) % nyC] + \
                            gameState[(x-1) % nxC, (y+1) % nyC] + \
                            gameState[  (x) % nxC, (y+1) % nyC] + \
                            gameState[(x+1) % nxC, (y+1) % nyC]

                # Regla 1
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla 2
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Definimos las coordenadas de los rectángulos
            poly = [(    (x) * dimCW,       y * dimCH),
                    ((x + 1) * dimCW,       y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (    (x) * dimCW, (y + 1) * dimCH)]
            # Dibujamos la celda para cada par de x e y
            if newGameState[x, y] == 0:
                color = 255, 255, 255
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            # Dibujamos las celdas vivas
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)
    # Actualizamos la pantalla
    pygame.display.flip()
