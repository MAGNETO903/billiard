import pygame
import pymunk

class Ball(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.raduis = 13
        self.shape = 'none'
        self.body = 'none'
        self.image = img.convert_alpha()
        self.rect = self.image.get_rect(
            centerx=x, centery=y)

    def add_to_space(self, space):
        mass = 1
        radius = self.raduis
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = self.rect.centerx, self.rect.centery
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        body.data = 'ball'
        space.add(body, shape)
        self.shape = shape
        self.body = body