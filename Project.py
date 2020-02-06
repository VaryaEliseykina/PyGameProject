import pygame
import sys
import os
import random

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 30
WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.Surface(screen.get_size()).convert()
clock = pygame.time.Clock()

name = os.path.join('data', 'score.wav')
ScoreSound = pygame.mixer.Sound(name)

score = 0
brick_group_red = pygame.sprite.Group()
brick_group_yellow = pygame.sprite.Group()
brick_group_green = pygame.sprite.Group()
brick_group_blue = pygame.sprite.Group()
rect_group = []


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


#  Начальный экран
def start_screen():
    intro_text = ["ATARI BREAKOUT", "PRESS SPACE TO START"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                play_screen()  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


#  Экран игры
def play_screen():
    global score
    ball = Ball()
    ball_group = pygame.sprite.Group(ball)

    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    score = 0
    x_ = 300
    x_change = 0
    right = True
    left = True

    brick_group_red.add(Wall((255, 0, 0), 5, 1), Wall((255, 0, 0), 65, 1), Wall((255, 0, 0), 125, 1),
                        Wall((255, 0, 0), 185, 1), Wall((255, 0, 0), 245, 1), Wall((255, 0, 0), 305, 1),
                        Wall((255, 0, 0), 365, 1), Wall((255, 0, 0), 425, 1), Wall((255, 0, 0), 485, 1),
                        Wall((255, 0, 0), 545, 1))
    brick_group_yellow.add(Wall((255, 255, 0), 35, 40), Wall((255, 255, 0), 95, 40), Wall((255, 255, 0), 155, 40),
                           Wall((255, 255, 0), 215, 40), Wall((255, 255, 0), 275, 40), Wall((255, 255, 0), 335, 40),
                           Wall((255, 255, 0), 395, 40), Wall((255, 255, 0), 455, 40), Wall((255, 255, 0), 515, 40))
    brick_group_green.add(Wall((0, 255, 0), 125, 79), Wall((0, 255, 0), 185, 79), Wall((0, 255, 0), 245, 79),
                          Wall((0, 255, 0), 305, 79), Wall((0, 255, 0), 365, 79), Wall((0, 255, 0), 425, 79))
    brick_group_blue.add(Wall((0, 0, 255), 155, 118), Wall((0, 0, 255), 215, 118), Wall((0, 0, 255), 275, 118),
                         Wall((0, 0, 255), 335, 118), Wall((0, 0, 255), 395, 118))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if left:
                        x_change = -10
                if event.key == pygame.K_RIGHT:
                    if right:
                        x_change = 10
                if event.key == pygame.K_SPACE:
                    terminate()
            if event.type == pygame.KEYUP:
                x_change = 0
        ball_group.clear(screen, background)
        x_ += x_change
        for ball in ball_group:
            ball.update(True)
        screen.fill((0, 0, 0))
        ball_group.draw(screen)
        Rect = pygame.draw.rect(screen, (255, 255, 255), (x_, 378, 50, 4))
        rect_group.append(Rect)

        for i in rect_group:
            if i != Rect:
                rect_group.remove(i)

        set_bricks(brick_group_red)
        set_bricks(brick_group_yellow)
        set_bricks(brick_group_green)
        set_bricks(brick_group_blue)

        text = pygame.font.SysFont(None, 30).render("Score:" + str(score), True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.bottomright = screen.get_rect().bottomright
        screen.blit(text, textRect)

        for ball in ball_group:
            ball.check_defeat()

        for ball in ball_group:
            ball.check_victory()

        clock.tick(FPS)
        pygame.display.flip()


def game_over_screen():
    screen.fill((0, 0, 0))
    Font = pygame.font.SysFont(None, 30)
    Font2 = pygame.font.SysFont(None, 72)

    text2 = Font2.render("GAME OVER", True, (255, 255, 255), (0, 0, 0))
    text3 = Font.render("Press space to restart", True, (255, 255, 255), (0, 0, 0))
    text7 = Font.render("Score:" + str(score), True, (255, 255, 255), (0, 0, 0))
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect7 = text7.get_rect()
    textRect2.center = screen.get_rect().center
    textRect3.midbottom = screen.get_rect().midbottom
    textRect7.midtop = screen.get_rect().midtop
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text7, textRect7)
    #if musicPlaying:
        #pygame.mixer.music.stop()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                play_screen()  # начинаем игру

        brick_group_red.empty()
        brick_group_yellow.empty()
        brick_group_green.empty()
        brick_group_blue.empty()

        pygame.display.flip()
        clock.tick(FPS)


def victory_screen():
    screen.fill((0, 0, 0))
    Font = pygame.font.SysFont(None, 30)
    Font2 = pygame.font.SysFont(None, 72)

    text2 = Font2.render("VICTORY", True, (255, 255, 255), (0, 0, 0))
    text3 = Font.render("Press space to restart", True, (255, 255, 255), (0, 0, 0))
    text7 = Font.render("Score:" + str(score), True, (255, 255, 255), (0, 0, 0))
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect7 = text7.get_rect()
    textRect2.center = screen.get_rect().center
    textRect3.midbottom = screen.get_rect().midbottom
    textRect7.midtop = screen.get_rect().midtop
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text7, textRect7)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                play_screen()  # начинаем игру

        brick_group_red.empty()
        brick_group_yellow.empty()
        brick_group_green.empty()
        brick_group_blue.empty()

        pygame.display.flip()
        clock.tick(FPS)


#  Кирпичики
class Wall(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 20)).convert()
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        # координаты
        self.rect.left = x
        self.rect.top = y


#  Вывод кирпичиков на экран
def set_bricks(brick_group):
    brick_group.clear(screen, background)
    brick_group.draw(screen)


#  Шарик
class Ball(pygame.sprite.Sprite):
    def __init__(self, radius=5):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (255, 255, 255), (radius, radius), radius)
        self.rect = self.image.get_rect()

        #  координаты
        self.rect.left = random.randrange(0, screen.get_width() - self.rect.width)
        self.rect.top = random.randrange(162, 200)
        self.dir_x = random.choice([-1, 1])
        self.dir_y = 1
        #  скорость
        self.speed = 3

    #  Сбиваем кирпичики
    def update(self, corr):
        global score

        check = self.rect.move(self.speed * self.dir_x, 0)
        for rect in rect_group:
            if rect.colliderect(check):
                self.dir_x *= -1
                break

        check = self.rect.move(0, self.speed * self.dir_y)
        for rect in rect_group:
            if rect.colliderect(check):
                self.dir_y *= -1
                break

        #  красные
        check = self.rect.move(0, self.speed * self.dir_y)
        for brick in brick_group_red:
            if brick.rect.colliderect(check):
                brick_group_red.remove(brick)
                self.dir_y *= -1
                self.speed = 6.5
                score += 1
                ScoreSound.play()
                break

        #  желтые
        check = self.rect.move(0, self.speed * self.dir_y)
        for brick in brick_group_yellow:
            if brick.rect.colliderect(check):
                brick_group_yellow.remove(brick)
                self.dir_y *= -1
                self.speed = 6
                score += 1
                ScoreSound.play()
                break

        #  зеленые
        check = self.rect.move(0, self.speed * self.dir_y)
        for brick in brick_group_green:
            if brick.rect.colliderect(check):
                brick_group_green.remove(brick)
                self.dir_y *= -1
                self.speed = 4
                score += 1
                ScoreSound.play()
                break

        #  синие
        check = self.rect.move(0, self.speed * self.dir_y)
        for brick in brick_group_blue:
            if brick.rect.colliderect(check):
                brick_group_blue.remove(brick)
                self.dir_y *= -1
                self.speed = 3
                score += 1
                ScoreSound.play()
                break

        # Смена направления
        if self.rect.left < 0 or self.rect.right >= screen.get_width():
            self.dir_x *= -1
        if self.rect.top < 0:
            self.dir_y *= -1
        self.rect.move_ip(self.speed * self.dir_x, self.speed * self.dir_y)

    def check_defeat(self):
        if self.rect.bottom >= screen.get_height():
            game_over_screen()

    def check_victory(self):
        if len(brick_group_red) == len(brick_group_yellow) == len(brick_group_green) == len(brick_group_blue) == 0:
            victory_screen()


start_screen()
