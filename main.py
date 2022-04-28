# first calc data to sort
import random

range_min = 1
range_max = 25
data_to_sort = []


def calc_data():
    global data_to_sort
    data_to_sort = []
    for _ in range(50):
        data_to_sort.append(random.randint(range_min, range_max))


calc_data()

# visualization of bubble sort
import pygame
pygame.init()

rect_color = (255, 0, 0)
text_color = (0, 255, 0)

data_count = len(data_to_sort)
max_value = max(data_to_sort)

font_height = 18
font = pygame.font.Font('freesansbold.ttf', font_height)

text = font.render(str(range_max), True, text_color)
textRect = text.get_rect()


text_y_offset = font_height / 2

block_width = textRect.width
block_gap = 5
block_offset = block_width + block_gap
# one_block_height = 5
one_block_height = block_width
border_offset = 10

screen_width = data_count * block_offset - block_gap + 2 * border_offset
screen_height = one_block_height * max_value + 2 * border_offset + font_height

screen = pygame.display.set_mode([screen_width, screen_height])

is_pause = True

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 200)


def draw_mode_rect(surface, color, pos, index, value):
    start_x, start_y = pos
    rect_pos = (start_x + block_offset * index, start_y)
    draw_rect(surface, color, rect_pos, block_width, value * one_block_height)


def draw_mode_circle(surface, color, pos, index, value):
    start_x, start_y = pos
    circle_pos = (start_x + block_offset * index + block_width / 2,
                  start_y + value * one_block_height - block_width / 2)
    draw_circle(surface, color, circle_pos, block_width / 2)


def draw_mode_circles(surface, color, pos, index, value):
    start_x, start_y = pos
    for n in range(1, value+1):
        circle_pos = (start_x + block_offset * index + block_width / 2,
                      start_y + n * one_block_height - block_width / 2)
        draw_circle(surface, color, circle_pos, block_width / 2)


def draw_mode_cross(surface, color, pos, index, value):
    start_x, start_y = pos
    line_width = 3
    start_pos_y = (start_x + block_offset * index,
                   start_y + value * one_block_height - block_width / 2)
    end_pos_y = (start_x + block_offset * index + block_width,
                 start_y + value * one_block_height - block_width / 2)
    start_pos_x = (start_x + block_offset * index + block_width / 2,
                   start_y + value * one_block_height - block_width)
    end_pos_x = (start_x + block_offset * index + block_width / 2,
                 start_y + value * one_block_height)
    draw_line(surface, color, start_pos_y, end_pos_y, line_width)
    draw_line(surface, color, start_pos_x, end_pos_x, line_width)


draw_modes = [
    ('rect', draw_mode_rect),
    ('circle', draw_mode_circle),
    ('circles', draw_mode_circles),
    ('cross', draw_mode_cross),
]

draw_modes_dict = dict(draw_modes)
print(draw_modes_dict)

draw_mode = 'circle'


def next_draw_mode():
    global draw_mode
    global draw_modes
    idx = 0
    for n, (mode_name, mode_func) in enumerate(draw_modes):
        if mode_name == draw_mode:
            idx = n
            break

    if idx + 1 == len(draw_modes):
        idx = 0
    else:
        idx += 1
    draw_mode = draw_modes[idx][0]


def translate_pos(pos):
    x, y = pos
    return x, -y + screen_height


# pos - left bottom rect corner pos
def draw_rect(surface, color, pos, width, height):
    left, top = translate_pos(pos)
    pygame.draw.rect(surface, color, pygame.Rect(left, top - height, width, height))


def draw_circle(surface, color, center, radius):
    pygame.draw.circle(surface, color, translate_pos(center), radius)


def draw_line(surface, color, start, end, width=1):
    pygame.draw.line(surface, color, translate_pos(start), translate_pos(end), width=width)


def draw_text(surface, color, pos, value):
    text = font.render(str(value), True, color)
    textRect = text.get_rect()
    textRect.center = pos
    surface.blit(text, textRect)


def draw_elem(surface, color, pos, index, value):
    draw_func = draw_modes_dict[draw_mode]
    draw_func(surface, color, pos, index, value)


def draw_data(surface, rect_color, text_color, pos, data):
    start_x, start_y = pos
    for n, x in enumerate(data):
        draw_elem(surface, rect_color, pos, n, x)

        text_pos = (start_x + block_offset * n + block_width / 2, start_y + x * one_block_height + text_y_offset)
        draw_text(surface, text_color, translate_pos(text_pos), x)


def step():
    for i in range(len(data_to_sort) - 1):
        if data_to_sort[i] > data_to_sort[i + 1]:
            temp = data_to_sort[i]
            data_to_sort[i] = data_to_sort[i+1]
            data_to_sort[i+1] = temp


def update():
    if not is_pause:
        step()


def reset():
    calc_data()


running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            update()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_n:
                step()
            if event.key == pygame.K_SPACE:
                is_pause = not is_pause
            if event.key == pygame.K_d:
                next_draw_mode()

    screen.fill((0, 0, 0))
    draw_data(screen, rect_color, text_color, (border_offset, border_offset), data_to_sort)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()