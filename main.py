################################################################################
# Sort data setup
################################################################################
import random

range_min = 1
range_max = 20
elem_count = 25
data_to_sort = []


def calc_data():
    global data_to_sort
    data_to_sort = []
    for _ in range(elem_count):
        data_to_sort.append(random.randint(range_min, range_max))


################################################################################
# Params for sort visualization
################################################################################
import pygame

pygame.init()

rect_color = (255, 0, 0)
text_color = (0, 255, 0)

font_values = pygame.font.Font('freesansbold.ttf', 16)
font_info = pygame.font.Font('freesansbold.ttf', 14)
font_sorted = pygame.font.Font('freesansbold.ttf', 30)

text = font_values.render(str(range_max), True, text_color)
textRect = text.get_rect()

block_width = textRect.width
block_gap = 5
block_offset = block_width + block_gap
one_block_height = block_width
border_offset = font_info.get_height() + 2

screen_width = elem_count * block_offset - block_gap + 2 * border_offset
screen_height = one_block_height * range_max + font_values.get_height() + 2 * border_offset

screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Sort view')

is_pause = False
is_sorted = False
is_show_info = False
is_demo_enabled = True
is_sort_from_small_to_greater = True

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 200)


################################################################################
# Wrappers over draw calls
################################################################################
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


def draw_text(surface, color, pos, value, font, bgcolor=None, alpha=None):
    text = font.render(str(value), True, color, bgcolor)
    textRect = text.get_rect()
    textRect.center = pos
    if alpha is not None:
        text.set_alpha(alpha)
    surface.blit(text, textRect)


################################################################################
# Draw modes
################################################################################
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
draw_mode = 'rect'


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


################################################################################
# Main logic functions
################################################################################
def draw_elem(surface, color, pos, index, value):
    draw_func = draw_modes_dict[draw_mode]
    draw_func(surface, color, pos, index, value)


def draw_data(surface, rect_color, text_color, pos, data):
    start_x, start_y = pos
    for n, x in enumerate(data):
        draw_elem(surface, rect_color, pos, n, x)

        text_pos = (start_x + block_offset * n + block_width / 2, start_y + x * one_block_height + font_values.get_height() / 2)
        draw_text(surface, text_color, translate_pos(text_pos), x, font_values)


def sort_need_swap(left, right):
    if is_sort_from_small_to_greater:
        return left > right
    else:
        return left < right


def step():
    global is_sorted
    if is_sorted:
        return
    has_swap = False
    for i in range(len(data_to_sort) - 1):
        if sort_need_swap(data_to_sort[i], data_to_sort[i + 1]):
            temp = data_to_sort[i]
            data_to_sort[i] = data_to_sort[i+1]
            data_to_sort[i+1] = temp
            has_swap = True
    if not has_swap:  # means that we already have sorted list
        is_sorted = True


def update():
    if is_pause:
        return

    step()


def reset():
    global is_sorted
    is_sorted = False
    calc_data()


def draw_info_text(surface):
    if is_show_info:
        info = [
            "[SPACE] - play/stop animation",
            "[R] - reset",
            "[D] - change draw mode",
            "[C] - change sort direction",
            "[N] - next sort step",
            "[S] - demo",
            "[TAB] - hide this help info",
        ]
        for n, text_value in enumerate(info):
            pos = (screen_width / 2,
                   screen_height - border_offset - font_info.get_height() / 2 - (font_info.get_height() + 3) * n)
            draw_text(surface, (0, 0, 255), translate_pos(pos), text_value, font_info, (255, 255, 255), 200)
    else:
        pos = (screen_width / 2,
               screen_height - font_info.get_height() / 2)
        draw_text(surface, (0, 0, 255), translate_pos(pos), "[TAB] - show help", font_info, (255, 255, 255), 75)


def draw_sorted_text(surface):
    if not is_sorted:
        return

    pos = (screen_width / 2, block_offset + font_sorted.get_height())
    draw_text(surface, (255, 0, 0), translate_pos(pos), "SORTED", font_sorted, (255, 255, 255), 200)


def set_random_draw_mode():
    for _ in range(random.randint(0, len(draw_modes))):
        next_draw_mode()


def set_random_sort_direction():
    global is_sort_from_small_to_greater
    for _ in range(random.randint(0, 20)):
        is_sort_from_small_to_greater = not is_sort_from_small_to_greater


################################################################################
# Main logic
################################################################################
reset()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            update()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                reset()
            elif event.key == pygame.K_n:
                step()
            elif event.key == pygame.K_s:
                is_demo_enabled = not is_demo_enabled
                is_pause = not is_demo_enabled
            elif event.key == pygame.K_c:
                is_sort_from_small_to_greater = not is_sort_from_small_to_greater
            elif event.key == pygame.K_SPACE:
                is_pause = not is_pause
            elif event.key == pygame.K_d:
                next_draw_mode()
            elif event.key == pygame.K_TAB:
                is_show_info = not is_show_info

    # do some updates
    if is_demo_enabled:
        if is_sorted is True:
            set_random_draw_mode()
            set_random_sort_direction()
            reset()

    # draw black background
    screen.fill((0, 0, 0))

    # draw list elements
    draw_data(screen, rect_color, text_color, (border_offset, border_offset), data_to_sort)
    draw_info_text(screen)
    draw_sorted_text(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()