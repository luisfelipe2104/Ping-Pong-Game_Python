import pygame
pygame.init()

#----------------------------------------------------------------------------------------------

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (194, 17, 17)
BLUE = (17, 35, 194)
GREEN = (39, 204, 58)

PADDLE_HEIGHT, PADDLE_WIDTH = 100, 20
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WINNING_SCORE = 10

#----------------------------------------------------------------------------------------------

class Paddle:
    
    VEL = 4

    def __init__(self, x, y, width, height, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):   # draws the paddle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))  # creates a rectangle

    def move(self, up=True):
        if up:
            self.y -= self.VEL  # moves up
        else:
            self.y += self.VEL  # moves down

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        

#----------------------------------------------------------------------------------------------

class Ball:
    MAX_VEL = 5
 

    def __init__(self, x, y, radius, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        
#----------------------------------------------------------------------------------------------

def draw(win, paddles, ball, red_score, blue_score):
    win.fill(BLACK)

    blue_score_text = SCORE_FONT.render(f"{blue_score}", 1, WHITE)
    red_score_text = SCORE_FONT.render(f"{red_score}", 1, WHITE)
    win.blit(blue_score_text, (WIDTH//4 - blue_score_text.get_width() // 2, 20))
    win.blit(red_score_text, (WIDTH * (3/4) - red_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)    # draws the paddle

    for i in range(10, HEIGHT, HEIGHT//20):   # draws the dotted line
        if i % 2 == 1:  # if i == an even number, it doesn't draw the dotted line
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()  # performs all the drawing operations

#----------------------------------------------------------------------------------------------

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1    # if the ball hits the bottom ceiling it'll go in the opposite direction
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1    # if the ball hits the top ceiling it'll go in the opposite direction

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1    # handles the collision to the left paddle

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1  # handles the collision to the right paddle

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

#----------------------------------------------------------------------------------------------

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
    
#----------------------------------------------------------------------------------------------

# game loop
def main():
    run = True
    clock = pygame.time.Clock()     # runs at the same speed in every computer

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, BLUE)  # creates the object LEFT PADDLE

    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, RED)  # creates the object RIGHT PADDLE

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, GREEN)

    blue_score = 0
    red_score = 0

    while run:
        clock.tick(FPS) # won't run faster than 60fps
        draw(WIN, [left_paddle, right_paddle], ball, red_score, blue_score)   # draws the paddle
        for event in pygame.event.get():    # gets all the events
            if event.type == pygame.QUIT:   # if you hit the red button on the top right corner
                run = False
                break   # stops the main loop

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            red_score += 1  # if it's beyond the screen
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        elif ball.x > WIDTH:
            blue_score += 1 # if it's beyond the screen
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        won = False
        if red_score >= WINNING_SCORE:
            won = True
            win_text = "Red Player Won!"

        elif blue_score >= WINNING_SCORE:
            won = True
            win_text = "Blue Player Won!"
        
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            red_score = 0
            blue_score = 0
    
    pygame.quit()   # quits pygame

#----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()