import pygame
import math
import random

room_width = 3200
room_height = 2400

class Game:
    window_size = (800, 600)
    room_size = (room_width, room_height)
    window_caption = "cop.io version 0.3"
    
    def __init__(self):
        pygame.init()
        self.room = pygame.Surface(self.room_size)
        self.game_display = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_caption)
        self.game_clock = pygame.time.Clock()
        self.player = Cell()
        self.cells = [self.player]
        self.masses = []
        self.game_loop()

    def game_objs(self):
        return self.masses + self.cells

    def display_pos_x(self):
        return self.player.x-(self.window_size[0]/2)

    def display_pos_y(self):
        return self.player.y-(self.window_size[1]/2)

    def room_pos(self, pos):
        x = pos[0] + self.display_pos_x()
        y = pos[1] + self.display_pos_y()
        return (x, y)
        
    def blit_room_to_display(self):
        self.game_display.blit(self.room, (-self.display_pos_x(), -self.display_pos_y()))

    def add_mass(self):
        self.masses.append(Mass())

    def add_cell(self):
        self.cells.append(Cell())
        
    def game_loop(self):
        while True:
            self.game_display.fill((200, 200, 200))  #the outside of the room
            self.room.fill((255, 255, 255))  #the inside of the room

            if random.randint(0, 30) == 30:
                self.add_mass()
                if random.randint(0, 10) == 10:
                    self.add_cell()

            for cell in self.cells:
                if random.randint(0, 300) == 300:
                    cell.target_x = random.randint(0, room_width)
                    cell.target_y = random.randint(0, room_height) 
            self.player.set_target(self.room_pos(pygame.mouse.get_pos()))

            for cell in self.cells:
                cell.move()

            for game_obj in self.game_objs():
                game_obj.draw(self.room)

            for cell in self.cells:
                if cell.distance_to_point((cell.target_x, cell.target_y)) < cell.radius:
                    cell.target_x = random.randint(0, room_width)
                    cell.target_y = random.randint(0, room_height)   
                for other_game_obj in self.game_objs():
                    if cell != other_game_obj:
                        if cell.distance_to_point((other_game_obj.x, other_game_obj.y)) < cell.radius:
                            cell.absorb(other_game_obj)
                            if self.masses.count(other_game_obj) > 0:
                                self.masses.pop(self.masses.index(other_game_obj))
                            elif self.cells.count(other_game_obj) > 0:
                                self.cells.pop(self.cells.index(other_game_obj))
                                

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


class Mass:
    def __init__(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = 8
        self.x = random.randint(0, room_width)
        self.y = random.randint(0, room_height)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class Cell(Mass):
    def __init__(self):
        super().__init__()
        self.speed_factor = 64
        self.radius = 16
        self.target_x = random.randint(0, room_width)
        self.target_y = random.randint(0, room_height)

    #Used to calculate movement
    def set_target(self, pos):
        self.target_x = pos[0]
        self.target_y = pos[1]

    def rise_to_point(self, y):
        return self.y-y

    def run_to_point(self, x):
        return self.x-x

    def distance_to_point(self, point):
        return max(1, math.sqrt(math.pow(self.rise_to_point(point[1]), 2) + math.pow(self.run_to_point(point[0]), 2)))

    def speed(self):
        return self.speed_factor/self.radius
        
    def frac_travel(self):
        return self.speed() / self.distance_to_point((self.target_x, self.target_y))
            
    def slope(self):
        return self.rise_to_point(self.target_y) / self.run_to_point(self.target_x)
    
    def direction(self):
        return math.degrees(math.atan(self.slope()))

    def rise_this_tick(self):
        return self.rise_to_point(self.target_y) * self.frac_travel()

    def run_this_tick(self):
        return self.run_to_point(self.target_x) * self.frac_travel()

    def clip_to_room(self):
        self.x = max(0, min(room_width, self.x))
        self.y = max(0, min(room_height, self.y))
        
    def move(self):
        self.x -= self.run_this_tick()
        self.y -= self.rise_this_tick()
        self.clip_to_room()

    def absorb(self, mass):
        self.radius = int(round(math.sqrt(math.pow(mass.radius, 2) + math.pow(self.radius, 2))))
        
    
Game()

