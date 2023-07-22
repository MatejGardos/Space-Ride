import pygame
import cfg

class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/graphics/Rocket.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = cfg.SCREEN_WIDTH//2
        self.rect.bottom = cfg.SCREEN_HEIGHT-150

        self.vertical_speed = cfg.VERTICAL_SPEED

        self.fuel = 100
    
    def update(self):
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.left = max(0, self.rect.left - self.vertical_speed)
        if keys[pygame.K_RIGHT]:
            self.rect.right = min(self.rect.right + self.vertical_speed, cfg.SCREEN_WIDTH)

    def reset(self):
        self.rect.centerx = cfg.SCREEN_WIDTH//2
        self.rect.bottom = cfg.SCREEN_HEIGHT-150
        self.fuel = 100


class Flame(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.flames_images = []
        for i in range(4):
            img = pygame.image.load(f"assets/graphics/flame/Flame{i}.png")
            self.flames_images.append(img)

        self.current_sprite = 0

        self.image = self.flames_images[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.top =  self.y
        self.rect.x = self.x

    def update(self, x, y):
        self.animate()
        self.rect.top =  y
        self.rect.x = x

    def animate(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.current_sprite += 0.2
            if self.current_sprite >= 4:
                self.current_sprite = 1
        else:
            self.current_sprite =  0

        self.image = self.flames_images[int(self.current_sprite)]