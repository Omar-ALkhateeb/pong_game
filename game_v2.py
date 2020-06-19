# Import the pygame library and initialise the game engine
import pygame
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
pong = pd.read_csv('pong_intern.csv')

clf = KNeighborsRegressor(n_neighbors=3)

pong.drop_duplicates()
y = pong['Paddle.y']
x = pong.drop(columns='Paddle.y')


clf = clf.fit(x, y)
df = pd.DataFrame(columns=['x', 'y', 'vx', 'vy'])

pygame.init()

bgcolor = pygame.Color(0, 0, 0)
fgcolor = pygame.Color(255, 255, 255)

# Open a new window
WIDTH = 700
HEIGHT = 500
BORDER = 10
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

pygame.display.flip()
pygame.display.set_caption("Pong")

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carry_on = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()


class Ball:
    RADIUS = 10
    VELOCITY = 4

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def show(self):
        # global screen
        # global fgcolor
        pygame.draw.circle(
            screen, fgcolor, (int(self.x), int(self.y)), self.RADIUS)

    # def increase_vel(self):
    #     self.vx *= 1.02
    #     self.vy *= 1.02

    def update(self, AI_pos):
        newx = self.x + self.vx
        newy = self.y + self.vy
        paddle_y_range = range(int(AI_pos)-Paddle.HEIGHT//2,
                               int(AI_pos)+Paddle.HEIGHT//2)
        paddle_x_range = range(WIDTH-Paddle.WIDTH-self.RADIUS,
                               WIDTH-Paddle.WIDTH+self.RADIUS)
        # print(self.x, WIDTH-Paddle.WIDTH)
        if newy < (0+BORDER+self.RADIUS) or newy >= (HEIGHT-BORDER-self.RADIUS):
            self.vy *= -1
        if newx < (0+BORDER+self.RADIUS):
            self.vx *= -1
        if newx in paddle_x_range and newy in paddle_y_range:
            self.vx = -1*abs(self.vx)
            print('hit')
            # self.increase_vel()
            # self.vy *= -1
        if(newx > WIDTH):
            global carry_on
            carry_on = False
        else:
            self.x += self.vx
            self.y += self.vy


class Paddle:
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, y):
        self.y = y

    def show(self):
        pygame.draw.rect(screen, fgcolor, pygame.Rect(
            (WIDTH-self.WIDTH, self.y-self.HEIGHT//2, self.WIDTH, self.HEIGHT)))

    def update(self, AI_pos):
        # print(self.y)
        # self.y = pygame.mouse.get_pos()[1]
        print(AI_pos)
        self.y = AI_pos


ball_play = Ball(WIDTH-Ball.RADIUS, HEIGHT//2, -Ball.VELOCITY, -Ball.VELOCITY)
paddle_play = Paddle(HEIGHT//2)

#  train a new AI
# db = open('pong_intern.csv', 'w')

# print('x,y,vx,vy,Paddle.y', file=db)

# -------- Main Program Loop -----------
while carry_on:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carry_on = False  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                carry_on = False
    # --- Drawing code should go here
    # First, clear the screen to black.
    screen.fill(bgcolor)
    # Draw the net
    pygame.draw.line(screen, fgcolor, [349, 0], [349, 500], 5)
    # draw the borders
    pygame.draw.rect(screen, fgcolor,
                     pygame.Rect((0, 0, WIDTH, BORDER)))
    pygame.draw.rect(screen, fgcolor,
                     pygame.Rect((0, 0, BORDER, HEIGHT)))
    pygame.draw.rect(screen, fgcolor,
                     pygame.Rect((0, HEIGHT-BORDER, WIDTH, BORDER)))

    to_predict = df.append({'x': ball_play.x, 'y': ball_play.y,
                            'vx': ball_play.vx, 'vy': ball_play.vy}, ignore_index=True)
    AI_move = clf.predict(to_predict)
    ball_play.VELOCITY += 0.1
    # print(AI_move)

    ball_play.show()
    ball_play.update(AI_move)
    paddle_play.update(AI_move)
    paddle_play.show()

    # print('{},{},{},{},{}'.format(ball_play.x, ball_play.y, ball_play.vx, ball_play.vy, paddle_play.y), file=db)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
