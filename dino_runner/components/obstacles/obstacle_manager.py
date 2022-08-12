import pygame, random
from dino_runner.components.obstacles.cactus import Bird, Cactus, LargeCactus
from dino_runner.utils.constants import BIRD, SMALL_CACTUS ,LARGE_CACTUS

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.death_s = pygame.mixer.Sound("dino_runner/effect_sounds/death_s.mp3")
        self.death_s.set_volume(2)

    def update (self, game):
        if len(self.obstacles) == 0:
            possibility = random.randint(0,2)
            if possibility == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif possibility == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            elif possibility == 2:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect): 
                if not game.player.shield or not game.player.hammer:
                    self.death_s.play()
                    pygame.time.delay(700)
                    game.playing = False
                    game.death_count +=1 
                else:
                    self.obstacles.remove(obstacle)
                break 

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset_obstacles(self):
        self.obstacles = []