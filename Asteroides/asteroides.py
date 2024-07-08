# Propuesta 1

import random
import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_SPACE

### SETUP *********************************************************************
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 500

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Asteroides - Nombre Apellido del alumno')

# Cargar imágenes
rocket_image = pygame.image.load('assets/rocket.png').convert()
asteroid_image = pygame.image.load('assets/asteroids/asteroid1.png').convert()
bullet_image = pygame.image.load('assets/bullets/b1.png').convert()
explosion_image = pygame.image.load('assets/explosion/explosion0.png').convert()

font = pygame.font.Font('freesansbold.ttf', 32)

### Objetos & Eventos **********************************************************
class Rocket(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.image = rocket_image
        self.rect = self.image.get_rect()
        self.rect.center = (size[0] // 2, size[1] - 50)  #Inicio del cohete

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        # Limitar los movimientos de los asteroides
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SIZE[0])

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image, size):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, size[0] - self.rect.width)
        self.rect.y = random.randint(-self.rect.height * 2, -self.rect.height)  # Start above the screen

    def update(self):
        self.rect.y += 2  # Mover los asteroides hacia el cohete

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos, direction):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.direction = direction

    def update(self):
        self.rect.y -= 5  # Mover los disparos hacia arriba
        if self.rect.bottom < 0:
            self.kill()  # quitar las balas fuera de los lìmites

### Juego **********************************************************************
if __name__ == '__main__':
    score = 0
    running = True
    gameStarted = False

    rocket = Rocket(SIZE)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(rocket)

    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    ADD_ASTEROID = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_ASTEROID, 3000)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if not gameStarted and event.key == K_SPACE:
                    gameStarted = True

                # Disparar balas con la tecla espaciadora
                if event.key == K_SPACE and gameStarted:
                    pos = rocket.rect.midtop  # Posición de la punta de la nave
                    bullet = Bullet(bullet_image, pos, -1)  # Dirección -1 para disparar hacia arriba
                    bullets.add(bullet)
                    all_sprites.add(bullet)

            if event.type == ADD_ASTEROID and gameStarted:
                asteroid = Asteroid(asteroid_image, SIZE)
                asteroids.add(asteroid)
                all_sprites.add(asteroid)

        pressed_keys = pygame.key.get_pressed()
        rocket.update(pressed_keys)

        asteroids.update()
        bullets.update()

        win.fill((0, 0, 0))  # Limpiar la pantalla

        all_sprites.draw(win)

        # Colisiones
        for bullet in bullets:
            collision = pygame.sprite.spritecollide(bullet, asteroids, True)
            if collision:
                score += 1  # Sumar un punto por cada asteroide destruido - se puede modificar
                bullet.kill()

        # Colisión de la nave con los asteroides
        if pygame.sprite.spritecollideany(rocket, asteroids):
            rocket.kill()
            score = 0
            for sprite in all_sprites:
                sprite.kill()
            all_sprites.empty()
            rocket = Rocket(SIZE)
            all_sprites.add(rocket)
            gameStarted = False

        text = font.render('Puntaje : ' + str(score), 1, (200, 255, 0))
        win.blit(text, (340, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
