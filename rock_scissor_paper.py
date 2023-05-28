import pygame
import random 



class Window:

    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def get_tuple(self):
        return self.width, self.height
    
window = Window(800, 600)

size = window.get_tuple()
print("Ширина окна: ", size[0])
print("Высота окна: ", size[1])

pygame.init()

screen = pygame.display.set_mode(size)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()

