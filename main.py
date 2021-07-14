import pygame
import pymunk
from Ball import Ball

from pygame import mixer

import math

from pymunk import Vec2d
import pymunk.pygame_util

pygame.init()

winW = 396
winH = 700

size = [winW, winH]

display = pygame.display.set_mode(size)

ball_size = 26

back_img = pygame.image.load('images/table.png')
back_img = pygame.transform.scale(back_img, size)

ball_1_img = pygame.image.load('images/ball 1.png')
ball_1_img = pygame.transform.scale(ball_1_img, (ball_size, ball_size))

ball_img = pygame.image.load('images/ball_16.png')
ball_img = pygame.transform.scale(ball_img, (ball_size, ball_size))

balls = []

# основной шар на первой позиции
balls.append(Ball(ball_1_img, winW // 2, 534))

# остальные шары
# первый ряд
balls.append(Ball(ball_img, winW // 2, 300))

# второй ряд
balls.append(Ball(ball_img, winW // 2 - ball_size//2, 300 - ball_size))
balls.append(Ball(ball_img, winW // 2 + ball_size//2, 300 - ball_size))

# третий ряд
balls.append(Ball(ball_img, winW // 2 - ball_size, 300 - ball_size*2))
balls.append(Ball(ball_img, winW // 2, 300 - ball_size*2))
balls.append(Ball(ball_img, winW // 2 + ball_size, 300 - ball_size*2))

# четвертый ряд
balls.append(Ball(ball_img, winW // 2 - ball_size*1.5, 300 - ball_size*3))
balls.append(Ball(ball_img, winW // 2 - ball_size//2, 300 - ball_size*3))
balls.append(Ball(ball_img, winW // 2 + ball_size//2, 300 - ball_size*3))
balls.append(Ball(ball_img, winW // 2 + ball_size*1.5, 300 - ball_size*3))

# пятый ряд
balls.append(Ball(ball_img, winW // 2 - ball_size*2, 300 - ball_size*4))
balls.append(Ball(ball_img, winW // 2 - ball_size, 300 - ball_size*4))
balls.append(Ball(ball_img, winW // 2, 300 - ball_size*4))
balls.append(Ball(ball_img, winW // 2 + ball_size, 300 - ball_size*4))
balls.append(Ball(ball_img, winW // 2 + ball_size*2, 300 - ball_size*4))

clock = pygame.time.Clock()
FPS = 60


space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = 0,0       # Set its gravity

static_lines = [
    # верхний
    # ровная часть
    pymunk.Segment(space.static_body, (70, 46), (winW-70, 46), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (70, 46), (70 - 10, 46 - 10), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (winW-70, 46), (winW-70 + 10, 46-10), 1.0),


    # левый верхний
    # ровная часть
    pymunk.Segment(space.static_body, (46, 66), (46, winH // 2 - 27), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (46, 66), (46 - 10, 66 - 10), 1.0),
    # уголок
    pymunk.Segment(space.static_body,  (46, winH // 2 - 27), (46 - 10, winH // 2 - 27 + 5), 1.0),


    # левый нижний
    # ровная часть
    pymunk.Segment(space.static_body, (46,  winH // 2 + 19), (46, winH - 71), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (46,  winH // 2 + 19), (46 - 10, winH // 2 + 19 - 5), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (46, winH - 71), (46 - 10, winH - 71 + 10), 1.0),


    # правый верхний
    # ровная часть
    pymunk.Segment(space.static_body, (winW - 46, 66), (winW - 46, winH // 2 - 27), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (winW - 46, 66) , (winW - 46 + 10, 66 - 10), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (winW - 46, winH // 2 - 27), (winW - 46 + 10 , winH // 2 - 27 + 5), 1.0),


    # правый нижний
    # ровная часть
    pymunk.Segment(space.static_body, (winW - 46,  winH // 2 + 19), (winW - 46, winH  - 71), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (winW - 46,  winH // 2 + 19), (winW - 46 + 10,  winH // 2 + 19 - 5), 1.0),
    # уголок
    pymunk.Segment(space.static_body, (winW - 46, winH  - 71 ), (winW - 46 + 10, winH  - 71 + 10), 1.0),


    # нижний
    # ровная часть
    pymunk.Segment(space.static_body, (70, winH-46), (winW-70, winH-46), 1.0),
    pymunk.Segment(space.static_body, (70, winH-46), (70 - 10, winH-46 + 10), 1.0),
    pymunk.Segment(space.static_body, (winW-70, winH-46), (winW-70 + 10, winH-46 + 10), 1.0),
]

holes = [
    [37, 34],
    [winW - 37, 34],
    [37, winH - 36],
    [winW - 37, winH - 36],
    [29, winH // 2 - 2],
    [winW - 28, winH // 2 - 2]
]

for line in static_lines:
    line.elasticity = 0.3
    line.data = 'wall'

space.add(*static_lines)

for ball in balls:
    ball.add_to_space(space)

draw_options = pymunk.pygame_util.DrawOptions(display)



print_options = pymunk.SpaceDebugDrawOptions() # For easy printing

mouse_down = False
ball_selected = False
balls_moving = False
moves = 0
mouse_x = 0
mouse_y = 0

col_handler = space.add_default_collision_handler()
def begin(arbiter, space, data):
    if type(arbiter.shapes[1]) == pymunk.shapes.Circle:
        bullet_sound = mixer.Sound('sounds/ball_col.mp3')
        bullet_sound.play(0)
    elif type(arbiter.shapes[1]) == pymunk.shapes.Segment:
        bullet_sound = mixer.Sound('sounds/wall_col.mp3')
        bullet_sound.play(0)

    return True

col_handler.begin = begin


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_down = True
            if balls[0].rect.collidepoint(pygame.mouse.get_pos()) and balls_moving == False:
                ball_selected = True
            else:
                ball_selected = False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

            if ball_selected:
                ball_selected = False
                power = math.sqrt((mouse_x - balls[0].rect.centerx)**2+(mouse_y - balls[0].rect.centery)**2) * 1.5
                impulse = power * Vec2d((mouse_x - balls[0].rect.centerx)/power, (mouse_y - balls[0].rect.centery)/power)
                #print(power, impulse)
                balls[0].body.apply_impulse_at_world_point(impulse, balls[0].body.position)
                moves += 1
                bullet_sound = mixer.Sound('sounds/ball_col.mp3')
                bullet_sound.play(0)


        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

    display.blit(back_img, (0, 0))

    balls_moving = False



    for ball in balls:
        ball.rect.centerx = ball.body.position.x
        ball.rect.centery = ball.body.position.y
        if math.sqrt(ball.body.velocity.x ** 2 + ball.body.velocity.y**2) > 10:
            ball.body.velocity *= 0.995
        else:
            ball.body.velocity *= 0.5
        if math.sqrt(ball.body.velocity.x ** 2 + ball.body.velocity.y**2) > 2:
            #print(math.sqrt(ball.body.velocity.x ** 2 + ball.body.velocity.y**2))
            balls_moving = True
        pass
        #if ball.status == 'active':
        display.blit(ball.image, ball.rect)

        for hole in holes:
            dist =  math.sqrt((ball.rect.centerx - hole[0]) ** 2 + (ball.rect.centery - hole[1])**2)

            if dist < ball_size:
                pymunk.Body.update_velocity(ball.body, Vec2d(-ball.rect.centerx + hole[0],  -ball.rect.centery + hole[1]), 1, 1)
                #ball.body.velocity.y = -ball.rect.centery + hole[1]


            if dist < 5:
                space.remove(ball.body)
                balls.remove(ball)
                moves -= 1
                bullet_sound = mixer.Sound('sounds/hole_col.mp3')
                bullet_sound.play()

    #print(balls[0].body.position)
    #print(balls[0].body.velocity)
    dt = 1.0 / 60.0 / 5.0
    for x in range(5):
        space.step(dt)

    #space.debug_draw(draw_options)


    if ball_selected:

        pygame.draw.line(display, 'black', (balls[0].rect.centerx, balls[0].rect.centery), (mouse_x, mouse_y), 5)

    if len(balls) == 0:
        balls = []

        # основной шар на первой позиции
        balls.append(Ball(ball_1_img, winW // 2, 534))

        # остальные шары
        # первый ряд
        balls.append(Ball(ball_img, winW // 2, 300))

        # второй ряд
        balls.append(Ball(ball_img, winW // 2 - ball_size // 2, 300 - ball_size))
        balls.append(Ball(ball_img, winW // 2 + ball_size // 2, 300 - ball_size))

        # третий ряд
        balls.append(Ball(ball_img, winW // 2 - ball_size, 300 - ball_size * 2))
        balls.append(Ball(ball_img, winW // 2, 300 - ball_size * 2))
        balls.append(Ball(ball_img, winW // 2 + ball_size, 300 - ball_size * 2))

        # четвертый ряд
        balls.append(Ball(ball_img, winW // 2 - ball_size * 1.5, 300 - ball_size * 3))
        balls.append(Ball(ball_img, winW // 2 - ball_size // 2, 300 - ball_size * 3))
        balls.append(Ball(ball_img, winW // 2 + ball_size // 2, 300 - ball_size * 3))
        balls.append(Ball(ball_img, winW // 2 + ball_size * 1.5, 300 - ball_size * 3))

        # пятый ряд
        balls.append(Ball(ball_img, winW // 2 - ball_size * 2, 300 - ball_size * 4))
        balls.append(Ball(ball_img, winW // 2 - ball_size, 300 - ball_size * 4))
        balls.append(Ball(ball_img, winW // 2, 300 - ball_size * 4))
        balls.append(Ball(ball_img, winW // 2 + ball_size, 300 - ball_size * 4))
        balls.append(Ball(ball_img, winW // 2 + ball_size * 2, 300 - ball_size * 4))

        for ball in balls:
            ball.add_to_space(space)

        moves = 0

    font = pygame.font.SysFont(None, 30)
    img = font.render(str(moves), True, (255, 255, 255))
    text_rect = img.get_rect(center=(winW / 2, winH * 0.03))
    display.blit(img, text_rect)

    pygame.display.update()
    clock.tick(FPS)
