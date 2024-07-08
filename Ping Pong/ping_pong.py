# Juego de Ping - Pong usando pygame
import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla - podemos adaptarlo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

# Velocidad de la pelota
BALL_SPEED = 5
BALL_RADIUS = 10

# Velocidad de las paletas
PADDLE_SPEED = 7
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Inicialización de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Reloj para controlar la velocidad de actualización - es posible pensar en otras alternativas
clock = pygame.time.Clock()

# Función para dibujar las paletas
def draw_paddle(surface, color, x, y):
    pygame.draw.rect(surface, color, pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Función para dibujar la pelota
def draw_ball(surface, color, x, y):
    pygame.draw.circle(surface, color, (x, y), BALL_RADIUS)

# Función principal del juego
def main():
    # Posiciones iniciales de las paletas
    paddleA_x = 50
    paddleA_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddleB_x = SCREEN_WIDTH - 50 - PADDLE_WIDTH
    paddleB_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

    # Velocidades iniciales de las paletas
    paddleB_dy = 0

    # Posición inicial de la pelota
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = random.choice([-1, 1]) * BALL_SPEED
    ball_dy = random.choice([-1, 1]) * BALL_SPEED

    # Puntajes iniciales
    scoreA = 0
    scoreB = 0

    # Loop principal del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Control del jugador B (teclas arriba y abajo)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddleB_dy = -PADDLE_SPEED
                elif event.key == pygame.K_DOWN:
                    paddleB_dy = PADDLE_SPEED
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddleB_dy = 0

        # Movimiento automático del jugador A hacia la posición de la pelota - Enemigo
        if ball_dy > 0:
            if paddleA_y < ball_y - PADDLE_HEIGHT // 2:
                paddleA_y += PADDLE_SPEED
            elif paddleA_y > ball_y - PADDLE_HEIGHT // 2:
                paddleA_y -= PADDLE_SPEED

        # Movimiento de la paleta B
        paddleB_y += paddleB_dy
        paddleB_y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddleB_y))

        # Movimiento de la pelota
        ball_x += ball_dx
        ball_y += ball_dy

        # Colisiones de la pelota con las paredes superior e inferior
        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
            ball_dy *= -1

        # Acertar las colisiones de la pelota con las paletas
        if (paddleA_x + PADDLE_WIDTH >= ball_x - BALL_RADIUS >= paddleA_x and
            paddleA_y + PADDLE_HEIGHT >= ball_y >= paddleA_y):
            ball_dx *= -1
            scoreA += 1
        elif (paddleB_x <= ball_x + BALL_RADIUS <= paddleB_x + PADDLE_WIDTH and
              paddleB_y <= ball_y <= paddleB_y + PADDLE_HEIGHT):
            ball_dx *= -1
            scoreB += 1

        # Que pasa con la fuera de los límites izquierdo y derecho (punto marcado)
        if ball_x - BALL_RADIUS <= 0:
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_dx = BALL_SPEED
            ball_dy = random.choice([-1, 1]) * BALL_SPEED
            scoreB += 1
        elif ball_x + BALL_RADIUS >= SCREEN_WIDTH:
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_dx = -BALL_SPEED
            ball_dy = random.choice([-1, 1]) * BALL_SPEED
            scoreA += 1

        # Para dibujar los elementos en la pantalla
        screen.fill(GREEN)
        draw_paddle(screen, WHITE, paddleA_x, paddleA_y)
        draw_paddle(screen, WHITE, paddleB_x, paddleB_y)
        draw_ball(screen, WHITE, int(ball_x), int(ball_y))

        # Tenemos los puntajes en la pantalla
        font = pygame.font.Font(None, 36)
        text = font.render(f"Player A: {scoreA}    Player B: {scoreB}", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 10))

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlamos la velocidad del juego
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
