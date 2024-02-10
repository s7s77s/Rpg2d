import pygame
import os
import sys
from math import cos, sin, radians

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Rpg2d')
lvlgame = 1

from loader import *


def drawMaps(nameFile):
    maps = []
    source = "game_lvl/" + str(nameFile)
    with open(source, "r") as file:
        for i in range(0, 100):
            maps.append(file.readline().replace("\n", "").split(",")[0: -1])

    pos = [0, 0]
    for i in range(0, len(maps)):
        pos[1] = i * 80
        for j in range(0, len(maps[0])):
            pos[0] = 80 * j
            if maps[i][j] == '1':
                water = Block(water_image, pos)
                block_group.add(water)
                camera_group.add(water)
            elif maps[i][j] == '2':
                block = Block(block_image, pos)
                block_group.add(block)
                camera_group.add(block)
            elif maps[i][j] == '3':
                spawner = Spawner(spawner_image, pos)
                spawner_group.add(spawner)
                camera_group.add(spawner)


class Block(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    def update(self, stepx, stepy):
        self.rect.x += stepx
        self.rect.y += stepy


class Spawner(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    def update(self, stepx, stepy):
        self.rect.x += stepx
        self.rect.y += stepy


class Topor(pygame.sprite.Sprite):
    def __init__(self, image, pos, start_deg):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.deg_rotate = 0
        self.deg = start_deg
        self.timer_attack = 0

    def rotate(self):
        self.deg_rotate -= 20
        self.image = pygame.transform.rotate(topor_image, self.deg_rotate)

    def move(self):
        self.deg += 3
        self.rect.centerx = 150 * cos(radians(self.deg)) + player.rect.centerx
        self.rect.centery = 150 * sin(radians(self.deg)) + player.rect.centery

    def update(self):
        self.rotate()
        self.move()


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.key = pygame.key.get_pressed()
        self.speed = 5
        self.anime = False
        self.frame = 0
        self.pos_maps = [0, 0]
        self.score = 0
        self.topor = 3
        self.camera = False
        self.add_topor()
        self.speed = 5
        self.anime = False
        self.timer_anime = 0

    def update(self):
        self.move()
        self.animation()

    def add_topor(self):
        global topor_group
        topor_group = pygame.sprite.Group()
        for i in range(self.topor):
            topor = Topor(topor_image, (self.rect.centerx + 70, self.rect.centery + 70), (360 // self.topor * i))
            topor_group.add(topor)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.anime = True
            self.rect.y -= self.speed
            self.image = player_image_top[self.frame]
            if self.rect.top < 100:
                camera_group.update(0, self.speed)
                self.rect.top = 100
            else:
                self.camera = False
        elif key[pygame.K_a]:
            self.anime = True
            self.rect.x -= self.speed
            self.image = player_image_left[self.frame]
            if self.rect.left < 300:
                camera_group.update(self.speed, 0)
                self.rect.left = 300
        elif key[pygame.K_d]:
            self.anime = True
            self.rect.x += self.speed
            self.image = player_image_right[self.frame]
            if self.rect.right > 900:
                camera_group.update(-self.speed, 0)
                self.rect.right = 900
            else:
                self.camera = False
        elif key[pygame.K_s]:
            self.anime = True
            self.rect.y += self.speed
            self.image = player_image_bottom[self.frame]
            if self.rect.bottom > 700:
                camera_group.update(0, -self.speed)
                self.rect.bottom = 700
        else:
            self.anime = False
            self.camera = False

    def animation(self):
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player_image_bottom) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0


def restart():
    global topor_group, player_group, player, ptb, water_group, block_group, spawner_group, lvlgame, camera_group
    topor_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = Player(player_image_top, (300, 400))
    player_group.add(player)
    water_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    spawner_group = pygame.sprite.Group()
    camera_group = pygame.sprite.Group()


def lvl_game():
    sc.fill('gray')
    player_group.update()
    player_group.draw(sc)
    block_group.update(0, 0)
    block_group.draw(sc)
    spawner_group.update(0, 0)
    spawner_group.draw(sc)
    topor_group.update()
    topor_group.draw(sc)
    pygame.display.update()


restart()
drawMaps(str(lvlgame) + '.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    lvl_game()
    clock.tick(FPS)
