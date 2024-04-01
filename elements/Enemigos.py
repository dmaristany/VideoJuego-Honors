"""
Hola este es modulo Bug,
este modulo manejara la creacion y acciones de los Bugs
"""
import pygame, math
import random
from pygame.locals import (RLEACCEL)
from elements.bullet import Bullet


class EnemigoPower(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, vida = 3):
        # nos permite invocar métodos o atributos de Sprite
        super(EnemigoPower, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((0, 255, 0))
        #self.surf.set_colorkey((0, 255, 0), RLEACCEL)
        self.vida = int(vida)
        self.vidaMax = int(vida)
        self.exp_reward = 20

        # X
        minPosX = -100
        minExcludeX = 0
        maxPosX = SCREEN_WIDTH + 100
        maxExcludeX = SCREEN_WIDTH

        # Y
        minPosY = -100
        minExcludeY = 0
        maxPosY = SCREEN_HEIGHT + 100
        maxExcludeY = SCREEN_HEIGHT

        while True:
            posX = random.randint(minPosX, maxPosX)
            posY = random.randint(minPosY, maxPosY)
            if not (minExcludeX < posX < maxExcludeX and minExcludeY < posY < maxExcludeY):
                break


        self.rect = self.surf.get_rect(
            center=(
                posX,
                posY,
            )
        )
        self.speed = random.randint(1, 2)

        self.SCREEN_WIDTH = SCREEN_WIDTH   
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.balas = pygame.sprite.Group()

    def update(self, playerX, playerY):
        #Vida
        self.surf.fill((int(255 * (int(self.vidaMax)-int(self.vida))/int(self.vidaMax)), int(255 * (int(self.vida) / int(self.vidaMax))), 0))

        #Movimiento
        dx = playerX - self.rect.x
        dy = playerY - self.rect.y
        norm = math.sqrt(dx ** 2 + dy ** 2)
        dx = dx / norm
        dy = dy / norm

        self.rect.move_ip(dx * self.speed, dy * self.speed)
        

        if self.rect.right < -150 or self.rect.left > self.SCREEN_WIDTH + 150 or self.rect.bottom < -150 or self.rect.top > 150 + self.SCREEN_HEIGHT:
            self.kill()

        if pygame.time.get_ticks() % 1000 >= 900:
            new_bullet = Bullet(self.rect.x, self.rect.y, dx, dy, "enemigo", 1.2)
            self.balas.add(new_bullet)

            
            

