import pygame
import random
import time
import fluidsynth
import threading


# Initialize FluidSynth
fs = fluidsynth.Synth()
fs.start(driver="coreaudio")  # Use "coreaudio" for macOS, "dsound" for Windows, "alsa" for Linux
sfid = fs.sfload("/Users/jakub/Downloads/FluidR3/FluidR3_GM.sf2")
fs.program_select(0, sfid, 0, 0)

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
 
notes_sequence = [76, 12, 76, 12, 20, 12, 76, 12, 20, 12, 72, 12, 76, 12, 20, 12, 79, 12, 20, 36, 67, 12, 20, 36, 72, 12, 20,
24, 67, 12, 20, 24, 64, 12, 20, 24, 69, 12, 20, 12, 71, 12, 20, 12, 70, 12, 69, 12, 20, 12, 67, 16, 76, 16, 79, 16, 81, 12, 20,
12, 77, 12, 79, 12, 20, 12, 76, 12, 20, 12, 72, 12, 74, 12, 71, 12, 20, 24, 48, 12, 20, 12, 79, 12, 78, 12, 77, 12, 75, 12, 60,
12, 76, 12, 53, 12, 68, 12, 69, 12, 72, 12, 60, 12, 69, 12, 72, 12, 74, 12, 48, 12, 20, 12, 79, 12, 78, 12, 77, 12, 75, 12, 55,
12, 76, 12, 20, 12, 84, 12, 20, 12, 84, 12, 84, 12, 55, 12, 20, 12, 48, 12, 20, 12, 79, 12, 78, 12, 77, 12, 75, 12, 60, 12, 76,
12, 53, 12, 68, 12, 69, 12, 72, 12, 60, 12, 69, 12, 72, 12, 74, 12, 48, 12, 20, 12, 75, 24, 20, 12, 74, 24, 20, 12, 72, 24, 20,
12, 55, 12, 55, 12, 20, 12, 48, 12, 72, 12, 72, 12, 20, 12, 72, 12, 20, 12, 72, 12, 74, 12, 20, 12, 76, 12, 72, 12, 20, 12, 69,
12, 67, 12, 20, 12, 43, 12, 20, 12, 72, 12, 72, 12, 20, 12, 72, 12, 20, 12, 72, 12, 74, 12, 76, 12, 55, 12, 20, 24, 48, 12, 20,
24, 43, 12, 20, 12, 72, 12, 72, 12, 20, 12, 72, 12, 20, 12, 72, 12, 74, 12, 20, 12, 76, 12, 72, 12, 20, 12, 69, 12, 67, 12, 20,
12, 43, 12, 20, 12, 76, 12, 76, 12, 20, 12, 76, 12, 20, 12, 72, 12, 76, 12, 20, 12, 79, 12, 20, 36, 67, 12, 20, 36, 76, 12, 72,
12, 20, 12, 67, 12, 55, 12, 20, 12, 68, 12, 20, 12, 69, 12, 77, 12, 53, 12, 77, 12, 69, 12, 60, 12, 53, 12, 20, 12, 71, 16, 81,
16, 81, 16, 81, 16, 79, 16, 77, 16, 76, 12, 72, 12, 55, 12, 69, 12, 67, 12, 60, 12, 55, 12, 20, 12, 76, 12, 72, 12, 20, 12, 67,
12, 55, 12, 20, 12, 68, 12, 20, 12, 69, 12, 77, 12, 53, 12, 77, 12, 69, 12, 60, 12, 53, 12, 20, 12, 71, 12, 77, 12, 20, 12, 77,
12, 77, 16, 76, 16, 74, 16, 72, 12, 64, 12, 55, 12, 64, 12, 60, 12, 20, 36, 72, 12, 20, 24, 67, 12, 20, 24, 64, 24, 69, 16, 71,
16, 69, 16, 68, 24, 70, 24, 68, 24, 67, 12, 65, 12, 67, 48]


def play_coin_sound_thread(velocity=127):
    fs.noteon(0, 83, velocity)
    time.sleep(0.1)
    fs.noteon(0, 88, velocity)
    fs.noteoff(0, 83)
    fs.noteoff(0, 88)

def play_coin_sound():
    thread = threading.Thread(target=play_coin_sound_thread)
    thread.start()



# Function to play a MIDI note
def play_midi_note_thread(note, duration=0.5, velocity=127):
    fs.noteon(0, note, velocity)
    time.sleep(duration)
    fs.noteoff(0, note)

def play_midi_note(note, duration=0.5, velocity=127):
    if note != 20:
        thread = threading.Thread(target=play_midi_note_thread, args=(note, duration, velocity))
        thread.start()

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
        self.color = DARK_GREEN
        self.image.fill(self.color)
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
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, 20, 20])

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
font = pygame.font.Font(None, 36)
fruits = []
music_frames_counter = 0
frames_counter = 0
snake_coords = []
fps = 60

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
n = 0
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
    music_frames_counter += 1
   
    # every 30 frames the snake moves

    if music_frames_counter == 14:
        if n < len(notes_sequence) - 1:
            play_midi_note(notes_sequence[n], notes_sequence[n + 1]//12)
            # print(notes_sequence[n])
            # print(notes_sequence[n + 1]//12)

            n += 2
        else:
            n = 0
        music_frames_counter = 0
    
    if frames_counter == 28:
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
        pygame.draw.rect(screen, GREEN, [coord[0], coord[1], 20, 20], 7)
   
    for fr in fruits:
        # check if the snake collides with a fruit
        if fr.get_coords() == snake.get_coords():
            fruits_coords.remove(fr.get_coords())
            fruits.remove(fr)
            # play_midi_note(random.choice(notes_sequence))  # Play a random note when the snake eats a fruit
            play_coin_sound()
            # increase the snake length if it collides with a fruit
            snake.length += 1
            fps += 1
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
        
    score_text = font.render("Score: " + str(snake.length), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # --- update the screen --- #
    pygame.display.flip()
 
    # --- Limit to 60 frames per second --- #
    clock.tick(fps)
 

# Close the MIDI output device
fs.delete()


pygame.quit()

#TODO add a score animation
#TODO add a restart button
#TODO add a game over screen
#TODO add a start screen
#TODO add a game over sound
#TODO add a game over message
#TODO add a game over animation
#TODO win the game when the snake reaches a certain length
#TODO add a win screen
#TODO add a win sound
#TODO add a win message


