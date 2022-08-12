import pygame, random
from dino_runner.components.obstacles.cactus import Cactus, LargeCactus

from dino_runner.utils.constants import SMALL_CACTUS ,LARGE_CACTUS

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update (self, game):
        
        if len(self.obstacles) == 0:
            possibility = random.randint(0,1)
            if possibility == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif possibility == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:
                    pygame.time.delay(500)
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