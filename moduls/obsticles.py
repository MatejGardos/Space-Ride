import pygame
import cfg
import random 

class Obsticle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type

        self.meteor = pygame.image.load("assets/graphics/Meteor.png")
        self.satelite = pygame.image.load("assets/graphics/Satelite.png")
        self.fuel = pygame.image.load("assets/graphics/Fuel.png")

        self.angle = 0
        self.rotate_speed = random.randint(-3, 3)
        self.speed = random.randint(2, 6)

        if self.type == "obsticle":
            self.original_image = random.choice([self.meteor, self.satelite])

        if self.type == "fuel":
            self.original_image = self.fuel

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(0, cfg.SCREEN_WIDTH-self.image.get_width()), -100)


    def update(self, rocket_speed):
        self.move(rocket_speed)
        self.rotate()

    def move(self, rocket_speed):
        self.rect.y += self.speed + rocket_speed

        if self.rect.top > cfg.SCREEN_WIDTH - 100:
            self.kill()

    def rotate(self):
        original_rect = self.image.get_rect()
        self.angle = (self.angle + self.rotate_speed) % 360
        rot_image = pygame.transform.rotate(self.original_image, self.angle)
        rot_rect = original_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
