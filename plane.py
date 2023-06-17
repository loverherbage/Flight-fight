import pygame


class Plane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        self.blood = 5
        self.image_index = 0
        self.is_hit = False
        self.is_invincible = False
        source_img = pygame.image.load("image/source.png").convert_alpha()
        self.rect_lists = [pygame.Rect(0, 99, 102, 126), pygame.Rect(165, 360, 102, 126),
                           pygame.Rect(165, 234, 102, 126),
                           pygame.Rect(330, 624, 102, 126), pygame.Rect(330, 498, 102, 126),
                           pygame.Rect(432, 624, 102, 126)]
        for rect in self.rect_lists:
            self.image.append(source_img.subsurface(rect).convert_alpha())
        self.rect = self.image[0].get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 60
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image[0])

    def moveUp(self):
        if self.rect.top < 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.bottom > self.height - 60:
            self.rect.bottom = self.height - 60
        else:
            self.rect.bottom += self.speed

    def moveLeft(self):
        if self.rect.left < 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.right > self.width:
            self.rect.right = self.width
        else:
            self.rect.right += self.speed
