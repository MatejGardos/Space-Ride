import pygame
from sys import exit
from random import randint, choice 

pygame.init()

#main stuff
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Ride")
clock = pygame.time.Clock()
FPS = 60
running = False
speed = 0
fuel = 100


#design
space_surf = pygame.image.load("graphics/Space.png")
bottom = pygame.image.load("graphics/Bottom_card.png")
main_screen = pygame.image.load("graphics/Main_screen.png")

player_surf = pygame.image.load("graphics/Rocket.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (300,450))

flame_1 = pygame.image.load("graphics/flame/Flame1.png").convert_alpha()
flame_2 = pygame.image.load("graphics/flame/Flame2.png").convert_alpha()
flame_3 = pygame.image.load("graphics/flame/Flame3.png").convert_alpha()
lil_flame = pygame.image.load("graphics/flame/LilFlame.png ").convert_alpha()
flame = [flame_1, flame_2, flame_3]
flame_index = 0

flame_surf = flame[flame_index]
flame_rect = flame_surf.get_rect(midtop = (300,450))

fuel_surf = pygame.image.load("graphics/Fuel.png").convert_alpha()

meteor_surf = pygame.image.load("graphics/Meteor.png").convert_alpha()
satelite_surf = pygame.image.load("graphics/Satelite.png").convert_alpha()

font = pygame.font.SysFont("arial.ttf", 30)
font_bigger = pygame.font.SysFont("arial.ttf", 60)

#music
bg_music = pygame.mixer.Sound("audio/space-age.mp3")
bg_music.set_volume(0.3)
bg_music.play(loops = -1)

#sound
explosion_sound = pygame.mixer.Sound("audio/explosion.wav")
explosion_sound.set_volume(0.5)
pickup_sound = pygame.mixer.Sound("audio/pick_up.wav")
pickup_sound.set_volume(1.5)

obstacle_rect_list = []
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect, surface in obstacle_list:
            obstacle_rect.y += speed 

        obstacle_list = [[obstacle,surface] for obstacle,surface in obstacle_list if obstacle.y < 600]

        return obstacle_list
    else:
        return []

def collisions(player,obstacle_list):
    if obstacle_list:
        for obstacle_rect, surface in obstacle_list:
            if player.colliderect(obstacle_rect):
                return True 
    return False

fuel_rect_list = []
def fuel_movement(fuel_list):
    if fuel_list:
        for fuel in fuel_list:
            fuel.y += speed

        fuel_list = [fuel for fuel in fuel_list if fuel.y < 600]
        return fuel_list
    else:
        return []

def fuel_collisions(player,fuel_list):
    if fuel_list:
        for fuel_rect in fuel_list:
            if player.colliderect(fuel_rect):
                return True
    return False

def flame_animation():
    global flame_surf, flame_index

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and fuel > 0:
        flame_index += 0.2 
        if flame_index >= len(flame): flame_index = 0
        flame_surf = flame[int(flame_index)]
    else: 
        flame_surf = lil_flame

score_height = 0
def display_score():
    global score_height
    score_height += speed/FPS

    #height
    height_surf = font.render(f"{int(score_height)}", False, (0,0,0))
    height_rect = height_surf.get_rect(center = (300,558))
    screen.blit(height_surf,height_rect)

    #text "Height:"
    htext_surf = font.render("Height:", False, (0,0,0))
    htext_rect = htext_surf.get_rect(center = (300,532))
    screen.blit(htext_surf,htext_rect)

    #fuel in %
    fuel_text_surf = font.render(f"{int(fuel)}%", False, (0,0,0))
    fuel_text_rect = fuel_text_surf.get_rect(center = (100,560))
    screen.blit(fuel_text_surf, fuel_text_rect)

    #text "Fuel:"
    text_fuel_surf = font.render(f"Fuel:", False, (0,0,0))
    text_fuel_rect = text_fuel_surf.get_rect(center = (50, 518))
    screen.blit(text_fuel_surf,text_fuel_rect)

    #fuel tank
    #PS: Not even god understand this
    fuel_rectangle = pygame.Rect(22,530-((60*fuel/100)-60), 50,60*fuel/100)
    pygame.draw.rect(screen, (255,0,0), fuel_rectangle)

    #highscore
    highscore_surf = font.render(f"{int(old_highscore)}", False, (0,0,0))
    highscore_rect = highscore_surf.get_rect(center = (530,558))
    screen.blit(highscore_surf, highscore_rect)

    #text "Highscore:"
    highscore_text_surf = font.render(f"Highscore:", False, (0,0,0))
    highscore_text_rect = highscore_text_surf.get_rect(center = (530,532))
    screen.blit(highscore_text_surf,highscore_text_rect)

play_text_index = 0
def display_main_screen():
    screen.blit(main_screen, (0,0))

    #highscore
    highscore_surf = font.render(f"{int(old_highscore)}", False, (255,255,255))
    highscore_rect = highscore_surf.get_rect(center = (520,575))
    screen.blit(highscore_surf, highscore_rect)

    #text "Highscore:"
    highscore_text_surf = font.render(f"Highscore:", False, (255,255,255))
    highscore_text_rect = highscore_text_surf.get_rect(center = (520,550))
    screen.blit(highscore_text_surf,highscore_text_rect)

    #score
    height_surf = font_bigger.render(f"{int(score_height)}", False, (255,255,255))
    height_rect = height_surf.get_rect(center = (470,230))
    screen.blit(height_surf,height_rect)

    #text "Score:"
    htext_surf = font_bigger.render("Score:", False, (255,255,255))
    htext_rect = htext_surf.get_rect(center = (470,180))
    screen.blit(htext_surf,htext_rect)

    
    play_text1_surf = font_bigger.render("Click to play", False, (255,255,255))
    play_text2_surf = font_bigger.render("Click to play", False, (255,0,0))
    play_text = [play_text1_surf, play_text2_surf]

    global play_text_index
    play_text_index += 0.05
    if play_text_index > len(play_text): play_text_index = 0
    play_text_surf = play_text[int(play_text_index)]

    play_text_rect = play_text1_surf.get_rect(center = (300,525))
    screen.blit(play_text_surf, play_text_rect)

#drawing stuff on screen
def draw_screen():
    screen.blit(space_surf,(0,0))
    screen.blit(player_surf, player_rect)
    screen.blit(flame_surf, flame_rect )

    for obstacle, surface in obstacle_rect_list:
        screen.blit(surface, obstacle)

    for fuel_pos in fuel_rect_list:
        screen.blit(fuel_surf, fuel_pos)

    screen.blit(bottom,(0,500))


#timer for generating obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 500)

#timer for genearting fuel
fuel_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fuel_timer, 5000)

#getting highscore
with open("highscore/highscore.txt", "r") as file:
    old_highscore = file.read()

#main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #reseting variables
            speed = 10 
            score_height = 0
            fuel = 100
            #clearing lists
            obstacle_rect_list.clear()
            fuel_rect_list.clear()
            #putting player on starting position
            player_rect.midbottom = (300,450)
            flame_rect.midtop = (300,450)
            running = True

        if event.type == obstacle_timer and running:
            obstacle_rect_list.append([meteor_surf.get_rect(midbottom = (randint(50, 550),(randint(-200, 0)))), choice((meteor_surf, satelite_surf))])
           
        if event.type == fuel_timer and running:
            fuel_rect_list.append(fuel_surf.get_rect(midbottom = (randint(50, 550),(randint(-200, 0)))))

    #game loop    
    if running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += 5
            flame_rect.x += 5
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= 5
            flame_rect.x -= 5
        if keys[pygame.K_SPACE] and fuel > 0:
            if speed <= 10:
                speed += 2 
                fuel -= 0.25

        #updating position of obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        #checking collisions
        if collisions(player_rect, obstacle_rect_list):
            running = False
            explosion_sound.play()

        #updating position of fuel
        fuel_rect_list = fuel_movement(fuel_rect_list)
        #fuel colisions
        if fuel_collisions(player_rect, fuel_rect_list): 
            fuel= 100
            fuel_rect_list.clear()
            pickup_sound.play()

        #"gravity"
        speed -= 0.5
        if speed <= -10: running = False

        #animations
        flame_animation()

        #drawing everything on screen
        draw_screen()

        #score
        display_score()

    else:
        #checking if there is new highscore 
        if int(old_highscore) < int(score_height):
            with open("highscore/highscore.txt", "w") as file:
                file.write(str(int(score_height)))
                old_highscore = int(score_height)

        display_main_screen()


    pygame.display.update()
    clock.tick(FPS)