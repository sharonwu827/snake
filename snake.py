import sys
import pygame
from os.path import join, dirname
from random import randint,randrange


#set size
board_width = 40
board_height = 25
size= 25 # rectangle size for drawing snake and food
screen = pygame.display.set_mode((board_width,board_height)) #screen size

#set color

yellow = pygame.Color(192, 192, 192)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)

#set direction
left = (-1, 0)
right = (1, 0)
up = (0, -1)
down = (0, 1)


class Menu(object):
    def __init__(self):
        self.choice = 0

#Create the Snake
class Snake(object):
    def __init__(self):
        #set the snake starting postion and length for snack body, here I set it to 3 cell size
        self.pos = [(0,2), (0,1), (0,0)]
        self.dirt = down # make the initial move right
        self.ate = False
        self.speed = 30  #initial speed
        self.score = 0

    def draw(self, screen):
        #draw the rectangle for the blue snake
        for pos in self.pos:
            pygame.draw.rect(screen, blue, ((pos[0]*size, pos[1]*size), (size,size)))

    def move(self, ate):
        # if doesn't eat the egg, delete the last element of the snake,
        if not ate:
            self.pos.pop()

        #the new postion for the snake need to add the elements of the direction
        head = (self.pos[0][0] + self.dirt[0], self.pos[0][1] + self.dirt[1])

        #when snake hit itself or snack hit the wall then game over --- return False
        if head in self.pos or head[0] < 0 or head[1] < 0 or head[0] >= board_width or head[1] >= board_height:
            return False
        self.pos.insert(0, head) # previous head to the top of snake
        return True

    def eat(self, egg):
        #when eat the egg then score +1 and return True
        if self.pos[0] == egg.pos: #first element of snake reach the egg
            return True
        else:
            return False

class Egg(object):
    #random assign a cell to egg
    def __init__(self):
        self.pos = (randint(0, board_width - 1), randint(0, board_height - 1))

    #draw the rectangle for the yellow egg
    def draw(self, screen):
        pygame.draw.rect(screen, yellow, ((self.pos[0]*size, self.pos[1]*size), (size, size)))

    #update the egg postion if being ate
    def update(self, screen, ate, snake):
        if ate:
            self.pos = (randint(0, board_width - 1), randint(0, board_height - 1))
            if self.pos in snake.pos:
                self.draw(screen)
            else:
                self.draw(screen)
        else:
            self.draw(screen)


def message_display(screen, text, size, pos, color):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    prompt = font.render(text, True, yellow) #creates a new screen with text already drawn onto it.
    text_rect = prompt.get_rect() #returns a new rectangle covering the entire surface
    text_rect.center = pos
    screen.blit(prompt, text_rect) #blit the text surface onto your main screen.
    pygame.display.update() #update the screen for display

#display the text on screen when start/end the pragram
def select(screen, menu):
    while True:
        message_display(screen, 'Press Space to Start', 30, (board_width * size//2 , board_height * size // 2),black)
        message_display(screen, 'By Sharon Wu', 15, (board_width * size//2 , board_height * size // 2 + 30),black)
        pygame.display.update() #update the screen for display

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #click quit to end
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: #press space to start
                if event.key == pygame.K_SPACE:
                    return

#update the screen
def update(screen):
    screen.fill(white)
    for i in range(board_width):
        pygame.draw.line(screen, white, (i * size, 0), (i * size, board_height * size))
    for i in range(board_height):
        pygame.draw.line(screen, white, (0, i * size), (board_width * size, i * size))


def game_start(screen):
    menu = Menu()
    snake = Snake()
    egg = Egg()
    select(screen, menu)
    update(screen)
    egg.update(screen, snake.ate, snake)
    snake.draw(screen)
    pygame.display.update() # update the screen for display
    ttl, accelerate = 2, 0 # make the snake turn around, and add the current postion for the snake head to the elements of snakes

    while True:
        if accelerate:
            accelerate -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit when click the quit button on the screen
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: #capturing the keyboard input
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    if snake.dirt == up:
                        accelerate += ttl
                    elif not snake.dirt == down:
                        snake.dirt = up
                elif event.key == pygame.K_DOWN:
                    if snake.dirt == down:
                        accelerate += ttl
                    elif not snake.dirt == up:
                        snake.dirt = down
                elif event.key == pygame.K_LEFT:
                    if snake.dirt == left:
                        accelerate += ttl
                    elif not snake.dirt == right:
                        snake.dirt = left
                elif event.key == pygame.K_RIGHT:
                    if snake.dirt == right:
                        accelerate += ttl
                    elif not snake.dirt == left:
                        snake.dirt = right
                elif event.key == pygame.K_SPACE:
                    message_display(screen, 'Pause', 50, (board_width * size // 2, board_height * size // 2),black)
                    pause() #press the space and call the pause funtion
                break

        update(screen)
        egg.update(screen, snake.ate, snake)
        snake.draw(screen)
        message_display(screen, 'Score: %3d' % snake.score, 30,(board_width * size // 10 * 9, board_height * size // 15), red)

        if not snake.move(snake.ate):
            game_over(screen, menu, snake, egg)
            accelerate = 0

        if snake.eat(egg):
            snake.speed += 10
            snake.score += 1
            snake.ate = True
        else:
            snake.ate = False
        pygame.display.update() #ppdate portions of the screen for display


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def game_over(screen, menu, snake, egg):
    message_display(screen, 'Game Over, Press Space to Restart', 30, (board_width * size // 2, board_height * size // 2), red)
    #pause the pragram
    pause()
    #restart the game
    snake.__init__()
    egg.__init__()


def init_game():
    pygame.init()
    pygame.display.set_caption('Go eat egg! Snake!')
    screen = pygame.display.set_mode((board_width*size,board_height*size))
    return screen

def main():
    screen = init_game()
    game_start(screen)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pygame.quit()
        pygame.quit()
        sys.exit()
