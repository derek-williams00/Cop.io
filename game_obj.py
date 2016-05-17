import pygame
import math
import random


class Mass:
    def __init__(self, room_size):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = 8
        self.x = random.randint(0, room_size[0])
        self.y = random.randint(0, room_size[1])

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class Cell(Mass):
    def __init__(self, room_size):
        super().__init__(room_size)
        self.speed_factor = 64
        self.radius = 16
        self.target_x = random.randint(0, room_size[0])
        self.target_y = random.randint(0, room_size[1])
        self.eating = []

    #Movement functions
    def set_target(self, pos):
        self.target_x = pos[0]
        self.target_y = pos[1]

    def change_target_random(self, room_size):
        self.target_x = random.randint(0, room_size[0])
        self.target_y = random.randint(0, room_size[1])

    def chance_change_target_random(self, room_size):
        if random.randint(0, 300) == 300:
            self.change_target_random(room_size)

    def hit_target(self):
        if self.distance_to_point((self.target_x, self.target_y)) < self.radius:
            return True
        return False

    def rise_to_point(self, y):
        return self.y-y

    def run_to_point(self, x):
        return self.x-x

    def distance_to_point(self, point):
        return max(1, math.sqrt(math.pow(self.rise_to_point(point[1]), 2) + math.pow(self.run_to_point(point[0]), 2)))

    def speed(self):
        return min(8 ,self.speed_factor/math.sqrt(self.radius))
        
    def frac_travel(self):
        return self.speed() / self.distance_to_point((self.target_x, self.target_y))

    def rise_this_tick(self):
        return self.rise_to_point(self.target_y) * self.frac_travel()

    def run_this_tick(self):
        return self.run_to_point(self.target_x) * self.frac_travel()

    def clip_to_room(self, room_size):
        self.x = max(0, min(room_size[0], self.x))
        self.y = max(0, min(room_size[1], self.y))
        
    def move(self, room_size):
        self.x -= self.run_this_tick()
        self.y -= self.rise_this_tick()
        self.clip_to_room(room_size)

    #Interacting with other cells
    def collision(self, game_objs):
        for other_game_obj in game_objs:
                    if self != other_game_obj:
                        if self.distance_to_point((other_game_obj.x, other_game_obj.y)) < self.radius:
                            self.absorb(other_game_obj)
                            self.eating.append(other_game_obj)

    def absorb(self, mass):
        self.radius = int(round(math.sqrt(math.pow(mass.radius, 2) + math.pow(self.radius, 2))))

    def shrink(self):
        if self.radius > 16 and random.randint(0, int(6000/self.radius)) == 0:
                self.radius -= 1

    #Final Step Event
    def step(self, room_size, game_objs):
        self.eating = []
        self.collision(game_objs)
        self.shrink()
        self.chance_change_target_random(room_size)
        if self.hit_target():
            self.change_target_random(room_size)
        self.move(room_size)

