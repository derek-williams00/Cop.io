import pygame
import math
import random

room_width = 1600
room_height = 1200

class Game:
    window_size = (800, 600)
    room_size = (room_width, room_height)
    window_caption = "cop.io version 0.0"
    
    def __init__(self):
        pygame.init()
        self.room = pygame.Surface(self.room_size)
        self.game_display = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_caption)
        self.game_clock = pygame.time.Clock()
        self.player = Cell()
        self.game_loop()

    ##ADD: convert room position to display position and vice versa
        
    def blit_room_to_display(self):
        self.game_display.blit(self.room,
                                      (-(self.player.x-(self.window_size[0]/2)),
                                       -(self.player.y-(self.window_size[1]/2))))
        
    def game_loop(self):
        self.game_display.fill((200, 200, 200))  #the outside of the room
        self.room.fill((255, 255, 255))
        
        self.player.move()
        self.player.draw(self.room)
        
                         
        self.blit_room_to_display()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_w:
                    pass
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        self.game_clock.tick(30)       
        self.game_loop()                


class Mass:
    radius = 16
    x = 100
    y = 100
    
    def __init__(self):
        self.color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        self.x = random.randint(0, room_width)
        self.y = random.randint(0, room_height)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class Cell(Mass):
    def __init__(self):
        super().__init__()
        self.speed = 3
        self.target_x = random.randint(0, room_width)
        self.target_y = random.randint(0, room_height)

    #Used to calculate movement
    def rise_to_target(self):
        return self.y-self.target_y

    def run_to_target(self):
        return self.x-self.target_x

    def distance_to_target(self):
        return math.sqrt(math.pow( self.rise_to_target(), 2) + math.pow(self.run_to_target(), 2) )

    def frac_travel(self):
        return self.speed / self.distance_to_target()
            
    def slope(self):
        return self.rise_to_target() / self.run_to_target()
    
    def direction(self):
        return math.degrees(math.atan( self.slope() ))

    def rise_this_tick(self):
        return self.rise_to_target() * self.frac_travel()

    def run_this_tick(self):
        return self.run_to_target() * self.frac_travel()

    def move(self):
        self.x += self.rise_this_tick()
        self.y += self.run_this_tick()
        
    

        
        
        
            
        
