import pygame
import sys
import os
import random

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 600
HEIGHT = 400
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.Surface(screen.get_size()).convert()
clock = pygame.time.Clock()


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
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    build_bricks()


#  Класс, отвечающий за кирпичики
class Wall(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 20)).convert()
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        # set the position of the block
        self.rect.left = x
        self.rect.top = y


#  Кирпичики
def build_bricks():
    brick_group_red = pygame.sprite.Group(Wall((255, 0, 0), 1, 1), Wall((255, 0, 0), 61, 1), Wall((255, 0, 0), 121, 1),
                                          Wall((255, 0, 0), 181, 1), Wall((255, 0, 0), 241, 1),
                                          Wall((255, 0, 0), 301, 1), Wall((255, 0, 0), 361, 1),
                                          Wall((255, 0, 0), 421, 1), Wall((255, 0, 0), 481, 1),
                                          Wall((255, 0, 0), 541, 1))
    set_bricks(brick_group_red)
    brick_group_yellow = pygame.sprite.Group(Wall((255, 255, 0), 31, 40), Wall((255, 255, 0), 91, 40),
                                             Wall((255, 255, 0), 151, 40), Wall((255, 255, 0), 211, 40),
                                             Wall((255, 255, 0), 271, 40), Wall((255, 255, 0), 331, 40),
                                             Wall((255, 255, 0), 391, 40), Wall((255, 255, 0), 451, 40),
                                             Wall((255, 255, 0), 511, 40))
    set_bricks(brick_group_yellow)
    brick_group_green = pygame.sprite.Group(Wall((0, 255, 0), 121, 79), Wall((0, 255, 0), 181, 79),
                                            Wall((0, 255, 0), 241, 79), Wall((0, 255, 0), 301, 79),
                                            Wall((0, 255, 0), 361, 79), Wall((0, 255, 0), 421, 79))
    set_bricks(brick_group_green)
    brick_group_blue = pygame.sprite.Group(Wall((0, 0, 255), 151, 118), Wall((0, 0, 255), 211, 118),
                                           Wall((0, 0, 255), 271, 118), Wall((0, 0, 255), 331, 118),
                                           Wall((0, 0, 255), 391, 118))
    set_bricks(brick_group_blue)


#  Вывод кирпичиков на экран
def set_bricks(brick_group):
    brick_group.clear(screen, background)
    brick_group.draw(screen)


#  Шарик
class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)


start_screen()
