import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, plane_pos):
        pygame.sprite.Sprite.__init__(self)
        source_img = pygame.image.load("image/source.png").convert_alpha()
        self.image = source_img.subsurface(pygame.Rect(1004, 987, 9, 21)).convert_alpha()
        self.speed = 12
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.midbottom = plane_pos[0], plane_pos[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, plane_pos):
        self.rect.left, self.rect.top = plane_pos[0], plane_pos[1]
        self.active = True


class DoubleBullet(pygame.sprite.Sprite):
    def __init__(self, plane_pos):
        pygame.sprite.Sprite.__init__(self)
        source_img = pygame.image.load("image/source.png").convert_alpha()
        self.image = source_img.subsurface(pygame.Rect(66, 76, 15, 27)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = plane_pos
        self.speed = 14
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False
