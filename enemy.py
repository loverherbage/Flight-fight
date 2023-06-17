import random

import pygame


class minEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        source_img = pygame.image.load('image/source.png').convert_alpha()
        self.explosion_images = []
        self.destroy_index = 0
        self.bg_size = bg_size
        self.max_blood = 2
        self.blood = 2
        self.normal_images = source_img.subsurface(pygame.Rect(534, 612, 57, 43))
        exp_rects = [pygame.Rect(267, 347, 57, 43), pygame.Rect(873, 697, 57, 43), pygame.Rect(267, 296, 57, 43),
                     pygame.Rect(930, 697, 57, 43)]
        for er in exp_rects:
            self.explosion_images.append(source_img.subsurface(er).convert_alpha())
        self.rect = self.normal_images.get_rect()
        self.rect.left, self.rect.bottom = random.randint(0, bg_size[0] - self.rect.width), 0
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.normal_images)
        self.is_hit = self.is_over = False

    def move(self):
        if self.rect.top > self.bg_size[1]:
            pass
        else:
            self.rect.bottom += self.speed


class midEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        source_img = pygame.image.load('image/source.png').convert_alpha()
        self.explosion_images = []
        self.destroy_index = 0
        self.max_blood = 5
        self.blood = 5
        self.bg_size = bg_size
        self.normal_images = source_img.subsurface(pygame.Rect(0, 2, 69, 90))
        exp_rects = [pygame.Rect(432, 656, 69, 90), pygame.Rect(534, 656, 69, 90), pygame.Rect(604, 656, 69, 90),
                     pygame.Rect(671, 656, 69, 90), pygame.Rect(742, 656, 69, 90)]
        for er in exp_rects:
            self.explosion_images.append(source_img.subsurface(er).convert_alpha())
        self.rect = self.normal_images.get_rect()
        self.rect.left, self.rect.bottom = random.randint(0, bg_size[0] - self.rect.width), 0
        self.speed = 3
        self.mask = pygame.mask.from_surface(self.normal_images)
        self.is_hit = self.is_over = False

    def move(self):
        if self.rect.top > self.bg_size[1]:
            pass
        else:
            self.rect.bottom += self.speed


class BigEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        source_img = pygame.image.load('image/source.png').convert_alpha()
        self.explosion_images = []
        self.destroy_index = 0
        self.max_blood = self.blood = 15
        self.bg_size = bg_size
        self.normal_images = source_img.subsurface(pygame.Rect(337, 753, 165, 250)).convert_alpha()
        exp_rects = [pygame.Rect(507, 753, 165, 250), pygame.Rect(170, 753, 165, 250), pygame.Rect(1, 490, 165, 250),
                     pygame.Rect(1, 227, 165, 250),
                     pygame.Rect(842, 753, 165, 250), pygame.Rect(165, 490, 165, 250), pygame.Rect(678, 753, 165, 250),
                     pygame.Rect(1, 753, 165, 250)]
        for er in exp_rects:
            self.explosion_images.append(source_img.subsurface(er).convert_alpha())
        self.rect = self.normal_images.get_rect()
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.normal_images)
        self.rect.left, self.rect.bottom = random.randint(0, bg_size[0] - self.rect.width), random.randint(
            -2 * self.rect.height, 0)
        self.is_hit = self.is_over = False

    def move(self):
        if self.rect.top > self.bg_size[1]:
            pass
        else:
            self.rect.bottom += self.speed
