import pygame
from pygame.locals import *
from random import randint


class BoobSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.name = "boob"
        source_image = pygame.image.load("image/source.png").convert_alpha()
        self.image = source_image.subsurface(pygame.Rect(100, 120, 67, 108)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = randint(-2 * self.rect.width, 0), randint(0, bg_size[0] - self.rect.width)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = randint(1, 3)
        self.bg_size = bg_size
        self.is_hit = False
        self.is_alive = True

    def move(self):
        if self.rect.top > self.bg_size[1]:
            self.is_alive = False
        else:
            self.rect.top += self.speed


class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        source_image = pygame.image.load("image/source.png").convert_alpha()
        self.name = "bullet"
        self.image = source_image.subsurface(pygame.Rect(265, 396, 60, 88)).convert_alpha()
        self.bg_size = bg_size
        self.speed = randint(1, 3)
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = randint(-2 * self.rect.width, 0), randint(0, bg_size[0] - self.rect.width)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_hit = False
        self.is_alive = True

    def move(self):
        if self.rect.top > self.bg_size[1]:
            self.is_alive = False
        else:
            self.rect.top += self.speed

