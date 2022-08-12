from asyncio import shield
import random, pygame
from .power_up import PowerUp

from dino_runner.components.power_ups.powers  import Hammer, Shield
from dino_runner.utils.constants import HAMMER, SHIELD

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.grab_s = pygame.mixer.Sound("dino_runner/effect_sounds/grab_s.mp3")

    def generate_power_up(self, points):
        if len(self.power_ups) == 0 :
            possibility = random.randint(0,1)
            if self.when_appears == points and possibility == 0:
                self.when_appears = random.randint(self.when_appears+200, self.when_appears+300)
                self.power_ups.append(Shield())
            elif self.when_appears == points and possibility == 1:
                self.when_appears = random.randint(self.when_appears+200, self.when_appears+300)
                self.power_ups.append(Hammer())



    def update(self, points, game_speed, player):
        self.generate_power_up(points)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):     
                self.grab_s.play()
                player.shield = True 
                player.hammer = True
                power_up.start_time = pygame.time.get_ticks()
                player.show_text = True
                player.type = power_up.type
                time_random = random.randint(5,8)
                player.shield_time_up = power_up.start_time + (time_random * 1000)
                self.power_ups.remove(power_up)


    def draw (self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200,300)