import random
import math
from pygame import Rect
import pgzrun

WIDTH = 800
HEIGHT = 600

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
LASER_WIDTH = 8
LASER_HEIGHT = 16

MENU = 0
GAME = 1
PAUSE = 2
GAME_OVER = 3
state = MENU

player = None
enemies = []
projectiles = []
speed = 8
score = 0
lives = 3
music_enabled = True

pause_button = Rect((WIDTH - 60, 10, 50, 30))

def draw_menu():
    screen.clear()
    screen.blit("background_game1", (0, 0))
    screen.draw.text("Space Invaders", (WIDTH // 2 - 150, 100), fontsize=60, color="white")
    screen.draw.text("Começar o jogo", (WIDTH // 2 - 100, 300), fontsize=40, color="white")
    screen.draw.text(f"Música: {'Ligada' if music_enabled else 'Desligada'}", (WIDTH // 2 - 100, 350), fontsize=40, color="white")
    screen.draw.text("Sair", (WIDTH // 2 - 100, 400), fontsize=40, color="white")

def handle_menu_click(pos):
    global state, music_enabled, player, enemies, projectiles, score, lives
    if 300 <= pos[1] <= 340:
        state = GAME
        player = Actor("nave-player", (WIDTH // 2, HEIGHT - 50))
        enemies = []
        projectiles = []
        score = 0
        lives = 3
        clock.schedule_interval(spawn_enemy, 2.0)
        if music_enabled:
            music.play("music_background")
    elif 350 <= pos[1] <= 390:
        music_enabled = not music_enabled
        if music_enabled and state == GAME:
            music.play("music_background")
        else:
            music.stop()
    elif 400 <= pos[1] <= 440:
        exit()

def spawn_enemy():
    x = random.randint(50, WIDTH - 50)
    enemy = Actor("nave-espacial", (x, -50))
    enemies.append(enemy)

def update():
    global score, lives, state
    if state == PAUSE:
        return

    if keyboard.left and player.x > 40:
        player.x -= speed
    if keyboard.right and player.x < WIDTH - 40:
        player.x += speed

    for enemy in enemies:
        enemy.y += 1.5
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            lives -= 1
            if lives <= 0:
                state = GAME_OVER
                clock.unschedule(spawn_enemy)
                music.stop()

    for projectile in projectiles:
        projectile.y -= 12
        if projectile.y < 0:
            projectiles.remove(projectile)

    for enemy in enemies[:]:
        for projectile in projectiles[:]:
            if enemy.colliderect(projectile):
                enemies.remove(enemy)
                projectiles.remove(projectile)
                score += 10

    if lives <= 0:
        state = GAME_OVER
        clock.unschedule(spawn_enemy)
        music.stop()

def on_key_down(key):
    global state
    if key == keys.SPACE:
        if state == GAME:
            projectile = Actor("bala_player", (player.x, player.y - 20))
            projectiles.append(projectile)

def draw_game():
    screen.clear()
    screen.blit("background_game1", (0, 0))
    player.draw()
    for enemy in enemies:
        enemy.draw()
    for projectile in projectiles:
        projectile.draw()
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Lives: {lives}", (10, 40), fontsize=30, color="white")
    pause_button = Rect((WIDTH - 60, 10, 50, 30))
    screen.draw.filled_rect(pause_button, (200, 200, 200))
    screen.draw.text("Pausa", (WIDTH - 55, 15), fontsize=20, color="black")

def draw_pause():
    screen.surface.fill((0, 0, 0, 128))
    screen.draw.filled_rect(Rect((WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)), (50, 50, 50))
    screen.draw.text("Jogo Pausado", (WIDTH // 2 - 150, HEIGHT // 4 + 50), fontsize=60, color="white")
    screen.draw.text("Retomar", (WIDTH // 2 - 100, HEIGHT // 4 + 150), fontsize=40, color="white")
    screen.draw.text(f"Música: {'Ligada' if music_enabled else 'Desligada'}", (WIDTH // 2 - 100, HEIGHT // 4 + 200), fontsize=40, color="white")
    screen.draw.text("Sair", (WIDTH // 2 - 100, HEIGHT // 4 + 250), fontsize=40, color="white")

def draw_game_over():
    screen.clear()
    screen.surface.fill((0, 0, 0, 128))
    screen.draw.filled_rect(Rect((WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)), (50, 50, 50))
    screen.draw.text("Game Over", (WIDTH // 2 - 150, HEIGHT // 4 + 50), fontsize=60, color="white")
    screen.draw.text(f"Score: {score}", (WIDTH // 2 - 100, HEIGHT // 4 + 150), fontsize=40, color="white")
    screen.draw.text("Jogar Novamente", (WIDTH // 2 - 100, HEIGHT // 4 + 200), fontsize=40, color="white")
    screen.draw.text("Sair", (WIDTH // 2 - 100, HEIGHT // 4 + 250), fontsize=40, color="white")

def handle_pause_click(pos):
    global state, music_enabled
    if 300 <= pos[1] <= 340:
        state = GAME
        if music_enabled:
            music.play("music_background")
    elif 350 <= pos[1] <= 390:
        music_enabled = not music_enabled
        if music_enabled and state == GAME:
            music.play("music_background")
        else:
            music.stop()
    elif 400 <= pos[1] <= 440:
        state = MENU
        clock.unschedule(spawn_enemy)
        music.stop()

def handle_game_over_click(pos):
    global state, player, enemies, projectiles, score, lives
    if 350 <= pos[1] <= 390:
        state = GAME
        player = Actor("nave-player", (WIDTH // 2, HEIGHT - 50))
        enemies = []
        projectiles = []
        score = 0
        lives = 3
        clock.schedule_interval(spawn_enemy, 2.0)
        music.play("music_background")
    elif 400 <= pos[1] <= 440:
        exit()

def draw():
    if state == MENU:
        draw_menu()
    elif state == GAME:
        draw_game()
    elif state == PAUSE:
        draw_pause()
    elif state == GAME_OVER:
        draw_game_over()

def on_mouse_down(pos):
    global state
    if state == MENU:
        handle_menu_click(pos)
    elif state == PAUSE:
        handle_pause_click(pos)
    elif state == GAME and pause_button.collidepoint(pos):
        state = PAUSE
        music.pause()
    elif state == GAME_OVER:
        handle_game_over_click(pos)

pgzrun.go()