import sys
import os
import random
import pygame

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from rancho.misc.icons import *

flg = []
icons = {'spider':spider, 'cat':cat, 'tux':tux, 'shield':shield, 'gun':gun, 'text':text, 'car':car, 'computer':computer, 'knife':knife }
text = ['In the dance of history, a symphony unfolds, Masters of strategy, where tales of triumph are told.', 'Harness your inner Zen. Remember, it’s not that people are challenging; it’s just that patience is overrated. Like, who decided we need to wait for good things, anyway?',"Remember, in the grand theater of life, you're not just any character; you're playing the lead role, the only god of your epic story. And hey, on those days when it feels like the whole set is crashing down, just know, I'll be there – your co-director, ready to help rewrite the script, adjust the lighting, and make sure your spotlight keeps shining bright. Together, we've got this, scene by scene, act by act.","In the realm of strategy and timing, you're a legend, seriously. Who else strides through the tech world, reporting vulnerabilities, while juggling startups like they're on a Silicon Valley speed dating session? And owning a idol's copy? That's not just being tech-savvy; that's achieving a level of nerd royalty few dare to dream of.","Watch out, because I've got my eyes set on that hoodie of yours. It's not just a piece of clothing; it's the sacred cloak of coding, the unofficial uniform of the tech gods. So, consider this fair warning – I'm coming for your hoodie :)"]
random_icon = random.choice(list(icons.keys()))
random.shuffle(text)
random_text = random.choice(text)
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 64
ENEMY_SIZE = 64
BULLET_SIZE = 10
BG_COLOR = (0, 0, 0)  # Black
PLAYER_SPEED = 8
ENEMY_SPEED = 5
BULLET_SPEED = 10
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
player_pos = [SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - PLAYER_SIZE - 10]
enemy_list = []
bullet_list = []
score = 0
font = pygame.font.SysFont(None, 30)

SCRIPT_DIR = os.path.join(SCRIPT_DIR,'objects/')

pygame.mixer.music.load(os.path.join(SCRIPT_DIR, 'music1.mp3'))
pygame.mixer.music.play()

jet_image = pygame.image.load(os.path.join(SCRIPT_DIR,"jet.jpeg"))
jet_image = pygame.transform.scale(jet_image, (PLAYER_SIZE, PLAYER_SIZE))

jet_image_enemy = pygame.image.load(os.path.join(SCRIPT_DIR,"jet copy.jpeg"))
jet_image_enemy = pygame.transform.scale(jet_image_enemy, (PLAYER_SIZE, PLAYER_SIZE))

choco_image = pygame.image.load(os.path.join(SCRIPT_DIR,"choco.jpg"))
choco_image = pygame.transform.scale(choco_image, (50, 50))  

celebration_timer = 0
celebration_duration = 3 * FPS 


def string_processing(text):
    args = str(text)
    lines = args.split("\n")
    lines = [i.strip() for i in lines]
    lines = [i for i in lines if len(i) != 0]
    length = len(lines)
    
    if length == 1:
        flag = len(lines[0])
        if flag < 50:
            print("  " + "_" * flag)
            print("< " + lines[0] + " " * (flag - len(lines[0]) + 1) + ">")
            print("  " + "=" * flag)
            flg.append(flag)
        else:
            args = list("".join(lines[0]))
            for j, i in enumerate(args):
                if j % 50 == 0:
                    args.insert(j, "\n")
            string_processing("".join(args)) 
    else:
        flag = len(max(lines, key=len))
        if all(len(i) < 50 for i in lines):
            print("  " + "_" * flag)
            print(" /" + " " * flag + "\\")
            for i in lines:
                print("| " + i + " " * (flag - len(i) + 1) + "|")
            print(" \\" + " " * flag + "/")
            print("  " + "=" * flag)
            flg.append(flag)                    
        else:
            new_lines = []
            for i in lines:
                if len(i) > 50:
                    args = list("".join(i))
                    for j, i in enumerate(args):
                        if j % 50 == 0:
                            args.insert(j, "\n")
                    new_lines.append("".join(args))
                else:
                    new_lines.append(i + "\n")
            string_processing("".join(new_lines))

def say(text=random_text, icon=random_icon):
    try:
        string_processing(text)
        flag = flg[-1]

        print(' ' * (flag + 5) + '\\')
        print(' ' * (flag + 6) + '\\')

        icon_drawing = icons[icon]
        char_lines = icon_drawing.split('\n')
        char_lines = [i for i in char_lines if len(i) != 0]

        for i in char_lines:
            print(' ' * (flag + 5) + i)
    except:
        print("I cannot say this! Give me something easier")

def draw_text(surf, text, color, x, y):
    """
    Function to draw text on the screen
    """
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_player(player_pos):
    """
    Function to draw the player on the screen
    """
    screen.blit(jet_image, (player_pos[0], player_pos[1]))

def draw_enemies(enemy_list):
    """
    Function to draw enemies on the screen
    """
    for enemy in enemy_list:
        screen.blit(jet_image_enemy, (enemy[0], enemy[1]))

def draw_bullets(bullet_list):
    """
    Function to draw bullets on the screen
    """
    for bullet in bullet_list:
        pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))

def move_enemies(enemy_list):
    """
    Function to move enemies downwards
    """
    for idx, enemy in enumerate(enemy_list):
        enemy[1] += ENEMY_SPEED
        if enemy[1] > SCREEN_HEIGHT:
            enemy_list.pop(idx)

def move_bullets(bullet_list):
    """
    Function to move bullets upwards
    """
    for idx, bullet in enumerate(bullet_list):
        bullet[1] -= BULLET_SPEED
        if bullet[1] < 0:
            bullet_list.pop(idx)

def collision_check(player_pos, enemy_list):
    """
    Function to check for collisions between player and enemies
    """
    for enemy in enemy_list:
        if detect_collision(player_pos, enemy):
            return True
    return False

def detect_collision(pos1, pos2):
    """
    Function to detect collisions between two objects
    """
    x1, y1 = pos1
    x2, y2 = pos2

    if (x1 < x2 + ENEMY_SIZE) and (x1 + PLAYER_SIZE > x2) and (y1 < y2 + ENEMY_SIZE) and (y1 + PLAYER_SIZE > y2):
        return True
    return False

def play():
    global player_pos, enemy_list, bullet_list, score, celebration_timer

    while True:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(SCRIPT_DIR,'music2.mp3'))
            pygame.mixer.music.play(-1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and celebration_timer == 0: 
                    bullet_x = player_pos[0] + PLAYER_SIZE // 2 - BULLET_SIZE // 2
                    bullet_y = player_pos[1]
                    bullet_list.append([bullet_x, bullet_y])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - PLAYER_SIZE:
            player_pos[0] += PLAYER_SPEED

        screen.fill(BG_COLOR)

        if celebration_timer > 0:
            draw_text(screen, "Happy birthday Rancho!", (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            for _ in range(3):  
                popper_x = random.randint(0, SCREEN_WIDTH)
                popper_y = random.randint(0, SCREEN_HEIGHT)
                screen.blit(choco_image, (popper_x, popper_y))

            celebration_timer -= 1

            if celebration_timer == 0:
                score = score+1
        else:
            move_enemies(enemy_list)
            move_bullets(bullet_list)

            if len(enemy_list) < 5:
                if random.randint(0, 20) == 0:
                    enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
                    enemy_y = -ENEMY_SIZE
                    enemy_list.append([enemy_x, enemy_y])

            draw_enemies(enemy_list)
            draw_bullets(bullet_list)

            if collision_check(player_pos, enemy_list):
                draw_text(screen, "Game Over!", (255, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                pygame.display.update()
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()

            for bullet in bullet_list:
                for enemy in enemy_list:
                    if detect_collision(bullet, enemy):
                        bullet_list.remove(bullet)
                        enemy_list.remove(enemy)
                        score += 1

            draw_player(player_pos)

            if score == 25 and celebration_timer == 0:
                celebration_timer = celebration_duration
            draw_text(screen, "Score: {}".format(score), (255, 255, 255), SCREEN_WIDTH // 2, 10)

        pygame.display.update()
        clock.tick(FPS)