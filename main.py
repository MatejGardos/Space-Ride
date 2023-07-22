import pygame
from sys import exit
from random import randint, choice
import cfg
from moduls import *

pygame.init()

# Screen
screen = pygame.display.set_mode((cfg.SCREEN_WIDTH,cfg.SCREEN_HEIGHT))
pygame.display.set_caption("Space Ride")

# Music
pygame.mixer.music.load("assets/audio/space-age.mp3")
pygame.mixer.music.set_volume(0.3)

# Clock
clock = pygame.time.Clock()

# Images
background_image = pygame.image.load("assets/graphics/Space.png")
HUD_image = pygame.image.load("assets/graphics/Bottom_card.png")

# Initialize player
player = Rocket()
flame = Flame(player.rect.x, player.rect.bottom)

# Sprite Groups
player_group = pygame.sprite.Group()
player_group.add(player)

flame_group = pygame.sprite.Group()
flame_group.add(flame)

obsticle_group = pygame.sprite.Group()

# Game helper
game = Game(player, obsticle_group )

# The main game loop
pygame.mixer.music.play(-1, 0.0, 5000)
game.pause(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("LOL")
                obsticle = Obsticle()
                obsticle_group.add(obsticle)

    # Background
    screen.blit(background_image, (0,0))

    # Update and draw sprite groups
    player_group.update()
    player_group.draw(screen)

    flame_group.update(player.rect.x, player.rect.bottom)
    flame_group.draw(screen)           
      
    obsticle_group.update(game.rocket_speed)
    obsticle_group.draw(screen)

    # HUD
    screen.blit(HUD_image, (0, cfg.SCREEN_HEIGHT-100))

    # Calculate score
    game.score += game.rocket_speed/cfg.FPS

    # Calculate fuel
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        player.fuel -= 0.1
    else:
        player.fuel -= 0.05

    # Update and draw the game
    game.update(screen)
    game.draw(screen, round(player.fuel))

        
    # Update the screen and tick the clock
    pygame.display.update()
    clock.tick(cfg.FPS)

    

# Ending pygame
pygame.quit()