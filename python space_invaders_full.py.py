import pygame
import random
import math

pygame.init()

# ------------------------------
# تنظیمات صفحه
# ------------------------------
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders - Full Version")

# رنگ‌ها
WHITE = (255, 255, 255)
RED = (255, 60, 60)
GREEN = (0, 255, 120)

# فونت‌ها
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# ------------------------------
# بازیکن
# ------------------------------
player_img = pygame.Surface((50, 30))
player_img.fill((0, 180, 255))
player_x = 375
player_y = 520
player_dx = 0
player_speed = 0.5

# ------------------------------
# دشمن‌ها
# ------------------------------
enemy_img = pygame.Surface((40, 30))
enemy_img.fill((255, 80, 80))

enemy_list = []
num_enemies = 8

def create_enemies():
    enemy_list.clear()
    for i in range(num_enemies):
        enemy_list.append({
            "x": random.randint(0, 760),
            "y": random.randint(40, 150),
            "dx": 0.25,
            "dy": 40,
        })

create_enemies()

# ------------------------------
# گلوله‌ها (multi-shot)
# ------------------------------
bullet_img = pygame.Surface((5, 15))
bullet_img.fill(WHITE)

bullets = []
bullet_speed = 0.9

def fire_bullet(x, y):
    bullets.append({"x": x + 22, "y": y - 15})

# ------------------------------
# انفجار
# ------------------------------
explosion_img = pygame.Surface((20, 20))
explosion_img.fill((255, 150, 0))
explosions = []

def spawn_explosion(x, y):
    explosions.append({"x": x, "y": y, "timer": 15})

# ------------------------------
# برخورد
# ------------------------------
def collision(ex, ey, bx, by):
    return math.dist((ex, ey), (bx, by)) < 27

# ------------------------------
# حالت بازی
# ------------------------------
game_running = True
game_over = False
score = 0

# ------------------------------
# منوی شروع
# ------------------------------
def start_menu():
    waiting = True
    while waiting:
        screen.fill((0, 0, 30))
        title = big_font.render("SPACE INVADERS", True, WHITE)
        tip = font.render("Press SPACE to Start", True, WHITE)

        screen.blit(title, (170, 180))
        screen.blit(tip, (270, 300))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                waiting = False

start_menu()

# ------------------------------
# حلقه اصلی بازی
# ------------------------------
while game_running:

    screen.fill((0, 0, 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_dx = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_dx = player_speed
                if event.key == pygame.K_SPACE:
                    fire_bullet(player_x, player_y)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player_dx = 0

    if not game_over:

        # ------------------------------
        # حرکت بازیکن
        # ------------------------------
        player_x += player_dx
        player_x = max(0, min(750, player_x))
        screen.blit(player_img, (player_x, player_y))

        # ------------------------------
        # حرکت دشمن‌ها
        # ------------------------------
        for enemy in enemy_list:
            enemy["x"] += enemy["dx"]

            if enemy["x"] <= 0:
                enemy["dx"] = abs(enemy["dx"])
                enemy["y"] += enemy["dy"]

            elif enemy["x"] >= 760:
                enemy["dx"] = -abs(enemy["dx"])
                enemy["y"] += enemy["dy"]

            # برخورد با گلوله‌ها
            for b in bullets:
                if collision(enemy["x"], enemy["y"], b["x"], b["y"]):
                    spawn_explosion(enemy["x"], enemy["y"])
                    enemy["x"] = random.randint(0, 760)
                    enemy["y"] = random.randint(50, 150)
                    bullets.remove(b)
                    score += 10

            # برخورد دشمن با بازیکن = باخت
            if enemy["y"] > 480:
                game_over = True

            screen.blit(enemy_img, (enemy["x"], enemy["y"]))

        # ------------------------------
        # حرکت گلوله‌ها
        # ------------------------------
        for b in bullets[:]:
            b["y"] -= bullet_speed
            if b["y"] < 0:
                bullets.remove(b)
            else:
                screen.blit(bullet_img, (b["x"], b["y"]))

        # ------------------------------
        # انفجارها
        # ------------------------------
        for ex in explosions[:]:
            screen.blit(explosion_img, (ex["x"], ex["y"]))
            ex["timer"] -= 1
            if ex["timer"] <= 0:
                explosions.remove(ex)

        # ------------------------------
        # امتیاز
        # ------------------------------
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # ------------------------------
        # صفحه باخت
        # ------------------------------
        over_text = big_font.render("GAME OVER", True, RED)
        screen.blit(over_text, (260, 250))

        tip = font.render("Press R to Restart", True, WHITE)
        screen.blit(tip, (290, 330))

        # ریست
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            score = 0
            create_enemies()
            bullets.clear()
            explosions.clear()
            player_x = 375
            game_over = False

    pygame.display.update()

pygame.quit()
