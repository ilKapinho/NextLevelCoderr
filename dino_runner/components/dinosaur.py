
import pygame
from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING_HAMMER, DUCKING_SHIELD, HAMMER_TYPE, JUMPING, JUMPING_HAMMER, JUMPING_SHIELD, RUNNING, DUCKING, RUNNING_HAMMER, RUNNING_SHIELD, SHIELD_TYPE
from dino_runner.utils.text_utils import draw_message_component
from pygame.sprite import Sprite



DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}

class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image= RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = self.JUMP_VEL
        self.sound_jump = pygame.mixer.Sound("dino_runner/effect_sounds/jump_s.mp3")
        self.sound_jump.set_volume(0.3)
        self.powerup_s = pygame.mixer.Sound("dino_runner/effect_sounds/powerup_s.mp3")
        self.powerup_s.set_volume(0.3)
        self.powerup_s_on = pygame.mixer.get_busy()


        self.setup_state()

    def setup_state(self):
        self.has_power_up = False
        self.shield = False
        self.hammer = False
        self.show_text = False
        self.shield_time_up = 0  
        
    
    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.sound_jump.play()
            self.dino_duck = False
            self.dino_jump  = True
            self.dino_run = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_jump  = False
            self.dino_duck = False
            self.dino_run = True

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1 

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1 
        
    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < - self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False 
            self.jump_vel = self.JUMP_VEL

    def check_invencibility(self, screen):
        
        if self.shield:
            time_to_show = round((self.shield_time_up - pygame.time.get_ticks())/ 1000, 2 ) 
            if time_to_show >= 0 and self.show_text:
                if  self.powerup_s_on == False:
                    self.powerup_s.play()
                draw_message_component(f"Shield Enabled for {time_to_show}",
                screen, 
                font_size=18,
                pos_x_center=500,
                pos_y_center=40
                )
            else:
                self.powerup_s.fadeout(1)
                self.shield = False
                self.type = DEFAULT_TYPE
        elif self.hammer:
            
            time_to_show = round((self.shield_time_up - pygame.time.get_ticks())/ 1500, 2 ) 
            if time_to_show >= 0 and self.show_text:
                if  self.powerup_s_on == False:
                    self.powerup_s.play()
                draw_message_component(f"Hammer uses: {time_to_show}",
                screen, 
                font_size=18,
                pos_x_center=500,
                pos_y_center=40
                )
            else:
                self.powerup_s.fadeout(1)
                self.hammer = False
                self.type = DEFAULT_TYPE

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y) )