import pygame
from pygame.locals import *
from math import cos, radians


# функция, сравнивающая знаки двух чисел
def same_sign(a, b):
    return (a * b) >= 0


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True
clock = pygame.time.Clock()
FPS = 60
speed = 5  # скорость перемещения крюка
rotation_speed = 2  # скорость поворота
# положение крана (вид сбоку)
crane_side_view_X = 925
crane_side_view_Y = 225
arrow_angle = 0  # угол поворота стрелы
trolley_side_view_Y = crane_side_view_Y + 137  # начальное положение тележки

# загрузка изображений
crane_side_view = pygame.image.load('crane/crane_side_view.png')
trolley_side_view = pygame.image.load('crane/trolley_part_side_view.png')
hook_side_view = pygame.image.load('crane/hook_side_view.png')
arrow_up_view = pygame.image.load('crane/arrow.png')

# оптимизация изображений
crane_side_view.convert()
trolley_side_view.convert()
hook_side_view.convert()

# ограничения по перемещению тележки и крюка
trolley_side_view_X_min = crane_side_view_X + 255
trolley_side_view_X_max = crane_side_view_X + crane_side_view.get_width()
hook_side_view_Y_min = trolley_side_view_Y + trolley_side_view.get_height() + 15
hook_side_view_Y_max = crane_side_view_Y + crane_side_view.get_height() - 30

# создание невидимых рамок у тележки и крюка
trolley_side_view_rect = trolley_side_view.get_rect()
hook_side_view_rect = hook_side_view.get_rect()

# начальное положение тележки и крюка
hook_side_view_rect.midtop = trolley_side_view_X_min + trolley_side_view.get_width() // 2, hook_side_view_Y_min
trolley_side_view_rect.topleft = trolley_side_view_X_min, trolley_side_view_Y

# создание надписей
font = pygame.font.SysFont(None, 32)
label_above_view = font.render('Вид сверху', True, BLACK)
label_above_view_rect = label_above_view.get_rect()
label_above_view_rect.center = 409, 36
label_side_view = font.render('Вид сбоку', True, BLACK)
label_side_view_rect = label_side_view.get_rect()
label_side_view_rect.center = crane_side_view_X+crane_side_view.get_width()//2, crane_side_view_Y-15

# флаги для перемещения крюка и поворта стрелы
hook_move_left = False
hook_move_right = False
hook_move_up = False
hook_move_down = False
crane_orientation = True
crane_orientation_change = False
arrow_rotation_clockwise = False
arrow_rotation_counterclockwise = False

while running:
    # обработка нажатий на клавиши
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_a:
                hook_move_left = True
            elif event.key == K_d:
                hook_move_right = True
            elif event.key == K_w:
                hook_move_up = True
            elif event.key == K_s:
                hook_move_down = True
            elif event.key == K_e:
                arrow_rotation_clockwise = True
            elif event.key == K_q:
                arrow_rotation_counterclockwise = True
        elif event.type == KEYUP:
            if event.key in [K_a, K_d, K_w, K_s, K_e, K_q]:
                hook_move_up = hook_move_down = hook_move_left = hook_move_right = arrow_rotation_clockwise = arrow_rotation_counterclockwise = 0
    # перемещение крюка вправо
    if hook_move_right:
        if trolley_side_view_rect.right + speed < trolley_side_view_X_max:
            trolley_side_view_rect.move_ip(speed, 0)
            hook_side_view_rect.centerx = trolley_side_view_rect.centerx
    # перемещение крюка вплево
    if hook_move_left:
        if trolley_side_view_rect.left - speed > trolley_side_view_X_min:
            trolley_side_view_rect.move_ip(-speed, 0)
            hook_side_view_rect.centerx = trolley_side_view_rect.centerx
    # перемещение крюка вверх
    if hook_move_up:
        if hook_side_view_rect.top - speed > hook_side_view_Y_min:
            hook_side_view_rect.move_ip(0, -speed)
            hook_side_view_rect.centerx = trolley_side_view_rect.centerx
    # перемещение крюка вниз
    if hook_move_down:
        if hook_side_view_rect.bottom + speed < hook_side_view_Y_max:
            hook_side_view_rect.move_ip(0, speed)
            hook_side_view_rect.centerx = trolley_side_view_rect.centerx
    # вращение стрелы по часовой стрелке
    if arrow_rotation_clockwise:
        if not same_sign(cos(radians(arrow_angle)), cos(radians(arrow_angle - rotation_speed))):
            crane_orientation_change = True
        arrow_angle -= rotation_speed
    # вращение стрелы против часовой стрелки
    if arrow_rotation_counterclockwise:
        if not same_sign(cos(radians(arrow_angle)), cos(radians(arrow_angle + rotation_speed))):
            crane_orientation_change = True
        arrow_angle += rotation_speed
    # изменение ориентации крана (вид сбоку)
    if crane_orientation_change:
        if crane_orientation:
            trolley_side_view_X_min = crane_side_view_X
            trolley_side_view_X_max = trolley_side_view_X_min + crane_side_view.get_width() - 255
            trolley_side_view_rect.right = 2 * crane_side_view_X + crane_side_view.get_width() - \
                                           trolley_side_view_rect.topleft[0]
            hook_side_view_rect.centerx = trolley_side_view_rect.centerx
            crane_orientation = False
        elif not crane_orientation:
            trolley_side_view_X_min = crane_side_view_X + 255
            trolley_side_view_X_max = crane_side_view_X + crane_side_view.get_width()
            trolley_side_view_rect.left = 2 * crane_side_view_X + crane_side_view.get_width() - \
                                          trolley_side_view_rect.topright[0]
            hook_side_view_rect.centerx = trolley_side_view_rect.centerx
            crane_orientation = True
        crane_side_view = pygame.transform.flip(crane_side_view, True, False)
        trolley_side_view = pygame.transform.flip(trolley_side_view, True, False)
        crane_orientation_change = False

    # позиционирование стрелы
    arrow_up_view_rotated = pygame.transform.rotate(arrow_up_view, arrow_angle)
    arrow_up_view_rotated.convert()
    arrow_up_view_rotated_rect = arrow_up_view_rotated.get_rect()
    arrow_up_view_rotated_rect.center = 409, 460
    # отрисовка объектов
    screen.fill(WHITE)
    screen.blit(crane_side_view, (crane_side_view_X, crane_side_view_Y))
    screen.blit(trolley_side_view, trolley_side_view_rect)
    screen.blit(hook_side_view, hook_side_view_rect)
    screen.blit(arrow_up_view_rotated, arrow_up_view_rotated_rect)
    screen.blit(label_above_view, label_above_view_rect)
    screen.blit(label_side_view, label_side_view_rect)
    pygame.draw.rect(screen, BLACK, (trolley_side_view_rect.centerx - 5, trolley_side_view_rect.bottom, 10,
                                     hook_side_view_rect.top - trolley_side_view_rect.bottom))
    pygame.draw.circle(screen, BLACK, arrow_up_view_rotated_rect.center, arrow_up_view.get_width() // 2, 1)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
