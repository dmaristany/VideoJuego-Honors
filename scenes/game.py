'''
Hola este es modulo game,
este modulo manejara la escena donde ocurre nuestro juego
'''
import time
import pygame, math, random

from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT)

from elements.jorge import Player
from elements.bug import Enemy
from elements.bullet import Bullet
from elements.Enemigos import EnemigoPower



pygame.font.init()
font = pygame.font.Font(None, 36)  

SCREEN_WIDTH = 1000  # revisar ancho de la imagen de fondo
SCREEN_HEIGHT = 700 

def StartScene():

    from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL, K_SPACE, K_RETURN)
    pygame.mixer.init()
    pygame.mixer.music.load("assets/Hitman(chosic.com).mp3")
    pygame.mixer.music.play(-1)

    """
    Hitman by Kevin MacLeod | https://incompetech.com/
    Music promoted by https://www.chosic.com/free-music/all/
    Creative Commons CC BY 3.0
    https://creativecommons.org/licenses/by/3.0/
    """


    with open("score.txt", "r") as puntaje:
        score = puntaje.read()
        if score:
            tiempoMax = float(score)
        else:
            try:
                tiempoMax = float(score)
            except:
                tiempoMax = 0
    ''' iniciamos los modulos de pygame'''
    pygame.init()

    ''' Creamos y editamos la ventana de pygame (escena) '''
    ''' 1.-definir el tamaño de la ventana'''
    SCREEN_WIDTH = 1000  # revisar ancho de la imagen de fondo
    SCREEN_HEIGHT = 700  # revisar alto de la imagen de fondo

    ''' 2.- crear el objeto pantalla'''
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load("assets/pixelBackground.jpg").convert()

    ''' Preparamos el gameloop '''
    ''' 1.- creamos el reloj del juego'''
    clock = pygame.time.Clock()

    ''' 2.- generador de enemigos'''
    ENEMYTIMER = 1000
    TimeBoostOrder = 0

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, int(ENEMYTIMER*0.6))

    ADDPOWERRFULL = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDPOWERRFULL, int(ENEMYTIMER))

    velocidadEnemigoAzul = 3
    vidaEnemigoVerde = 3

    ''' 3.- creamos la instancia de jugador'''
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    Ability_use_time = 0
    exp_requirments = [10, 20, 300, 600, 1200, 2000, 3000, 5000, 5000, 10000000000]


    ''' 4.- contenedores de enemigos y jugador'''
    enemies = pygame.sprite.Group()

    ''' 5.- generamos el evento de agregar enemigos'''
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    #Disparo periodico
    #tiempo = 200
    DISPARO = pygame.USEREVENT + 2
    pygame.time.set_timer(DISPARO, player.attack_speed)
    Bullets = pygame.sprite.Group()

    DisparoArma = True
    count = 10
    countCanon = 0
    countCirculo = 0


    ''' hora de hacer el gameloop '''

    start_ticks = pygame.time.get_ticks()

    running = True
    while running:

        screen.blit(background_image, [0, 0])

        #Cambios dependientes del tiempo, ojo el orden de los if

        if (pygame.time.get_ticks() - start_ticks) / 15000 > TimeBoostOrder + 1 and TimeBoostOrder < 3:
            print("se puso dificil la wea")
            TimeBoostOrder += 1
            ENEMYTIMER -= 30

            if ENEMYTIMER < 200:
                ENEMYTIMER = 200

            pygame.time.set_timer(ADDENEMY, int(ENEMYTIMER*0.6))
            pygame.time.set_timer(ADDPOWERRFULL, int(ENEMYTIMER))

            vidaEnemigoVerde += 1
            velocidadEnemigoAzul += 1.5
        if pygame.time.get_ticks() - start_ticks > 40000 and TimeBoostOrder == 2:
            TimeBoostOrder = 3
            ENEMYTIMER = 250
            pygame.time.set_timer(ADDENEMY, int(ENEMYTIMER*0.6))
            pygame.time.set_timer(ADDPOWERRFULL, int(ENEMYTIMER))

            vidaEnemigoVerde = 4
            velocidadEnemigoAzul = 4
        elif pygame.time.get_ticks() - start_ticks > 20000 and TimeBoostOrder == 1:
            TimeBoostOrder = 2
            ENEMYTIMER = 300
            pygame.time.set_timer(ADDENEMY, int(ENEMYTIMER*0.6))
            pygame.time.set_timer(ADDPOWERRFULL, int(ENEMYTIMER))
        elif pygame.time.get_ticks() - start_ticks > 10000 and TimeBoostOrder == 0:
            TimeBoostOrder = 1
            ENEMYTIMER = 500
            pygame.time.set_timer(ADDENEMY, int(ENEMYTIMER*0.6))
            pygame.time.set_timer(ADDPOWERRFULL, int(ENEMYTIMER))
        

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        text_surface = font.render('Time: ' + str(seconds), True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))


        # Dibuja la vida del jugador
        pygame.draw.rect(screen, (0, 0, 0), (player.rect.x -11, player.rect.y + 30, 47, 5), 1)
        pygame.draw.rect(screen, (255, 0, 0), (player.rect.x - 11, player.rect.y + 30, 47 * (player.vida / player.maxVida), 5))

        #check player nivel
        if player.exp >= exp_requirments[player.nivel]:
            player.nivel += 1
            player.exp = 0
            player.vida += 1
            player.maxVida += 1
            #player.maxVida += 1
            #player.bullet_speed += 50

            #pause menu
            from elements.mejoras import AttackeRapido, BalasRapidas, MasVida, LifeRegen, dibujar
            mejoras = [AttackeRapido, BalasRapidas, MasVida, LifeRegen]
            seleccionado = 0
            NoSeHaSeleccionado = True

            sel1 = random.randint(0, len(mejoras) - 1)
            sel2 = random.randint(0, len(mejoras) - 1)
            sel3 = random.randint(0, len(mejoras) - 1)

            while NoSeHaSeleccionado:
                screen.fill((0, 0, 0))  # Fill the screen with black (optional)
        
                transparent_copy = screen_copy
                transparent_copy.set_alpha(40)
                screen.blit(transparent_copy, (0, 0))

                #Seleccionamos 3 opciones
                Primero = mejoras[sel1]
                Segundo = mejoras[sel2]
                Tercero = mejoras[sel3] 

                #Dibujamos las opciones 
                Primero(1, screen)
                Segundo(2, screen)
                Tercero(3, screen)

                from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL, K_SPACE, K_RETURN)

                
                        
                # Handle events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        from elements.AsignarSeleccionado import AsignarSeleccionado

                        if event.key == K_LEFT:
                            seleccionado = (seleccionado - 1) % 3
                        elif event.key == K_RIGHT:
                            seleccionado = (seleccionado + 1) % 3

                        elif event.key == K_RETURN or event.key == K_SPACE:
                            if seleccionado == 0:
                                AsignarSeleccionado(Primero,player)
                            elif seleccionado == 1:
                                AsignarSeleccionado(Segundo, player)
                            elif seleccionado == 2:
                                AsignarSeleccionado(Tercero, player)
                            
                            NoSeHaSeleccionado = False
                            break
                            
                            
                        
                        time.sleep(0.2)
                


                #reajustar cosas despues de mejoras
                pygame.time.set_timer(DISPARO, player.attack_speed)

                if seleccionado == 0:
                    pygame.draw.rect(screen, (255, 215, 0), (200, 200, 100, 300), 5)
                elif seleccionado == 1:
                    pygame.draw.rect(screen, (255, 215, 0), (450, 200, 100, 300), 5)
                elif seleccionado == 2:
                    pygame.draw.rect(screen, (255, 215, 0), (700, 200, 100, 300), 5)
                

                pygame.display.flip()  # Update the display to show the pause menu

            habilidades = ["TP", "explosion", "Curacion"]
            
            if player.nivel ==  1:
                NoSeHaSeleccionado = True

                while NoSeHaSeleccionado:
                    screen.fill((0, 0, 0))  # Fill the screen with black (optional)
        
                    transparent_copy = screen_copy
                    transparent_copy.set_alpha(40)
                    screen.blit(transparent_copy, (0, 0))

                    #Seleccionamos 3 opciones
                    Primero = habilidades[0]
                    Segundo = habilidades[1]
                    Tercero = habilidades[2] 

                    #Dibujamos las opciones 

                    dibujar(1, screen, image=pygame.image.load("assets/TP.png"))
                    dibujar(2, screen, image=pygame.image.load("assets/explosion.png"))
                    dibujar(3, screen, image=pygame.image.load("assets/escudo.png"))


                    

                    
                            
                    # Handle events
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            from elements.AsignarSeleccionado import AsignarSeleccionado

                            if event.key == K_LEFT:
                                seleccionado = (seleccionado - 1) % 3
                            elif event.key == K_RIGHT:
                                seleccionado = (seleccionado + 1) % 3

                            elif event.key == K_RETURN or event.key == K_SPACE:
                                if seleccionado == 0:
                                    player.habilidad = "TP"
                                elif seleccionado == 1:
                                    player.habilidad = "explosion"
                                    player.habilidad_wait_time = 30
                                elif seleccionado == 2:
                                    player.habilidad = "escudo"
                                    player.habilidad_wait_time = 50
                                
                                NoSeHaSeleccionado = False
                                break
                                
                                
                            
                            time.sleep(0.2)
                    


                    #reajustar cosas despues de mejoras
                    pygame.time.set_timer(DISPARO, player.attack_speed)

                    if seleccionado == 0:
                        pygame.draw.rect(screen, (255, 215, 0), (200, 200, 100, 300), 5)
                    elif seleccionado == 1:
                        pygame.draw.rect(screen, (255, 215, 0), (450, 200, 100, 300), 5)
                    elif seleccionado == 2:
                        pygame.draw.rect(screen, (255, 215, 0), (700, 200, 100, 300), 5)
                    

                    pygame.display.flip()  # Update the display to show the pause menu
            
            if player.nivel ==  2:
                from elements.menuUpgrades import menuUpgrades

                menuUpgrades(screen, screen_copy, player, DISPARO)






        #draw xp bar
        pygame.draw.rect(screen, (0, 0, 255), (250, 10, 500, 15), 1)
        pygame.draw.rect(screen, (0, 0, 255), (250, 10, 500 * (player.exp/exp_requirments[player.nivel]), 15))

        text_surface = font.render('Nivel: ' + str(player.nivel + 1), True, (255, 255, 255))
        #text_surface.set_alpha(128)
        screen.blit(text_surface, (450, 30))
       

        pressed_keys = pygame.key.get_pressed()


        player.update(pressed_keys)
        enemies.update(player.rect.x, player.rect.y)

        nearest_enemy = None
        nearest_distance = None

        NormalizedX = 0
        NormalizedY = 0

        for enemy in enemies:
            dx = player.rect.x - enemy.rect.x  
            dy = player.rect.y - enemy.rect.y  
            distance = math.sqrt(dx**2 + dy**2)  

            if nearest_distance is None or distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy
                NormalizedX = -dx / (dx*dx + dy*dy)
                NormalizedY = -dy / (dx*dx + dy*dy)

        if pygame.sprite.spritecollideany(player, enemies):
            
            if player.vida > 1:
                player.vida -= 1
                player.rect.x -= NormalizedX * 50
                player.rect.y -= NormalizedY * 50

                player.exp += 1

                enemies.remove(nearest_enemy)
                all_sprites.remove(nearest_enemy)

            else:
                if seconds > tiempoMax:
                    tiempoMax = seconds
                    with open("score.txt", "w") as puntaje:
                        puntaje.write(str(seconds))
                player.kill()
                CharacterDeath()
                running = False
                pygame.mixer.music.stop()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    
                    if player.habilidad_usable:

                        if player.habilidad == "TP":
                            from elements.habilidades import TP

                            posi = TP(screen_copy, screen)

                            player.rect.x = posi[0]
                            player.rect.y = posi[1]
                        
                        elif player.habilidad == "explosion":
                            player.habilidad_activa = True
                            tiempo_de_explosion = pygame.time.get_ticks() - start_ticks  # tiempo de la explosion

                        
                        elif player.habilidad == "escudo":
                            player.habilidad_activa = True
                            player.vida += 5
                            player.maxVida += 5
                            player.life_regen = player.life_regen * 2
                            tiempo_de_curacion = pygame.time.get_ticks() - start_ticks


                        Ability_use_time = pygame.time.get_ticks()
                        player.habilidad_usable = False

            elif event.type == QUIT:
                running = False
            
            elif event.type == ADDENEMY:
                new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, velocidadEnemigoAzul)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
            elif event.type == ADDPOWERRFULL:
                if pygame.time.get_ticks() - start_ticks > 1000:
                    new_enemy = EnemigoPower(SCREEN_WIDTH, SCREEN_HEIGHT, int(vidaEnemigoVerde))
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
            
            elif event.type == DISPARO:
                if len(enemies) > 2 and (NormalizedX, NormalizedY) != (0, 0):
                    new_bullet = Bullet(player.rect.x, player.rect.y, NormalizedX * player.bullet_speed, NormalizedY * player.bullet_speed)
                    Bullets.add(new_bullet)
                    all_sprites.add(new_bullet)
                
                if player.arma == "Cruz" and DisparoArma:
                    new_bullet = Bullet(player.rect.x, player.rect.y, 0, 0.01 * player.bullet_speed)
                    Bullets.add(new_bullet)
                    all_sprites.add(new_bullet)

                    new_bullet = Bullet(player.rect.x, player.rect.y, 0, 0.01 * -player.bullet_speed)
                    Bullets.add(new_bullet)
                    all_sprites.add(new_bullet)

                    new_bullet = Bullet(player.rect.x, player.rect.y, 0.01 * player.bullet_speed, 0)
                    Bullets.add(new_bullet)
                    all_sprites.add(new_bullet)

                    new_bullet = Bullet(player.rect.x, player.rect.y, 0.01 * -player.bullet_speed, 0)
                    Bullets.add(new_bullet)
                    all_sprites.add(new_bullet)

                if player.arma == "Canon" and DisparoArma and countCanon == 0:
                    print("Canon fue iniciado")
                    tiempo_de_explosion_canon = pygame.time.get_ticks()
                    count = 1
                    countCanon = 1
                    cordx = random.randint(0, SCREEN_WIDTH)
                    cordy = random.randint(0, SCREEN_HEIGHT)
                
                elif player.arma == "circulo" and DisparoArma and countCirculo == 0:
                    tiempo_de_explosion_circulo = pygame.time.get_ticks()
                    count = 1
                    countCirculo = 1
                    cordx = player.rect.centerx
                    cordy = player.rect.centery


                if player.arma == "Cruz":
                    if 0 < count < 10:
                        count += 1
                    else:
                        DisparoArma = True
                        count = 0
                
                if player.arma == "Canon":
                    if 0 < countCanon < 50:
                        countCanon += 1
                        print(countCanon)
                    else:
                        countCanon = 0
                        DisparoArma = True
                
                if player.arma == "circulo":
                    if ENEMYTIMER == 200:
                        if 0 < countCirculo < 300:
                            countCirculo += 1
                            print(countCirculo)
                        else:
                            countCirculo = 0
                            DisparoArma = True
                    elif ENEMYTIMER <= 300:
                        if 0 < countCirculo < 200:
                            countCirculo += 1
                            print(countCirculo)
                        else:
                            countCirculo = 0
                            DisparoArma = True
                    else:
                        if 0 < countCirculo < 100:
                            countCirculo += 1
                            print(countCirculo)
                        else:
                            countCirculo = 0
                            DisparoArma = True
                
        
        for bullet in Bullets:
            bullet.update()

            bnearest_enemy = None
            bnearest_distance = None
            for enemy in enemies:
                bdx = bullet.rect.x - enemy.rect.x  # difference in x coordinates
                bdy = bullet.rect.y - enemy.rect.y  # difference in y coordinates
                bdistance = math.sqrt(bdx**2 + bdy**2)  # Pythagorean theorem

                if bnearest_distance is None or bdistance < bnearest_distance:
                    bnearest_distance = bdistance
                    bnearest_enemy = enemy

            if pygame.sprite.spritecollideany(bullet, enemies):
                bullet.kill()

                if bnearest_enemy.vida > 0:
                    bnearest_enemy.vida -= 1
                else:
                    player.exp += bnearest_enemy.exp_reward


                    bnearest_enemy.kill()
                    enemies.remove(bnearest_enemy)
                    all_sprites.remove(bnearest_enemy)
                

        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

            if isinstance(entity, EnemigoPower):

                for bulletEnemiga in entity.balas:
                    bulletEnemiga.update()
                    screen.blit(bulletEnemiga.surf, bulletEnemiga.rect)

                    if pygame.sprite.spritecollideany(player, entity.balas):

                        if player.vida > 0:
                            player.vida -= 1

                            entity.balas.empty()
                        
                        else:
                            if seconds > tiempoMax:
                                tiempoMax = seconds
                                with open("score.txt", "w") as puntaje:
                                    puntaje.write(str(seconds))
                            player.kill()
                            CharacterDeath()
                            running = False
                            pygame.mixer.music.stop()

        """for sprite in all_sprites:  # Assuming all_sprites is a Group containing all your sprites
            pygame.draw.rect(screen, (255, 0, 0), sprite.rect, 2)  # Draw a red rectangle with a thickness of 2"""

        #Larga vida al jank
        #problema: hay enemigos afuera de pantalla que son inalcansables, toco matarlos periodicamente 
        if (pygame.time.get_ticks() - start_ticks) % 10000 == 0 or len(enemies) > 50:
            print(len(enemies))
            for enemy in enemies:
                if enemy.rect.x < 0 or enemy.rect.x > SCREEN_WIDTH - 10 or enemy.rect.y < 0 or enemy.rect.y > SCREEN_HEIGHT - 10:
                    enemy.kill()
                    enemies.remove(enemy)
                    all_sprites.remove(enemy)
            print("Exterminados", len(enemies))

        
        if player.habilidad_wait_time * 1000 < (pygame.time.get_ticks() - Ability_use_time):
            player.habilidad_usable = True
        
        if player.habilidad_usable:
            pygame.draw.rect(screen, (0, 255, 0), (980, 680, 20, 20))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (980, 680, 20, 20))
            progress = (pygame.time.get_ticks() - Ability_use_time) / (player.habilidad_wait_time * 1000) * 20

            pygame.draw.rect(screen, (0, 255, 0), (980, 680, progress, 20))
            

            
        

        if player.habilidad_activa and player.habilidad == "explosion":
            player.habilidad_usable = False
            explosion_radius = (pygame.time.get_ticks() - tiempo_de_explosion) / 1000 * 30
            pygame.draw.circle(screen, (255, 0, 0), player.rect.center, explosion_radius)
            for enemy in enemies:
                dx = player.rect.centerx - enemy.rect.centerx
                dy = player.rect.centery - enemy.rect.centery
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= explosion_radius:
                    player.exp += enemy.exp_reward
                    enemy.kill()
                    enemies.remove(enemy)
                    all_sprites.remove(enemy)

            

            # Randomly draw small flame colored dots inside the radius
            num_dots = int((pygame.time.get_ticks() - tiempo_de_explosion) / 1000)  # Number of dots increases with time
            for flame in range(num_dots):
                dot_radius = random.randint(1, 3)
                dot_x = random.uniform(player.rect.centerx - explosion_radius, player.rect.centerx + explosion_radius)
                dot_y = random.uniform(player.rect.centery - explosion_radius, player.rect.centery + explosion_radius)
                pygame.draw.circle(screen, (255, 165, 0), (dot_x, dot_y), dot_radius)
            
            if pygame.time.get_ticks() - tiempo_de_explosion  > 5000:
                player.habilidad_activa = False
                Ability_use_time = pygame.time.get_ticks()
        

        
        
        elif player.habilidad_activa and player.habilidad == "escudo":
            num_dots = 10  # Number of dots increases with time
            for cura in range(num_dots):
                dot_radius = random.randint(1, 3)
                dot_x = random.uniform(player.rect.centerx - 20, player.rect.centerx + 20)
                dot_y = random.uniform(player.rect.centery - 20, player.rect.centery + 20)
                pygame.draw.circle(screen, (0, 165, 0), (dot_x, dot_y), dot_radius)

            if pygame.time.get_ticks() - tiempo_de_curacion  > 5000:
                player.habilidad_activa = False
                Ability_use_time = pygame.time.get_ticks()

        print(player.arma, DisparoArma, countCanon)
        if player.arma == "Canon" and DisparoArma and countCanon != 0:
            print("Canon lanzado")
            explosion_radius = (pygame.time.get_ticks() - tiempo_de_explosion_canon) / 1000 * 10
            pygame.draw.circle(screen, (255, 0, 0), (cordx, cordy) , explosion_radius)
            for enemy in enemies:
                dx = cordx - enemy.rect.centerx
                dy = cordy - enemy.rect.centery
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= explosion_radius:
                    player.exp += enemy.exp_reward

                    enemy.vida -= 1

                    if enemy.vida <= 0:
                        enemy.kill()
                        enemies.remove(enemy)
                        all_sprites.remove(enemy)
            
            if pygame.time.get_ticks() - tiempo_de_explosion_canon > 5000:
                print("canon disparado")
                DisparoArma = False
                tiempo_de_explosion_canon = 0
                countCanon = 1

        elif player.arma == "circulo" and DisparoArma and countCirculo != 0:
            explosion_radius = (pygame.time.get_ticks() - tiempo_de_explosion_circulo) / 1000 * 50
            pygame.draw.circle(screen, (0, 255, 0), (cordx, cordy), explosion_radius, 1)
            for enemy in enemies:
                dx = cordx - enemy.rect.centerx
                dy = cordy - enemy.rect.centery
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= explosion_radius:
                    enemy.vida -= 1

                    if enemy.vida <= 0:
                        player.exp += enemy.exp_reward

                        enemy.kill()
                        enemies.remove(enemy)
                        all_sprites.remove(enemy)

            for entity in all_sprites:
                if isinstance(entity, EnemigoPower):
                    
                    for bulletEnemiga in entity.balas:
                        dx = cordx - bulletEnemiga.rect.centerx
                        dy = cordy - bulletEnemiga.rect.centery
                        distance = math.sqrt(dx**2 + dy**2)
                        if  explosion_radius - 10 <= distance <= explosion_radius + 10:
                            bulletEnemiga.kill()

            
            if pygame.time.get_ticks() - tiempo_de_explosion_circulo > 10000:
                print("circulo disparado")
                DisparoArma = False
                tiempo_de_explosion_circulo = 0
                countCirculo = 1

        clock.tick(40)
        screen_copy = screen.copy()
        pygame.display.flip()

        
def CharacterDeath():
    runing = True
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while runing:
        text_surface = font.render("Has muerto", True, (255, 255, 255))

        screen.fill((0, 0, 0))
        screen.blit(text_surface, (100, 350))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    runing = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            elif event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.flip()
    
