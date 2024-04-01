"""
Hola este es modulo principal,
el codigo que al ejecutar pondra en marcha nuestro juego
"""
import pygame, math, cProfile
import scenes.game as GameScene

'''Inicio la escena de mi juego'''
SCREEN_WIDTH = 1000  # revisar ancho de la imagen de fondo
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("assets/pixelBackground.jpg").convert()
pygame.font.init()
font = pygame.font.Font(None, 36) 
#menu


def main():
    while True:
    
        with open("score.txt", "r") as puntaje:
            score = puntaje.read()
            #print("score:", score)
            if score != "":
                tiempoMax = float(score)
                #print("tiempoMax:", tiempoMax)
            else:
                tiempoMax = 0

        screen.blit(background_image, [0, 0])

        text_surface = font.render("Presiona enter para jugar\nO esc para salir", True, (255, 255, 255))
        screen.blit(text_surface, (100, 350))

        text_surface = font.render("Record a vencer:", True, (255, 255, 255))
        screen.blit(text_surface, (600, 100))

        text_surface = font.render(str(tiempoMax), True, (255, 255, 255))
        screen.blit(text_surface, (600, 120))

        

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    GameScene.StartScene()
                if event.key == pygame.K_ESCAPE:
                    with open("score.txt", "w") as puntaje:
                        puntaje.write("")
                    #print("Se cerro el programa")
                    pygame.quit()
            elif event.type == pygame.QUIT:
                
                with open("score.txt", "w") as puntaje:
                    puntaje.write("")
                #print("Se cerro el programa")
                pygame.quit()
                

        pygame.display.flip()

cProfile.run("main()", sort="cumtime")
#main()