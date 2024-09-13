import pygame
import random
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()

def draw_grid():
    black = False
    for i in range(0, 500, 20):
        for j in range(0, 500, 20):
            black = not black
            if black:
                pygame.draw.rect(screen, (90, 90, 110), [i, j, 20, 20])
            else:
                pygame.draw.rect(screen, (100, 100, 120), [i, j, 20, 20])


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speed = 20
        self.direction = "down"
        self.next_direction = "down"
        self.length = 1

    def move(self, x, y):
        if self.rect.x + x < 0:
            self.rect.x = 480
        elif self.rect.x + x > 480:
            self.rect.x = 0
        else:
            self.rect.x += x

        if self.rect.y + y < 0:
            self.rect.y = 480
        elif self.rect.y + y > 480:
            self.rect.y = 0
        else:
            self.rect.y += y

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(screen, GREEN, [self.rect.x, self.rect.y, 20, 20])

class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 25) * 20
        self.rect.y = random.randint(0, 25) * 20

    def draw(self):
        pygame.draw.rect(screen, RED, [self.rect.x, self.rect.y, 20, 20])

    def reregenerate_coords(self):
        self.rect.x = random.randint(0, 25) * 20
        self.rect.y = random.randint(0, 25) * 20
        
    def get_fruit_coords(self):
        return (self.rect.x, self.rect.y)


size = (500, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Snake, or python idk")
 
done = False
clock = pygame.time.Clock()
snake = Snake()
fruits = []
frames_counter = 0

# Initializa the fruits
fruits_coords = []
for i in range(4):
    fruits.append(Fruit())
    while fruits[i].get_fruit_coords() in fruits_coords:
        fruits[i].regenerate_coords()
    fruits_coords.append(fruits[i].get_fruit_coords())
    # print(len(fruits))
    # print(len(fruits_coords))
    
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if snake.direction != "right":
                    snake.next_direction = "left"
            if event.key == pygame.K_RIGHT:
                if snake.direction != "left":
                    snake.next_direction = "right"
            if event.key == pygame.K_UP:
                if snake.direction != "down":
                    snake.next_direction = "up"
            if event.key == pygame.K_DOWN:
                if snake.direction != "up":
                    snake.next_direction = "down"

 
    # --- Game logic --- #
    frames_counter += 1
    if frames_counter == 30:
        frames_counter = 0
        if snake.next_direction == "left":
            snake.direction = "left"
            snake.move(-20, 0)
        if snake.next_direction == "right":
            snake.direction = "right"
            snake.move(20, 0)
        if snake.next_direction == "up":
            snake.direction = "up"
            snake.move(0, -20)
        if snake.next_direction == "down":
            snake.direction = "down"
            snake.move(0, 20)
        
   
    # --- Drawing code --- #

    draw_grid()
    snake.draw()

    for fr in fruits:
        if fr.rect.x == snake.rect.x and fr.rect.y == snake.rect.y:
            fruits_coords.remove((fr.rect.x, fr.rect.y))
            fruits.remove(fr)
            snake.length += 1
            fruits.append(Fruit())
            
            while fruits[-1].get_fruit_coords() in fruits_coords:
                fruits[-1].regenerate_coords()
            fruits_coords.append(fruits[-1].get_fruit_coords())
            print("snake length: ", snake.length)
        else:
            fr.draw()
        
    # --- update the screen --- #
    pygame.display.flip()
 
    # --- Limit to 60 frames per second --- #
    clock.tick(60)
 
pygame.quit()