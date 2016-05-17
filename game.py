import pygame
import math
import random
import game_obj as gobj

room_width = 3200
room_height = 2400

class Game:
    window_size = (800, 600)
    room_size = (room_width, room_height)
    window_caption = "cop.io version 0.4"
    
    def __init__(self):
        pygame.init()
        self.room = pygame.Surface(self.room_size)
        self.game_display = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        pygame.display.set_caption(self.window_caption)
        self.game_clock = pygame.time.Clock()
        self.player = gobj.Cell(self.room_size)
        self.cells = [self.player]
        self.masses = []
        self.game_loop()

    def game_objs(self):
        return self.masses + self.cells

    def display_pos(self):
        x = self.player.x -(self.window_size[0]/2)
        y = self.player.y -(self.window_size[1]/2)
        return (x, y)

    def room_pos(self, pos):
        x = pos[0] + self.display_pos()[0]
        y = pos[1] + self.display_pos()[1]
        return (x, y)
        
    def blit_room_to_display(self):
        self.game_display.blit(self.room, (-self.display_pos()[0], -self.display_pos()[1]))

    def add_mass(self):
        self.masses.append(gobj.Mass(self.room_size))

    def add_cell(self):
        self.cells.append(gobj.Cell(self.room_size))

    def delete_game_objs(self, objs):
        for obj in objs:
            if self.masses.count(obj) > 0:
                self.masses.pop(self.masses.index(obj))
            elif self.cells.count(obj) > 0:
                self.cells.pop(self.cells.index(obj))

    def step(self):
        if random.randint(0, 30) == 30:
                self.add_mass()
                if random.randint(0, 10) == 10:
                    self.add_cell()

    def game_loop(self):
        while True:
            self.game_display.fill((200, 200, 200))  #the outside of the room
            self.room.fill((255, 255, 255))  #the inside of the room

            self.step()

            #triggering step events for cells
            for cell in self.cells:
                cell.step(self.room_size, self.game_objs())
                self.delete_game_objs(cell.eating)

            #triggering draw events for all game objects
            for game_obj in self.game_objs():
                game_obj.draw(self.room)

            self.player.set_target(self.room_pos(pygame.mouse.get_pos()))

            self.blit_room_to_display()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
                    if event.key == pygame.K_w:
                        pass
                    if self.cells.count(self.player) == 0:
                        if event.key == pygame.K_UP:
                            self.player.y -= 100
                        if event.key == pygame.K_DOWN:
                            self.player.y += 100
                        if event.key == pygame.K_RIGHT:
                            self.player.x += 100
                        if event.key == pygame.K_LEFT:
                            self.player.x -= 100
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.VIDEORESIZE:
                    self.window_size = (event.w, event.h)
                    self.game_display = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
                    pygame.display.set_caption(self.window_caption)

            self.game_clock.tick(30)
