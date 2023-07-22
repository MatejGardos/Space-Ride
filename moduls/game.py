import pygame
from .obsticles import Obsticle
import cfg
import sys

class Game():
    def __init__(self, player, obsticle_group):
        self.main_screen = pygame.image.load("assets/graphics/Main_screen.png")

        self.title_font = pygame.font.Font("assets/font/simkai.ttf", 48)
        self.font = pygame.font.Font("assets/font/simkai.ttf", 20)

        self.pickup_sound = pygame.mixer.Sound("assets/audio/pick_up.wav")
        self.explosion_sound = pygame.mixer.Sound("assets/audio/explosion.wav")

        with open("assets/highscore/highscore.txt") as file:
            self.highscore = file.read()

        self.clock = pygame.time.Clock()

        self.is_game_over = False

        self.player = player
        self.obsticle_group = obsticle_group

        self.score = 0

        self.obsticle_frequency = 1000
        self.last_obsticle = pygame.time.get_ticks()
        self.fuel_frequency =  3000
        self.last_fuel = pygame.time.get_ticks()
        self.play_text_index = 0

        self.rocket_speed = 0
        self.VERTICAL_ACCELERATION = cfg.VERTICAL_ACCELERATION # gravity

    def update(self, surface):
        self.check_collisions()
        self.generate_obsticle()
        self.generate_fuel()
        self.calculate_rocket_speed()
        self.game_over(surface)

        self.obsticle_frequency = max(300, self.obsticle_frequency - (self.score/50))

    def check_collisions(self):
        for obsticle in self.obsticle_group:
            if self.player.rect.colliderect(obsticle):
                if obsticle.type == "fuel":
                    self.pickup_sound.play() 
                    self.player.fuel = max(self.player.fuel + 20, 100)
                    obsticle.kill()
                elif obsticle.type == "obsticle":
                    self.explosion_sound.play()
                    self.is_game_over = True

    def generate_obsticle(self):
        if pygame.time.get_ticks() - self.last_obsticle > self.obsticle_frequency and int(self.score) % 2 == 0:
            self.last_obsticle = pygame.time.get_ticks()
            obsticle = Obsticle("obsticle")
            self.obsticle_group.add(obsticle)

    def generate_fuel(self):
        if pygame.time.get_ticks() - self.last_fuel > self.fuel_frequency and int(self.score) % 40 == 0:
            self.last_fuel = pygame.time.get_ticks()
            obsticle = Obsticle("fuel")
            self.obsticle_group.add(obsticle)

    def calculate_rocket_speed(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.rocket_speed = min(self.rocket_speed + 1, 8)
        else:
            self.rocket_speed = max(1, self.rocket_speed-self.VERTICAL_ACCELERATION)


    def draw(self, surface, fuel):
        #height
        height_surf = self.font.render(f"{int(self.score)}", False,  cfg.BLACK)
        height_rect = height_surf.get_rect(center = (300,558))
        surface.blit(height_surf,height_rect)

        #text "Height:"
        htext_surf = self.font.render("Height:", False,  cfg.BLACK)
        htext_rect = htext_surf.get_rect(center = (300,532))
        surface.blit(htext_surf,htext_rect)

        #fuel in %
        fuel_text_surf = self.font.render(f"{int(fuel)}%", False,  cfg.BLACK)
        fuel_text_rect = fuel_text_surf.get_rect(center = (100,560))
        surface.blit(fuel_text_surf, fuel_text_rect)

        #text "Fuel:"
        text_fuel_surf = self.font.render(f"Fuel:", False, cfg.BLACK)
        text_fuel_rect = text_fuel_surf.get_rect(center = (50, 518))
        surface.blit(text_fuel_surf, text_fuel_rect)

        #fuel tank
        fuel_rectangle = pygame.Rect(22,530-((60*fuel/100)-60), 50,60*fuel/100)
        pygame.draw.rect(surface, (255,0,0), fuel_rectangle)

        #highscore
        highscore_surf = self.font.render(f"{int(self.highscore)}", False, cfg.BLACK)
        highscore_rect = highscore_surf.get_rect(center = (530,558))
        surface.blit(highscore_surf, highscore_rect)

        #text "Highscore:"
        highscore_text_surf = self.font.render(f"Highscore:", False, cfg.BLACK)
        highscore_text_rect = highscore_text_surf.get_rect(center = (530,532))
        surface.blit(highscore_text_surf,highscore_text_rect)

    def pause(self, surface):
        if int(self.highscore) < self.score:
            with open("assets/highscore/highscore.txt", "w") as file:
                file.write(str(round(self.score)))

        with open("assets/highscore/highscore.txt") as file:
            self.highscore = file.read()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
                if event.type == pygame.KEYDOWN:
                    is_paused = False
                    self.is_game_over = False

            surface.blit(self.main_screen, (0,0))

            #highscore
            highscore_surf = self.font.render(f"{int(self.highscore)}", False, cfg.WHITE)
            highscore_rect = highscore_surf.get_rect(center = (520,575))
            surface.blit(highscore_surf, highscore_rect)

            #text "Highscore:"
            highscore_text_surf = self.font.render(f"Highscore:", False, cfg.WHITE)
            highscore_text_rect = highscore_text_surf.get_rect(center = (520,550))
            surface.blit(highscore_text_surf,highscore_text_rect)

            #score
            height_surf = self.title_font.render(f"{int(self.score)}", False, cfg.WHITE)
            height_rect = height_surf.get_rect(center = (470,230))
            surface.blit(height_surf,height_rect)

            #text "Score:"
            htext_surf = self.title_font.render("Score:", False, cfg.WHITE)
            htext_rect = htext_surf.get_rect(center = (470,180))
            surface.blit(htext_surf,htext_rect)

            
            play_text1_surf = self.title_font.render("Press any button to play", False, cfg.WHITE)
            play_text2_surf = self.title_font.render("Press any button to play", False, cfg.RED)
            play_texts = [play_text1_surf,  play_text2_surf]

            self.play_text_index += 0.05
            if self.play_text_index > len(play_texts):
                self.play_text_index = 0
            play_text_surf = play_texts[int(self.play_text_index)] 

            play_text_rect = play_text1_surf.get_rect(center = (300,475))
            surface.blit(play_text_surf, play_text_rect)

            pygame.display.update()
            self.clock.tick(cfg.FPS)

    def game_over(self, surface):
        if self.player.fuel <= 0: self.is_game_over = True

        if self.is_game_over:
            self.pause(surface)
            self.obsticle_group.empty()
            self.player.reset()
            self.score = 0
            self.last_fuel = pygame.time.get_ticks()
            self.last_obsticle = pygame.time.get_ticks()
            