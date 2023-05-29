import pygame
import random 
import itertools

from enum import Enum
import pygame.mixer

pygame.init()
pygame.mixer.init()

class Window:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 0
        self.right = width
        self.top = 0
        self.bottom = height

    
    def get_tuple(self):
        return (self.width, self.height)
    

class InitValue(Enum):
    Rock = "./assets/rock.png"
    Scissors = "./assets/scissors.png"
    Paper = "./assets/paper.png"

class Functional(pygame.sprite.Sprite):
    def __init__(self, type: InitValue, startpos, velocity, startdir, width = 70):
        super().__init__()
        self.type = type
        self.pos = pygame.math.Vector2(startpos)
        self.velocity = velocity
        self.dir = pygame.math.Vector2(startdir).normalize()
        
        self.image = pygame.transform.scale(pygame.image.load(self.type.value).convert_alpha(), (width, width))
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))
        self.radius = width / 2
        self.width = width

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))

    def get_name(self):
        return self.type.name
    
    def load_image(self):
        self.image = pygame.transform.scale(pygame.image.load(self.type.value).convert_alpha(), (self.width, self.width))
    
    def update(self):
        self.pos += self.dir * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)
    


    def change_pic(self, other):

        if self.type == InitValue.Rock and other.type == InitValue.Paper:
                self.type = InitValue.Paper
                self.load_image()
        elif self.type == InitValue.Scissors and other.type == InitValue.Rock:
                self.type = InitValue.Rock
                self.load_image()
        elif self.type == InitValue.Paper and other.type == InitValue.Scissors:
                self.type = InitValue.Scissors
                self.load_image()
    
    def collided(self, window_size: Window):
        if self.rect.left <= window_size.left or self.rect.right >= window_size.right:
            self.reflect(pygame.math.Vector2(-1, 0))

        if self.rect.top <= window_size.top or self.rect.bottom >= window_size.bottom:
            self.reflect(pygame.math.Vector2(0, -1))


def find_collisions(sprites: pygame.sprite.Group):
    for a, b in itertools.permutations(sprites, 2):
        if a.pos.distance_to(b.pos) < a.radius + b.radius -2:
            a.change_pic(b)


def reflectObjects(object_1, object_2):
    vector_1 = pygame.Vector2(object_1.rect.center)
    vector_2 = pygame.Vector2(object_2.rect.center)
    radius_1 = object_1.rect.width // 2
    radius_2 = object_2.rect.width // 2
    distance = vector_1.distance_to(vector_2)
    if distance < radius_1 + radius_2 - 2:
        object_1.change_pic(object_2)
        next_distance = (vector_1 + object_1.dir).distance_to(vector_2 + object_2.dir)
        vector_3 = vector_2 - vector_1
        if next_distance < distance and vector_3.length() > 0:
            object_1.dir = object_1.dir.reflect(vector_3)
            object_2.dir = object_2.dir.reflect(vector_3)

def window_collisions(group: pygame.sprite.Group, window_size):
    [sprite.collided(window_size) for sprite in group]


def run():
    window = Window(800, 800)
    background = ["./assets/background1.jpg", "./assets/background2.jpg"]
    
    
    
    screen = pygame.display.set_mode(window.get_tuple())
    clock = pygame.time.Clock()
    
    
    pygame.mixer.music.load("./music/music.mp3")
    pygame.mixer.music.play(-1)

    sprite_groups = pygame.sprite.Group()
    init_values = [InitValue.Rock, InitValue.Scissors, InitValue.Paper]

    random_number = random.randint(3, 10)
    
    for init_value in init_values:
        
        for _ in range(random_number):
            x = random.randint(0, window.width)
            y = random.randint(0, window.height)
            velocity = random.uniform(1, 5)
            startdir = (random.random(), random.random())

            value_object = Functional(init_value, (x, y), velocity, startdir)
            sprite_groups.add(value_object)


    running = True
    background_index = 0

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sprite_groups.update()

        background_image = pygame.image.load(background[background_index])
        background_image = pygame.transform.scale(background_image, window.get_tuple())

        screen.blit(background_image, (0, 0))
        
        sprite_groups.draw(screen)

        window_collisions(sprite_groups, window)

        for a, b in itertools.permutations(sprite_groups, 2):
            reflectObjects(a, b)

        if all(sprite.type.name == sprite_groups.sprites()[0].type.name for sprite in sprite_groups):
            background_index = (background_index + 1) % len(background) 
            
        pygame.display.flip()

    pygame.mixer.music.stop()

if __name__ == "__main__":
    run()


