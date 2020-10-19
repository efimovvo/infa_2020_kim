import pygame
import os
from pygame.draw import *
from random import randint

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('arial', 30)

FPS = 30
time = 0
screen_size = (1200, 900)
screen = pygame.display.set_mode(screen_size)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Variables
g = 2

# Add more balls targets
def new_balls(balls_number):
    for i in range(balls_number):
        x = randint(100, screen_size[0] - 100)
        y = randint(100, screen_size[1] - 100)
        r = randint(30, 50)
        dx = randint(-8, 8)
        dy = randint(-8, 8)
        color = COLORS[randint(0, 5)]
        circle(screen, color, (x, y), r)
        balls.append((x, y, r, dx, dy, color))


# Add more face targets
def new_face(faces_number):
    for i in range(faces_number):
        x = randint(100, 700)
        y = randint(100, 500)
        r = randint(60, 100)
        dx = randint(-16, 16)
        dy = randint(-16, 16)

        img = pygame.transform.scale(image, (r, r))
        screen.blit(img, (x, y))

        faces.append((x, y, r, dx, dy))


# Moving of targets with every frame
def new_frame():
    # Moving of balls
    for i in range(number_of_balls):
        x, y, r, dx, dy, color = balls[i]
        (x, y) = (x + dx, y + dy)
        if x - r < 0 or x + r > screen_size[0]:
            dx = -dx
        if y - r < 0 or y + r > screen_size[1]:
            dy = -dy
        balls[i] = (x, y, r, dx, dy, color)
    for i in range(number_of_balls):
        circle(screen, balls[i][5], (balls[i][0], balls[i][1]), balls[i][2])

    # Moving of faces
    for i in range(number_of_faces):
        x, y, r, dx, dy = faces[i]
        (x, y) = (x + dx, y + dy + g/2)
        dy += g
        if x < 0 or x + r > screen_size[0]:
            dx = -dx
        if y < 0 or y + r > screen_size[1]:
            dy = -dy
        faces[i] = (x, y, r, dx, dy)
    for i in range(number_of_faces):
        img = pygame.transform.scale(image, (faces[i][2], faces[i][2]))
        screen.blit(img, (faces[i][0], faces[i][1]))


# Check if player hit any targets
def click(cur_event):
    # Check if player hit any ball
    for i in range(number_of_balls):
        if (cur_event.pos[0]-balls[i][0])**2 + (cur_event.pos[1]-balls[i][1])**2 < balls[i][2]**2:
            global hits
            hits += 1
            rect(screen, WHITE, (0, 0, screen_size[0], screen_size[1]), 100)
            balls.pop(i)
            new_balls(1)
            break

    # Check if player hit any face
    for i in range(number_of_faces):
        if 0 < cur_event.pos[0] - faces[i][0] < faces[i][2] and 0 < cur_event.pos[1] - faces[i][1] < faces[i][2]:
            hits += 5
            rect(screen, WHITE, (0, 0, screen_size[0], screen_size[1]), 100)
            faces.pop(i)
            new_face(1)
            break


# Make a results table
def results_table():
    # Read existing table
    output = open("output.txt", 'r+')
    file = output.readlines()
    # Add new result
    file.append(str(hits) + " " + input("Enter your name: ") + '\n')
    for line in file:
        line = line.split(' ')
    file.sort(reverse=True)

    # Rewrite results
    output.seek(0)
    for line in file:
        output.write(line)
    output.close()


pygame.display.update()
clock = pygame.time.Clock()
finished = False

hits = 0
time_limit = 20
balls = []
number_of_balls = 50
new_balls(number_of_balls)

faces = []
number_of_faces = 10
# image of "face" targets
image = pygame.image.load(os.path.join('face.png'))
new_face(number_of_faces)

while time < FPS * 20:
    clock.tick(FPS)
    time += 1

    text_surface = my_font.render(str(hits), False, WHITE)
    screen.blit(text_surface, (0, 0))

    text_surface = my_font.render(str(time_limit - time // 30), False, WHITE)
    screen.blit(text_surface, (screen_size[0] // 2, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)

    new_frame()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

results_table()