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

def collision(snake, snake_coords):
            if snake.get_coords() in snake_coords[1:]:
                return True
            return False


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

    def get_coords(self):
        return (self.rect.x, self.rect.y)


class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 24) * 20
        self.rect.y = random.randint(0, 24) * 20

    def draw(self):
        pygame.draw.rect(screen, RED, [self.rect.x, self.rect.y, 20, 20])

    def regenerate_coords(self):
        self.rect.x = random.randint(0, 24) * 20
        self.rect.y = random.randint(0, 24) * 20
        
    def get_coords(self):
        return (self.rect.x, self.rect.y)


size = (500, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Snake, or python idk")
 
done = False
clock = pygame.time.Clock()
snake = Snake()
fruits = []
frames_counter = 0
snake_coords = []

# Initializa the fruits
fruits_coords = []
for i in range(4):
    fruits.append(Fruit())
    # check if the fruit is not in the snake or in another fruit
    while fruits[i].get_coords() in fruits_coords or fruits[i].get_coords() in snake_coords:
        # if so, regenerate the fruit coords
        fruits[i].regenerate_coords()
    fruits_coords.append(fruits[i].get_coords())
    
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
    # every 30 frames the snake moves
    if frames_counter == 30:
        frames_counter = 0

        if snake.next_direction == "left":
            snake.direction = "left"
            snake.move(-20, 0)

        elif snake.next_direction == "right":
            snake.direction = "right"
            snake.move(20, 0)
            
        elif snake.next_direction == "up":
            snake.direction = "up"
            snake.move(0, -20)

        elif snake.next_direction == "down":
            snake.direction = "down"
            snake.move(0, 20)

        # insert the snake coords at the beginning of the snake_coords list
        snake_coords.insert(0, snake.get_coords())
    
        # remove the last element of the snake_coords list
        if len(snake_coords) > snake.length:
            snake_coords.pop()
        
        # print(snake_coords)
        
        # chech if the snake collides with itself 
        # if so, end the game
        if collision(snake, snake_coords):
            print("Game Over")
            done = True
   
    # --- Drawing code --- #

    draw_grid()
    snake.draw()

    # draw the snake tail
    for coord in snake_coords[1:]:
        pygame.draw.rect(screen, GREEN, [coord[0], coord[1], 20, 20])

    for fr in fruits:
        # check if the snake collides with a fruit
        if fr.get_coords() == snake.get_coords():
            fruits_coords.remove(fr.get_coords())
            fruits.remove(fr)
            # increase the snake length if it collides with a fruit
            snake.length += 1
            # add a new fruit
            fruits.append(Fruit())
            # check if the fruit is not in the snake or in another fruit
            while (fruits[-1].get_coords() in fruits_coords or fruits[-1].get_coords() in snake_coords) and snake.length <= 621:
                # if so, regenerate the fruit coords
                fruits[-1].regenerate_coords()

            # if the snake length is greater than 621, remove the last fruit
            if snake.length > 621:
                fruits.pop()
                
            fruits_coords.append(fruits[-1].get_coords())
            # print("snake length: ", snake.length)
        else:
            # draw the fruit
            fr.draw()
        
        
    # --- update the screen --- #
    pygame.display.flip()
 
    # --- Limit to 60 frames per second --- #
    clock.tick(60)
 
pygame.quit()

#TODO end the game when the snake collides with itself
#TODO add a score counter
#TODO add a score animation
#TODO add a restart button
#TODO add a game over screen
#TODO add a start screen
#TODO add a game over sound
#TODO add a background music
#TODO add a game over message
#TODO add a game over animation
#TODO win the game when the snake reaches a certain length
#TODO add a win screen
#TODO add a win sound
#TODO add a win message


