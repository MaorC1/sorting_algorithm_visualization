import random as rnd
import pygame

pygame.init()

class DrawInformation:
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    GRAY = 128, 128, 128
    GREEN = 0, 255, 0
    RED = 255, 0, 0

    BACKGROUND_COLOR = WHITE
    SIDE_PAD = 100 # in px
    TOP_PAD = 150 # in px
    LEFT_SIDE_MENU = 400 # left side menu 300 px

    # init fonts
    FONT = pygame.font.SysFont('comicsans', 30)
    SMALL_FONT = pygame.font.SysFont('comicsans', 25)

    COLORS = [GRAY, (160, 160, 160), (192, 192, 192)]


    def __init__(self, width: int, height: int, numbers_lst: list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm")

        self.set_lst(numbers_lst)

    def set_lst(self, lst: list):
        self.lst = lst
        # get the full range of the list
        self.min_val = min(lst)
        self.max_val = max(lst)

        # get the block width in px
        self.block_width = round((self.width - self.SIDE_PAD - self.LEFT_SIDE_MENU / 2) / len(lst))

        # get the full range of the numbers list and clac each block px size (result = Xpx * Y number)
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        # pygame start from the top left corner, the start of the block is the bottom left size (dividing by 2)
        self.start_x = (self.LEFT_SIDE_MENU + self.SIDE_PAD) // 2

def draw_lst(draw_info: DrawInformation, color_positions={}, clear_bg=False):
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.WHITE, clear_rect)  # clear with white rect

    for i, value in enumerate(draw_info.lst):
        # multiple but each index to move the bar on the x-axis to the right (no overlap)
        x = draw_info.start_x + (i * draw_info.block_width)
        y = draw_info.height - (value - draw_info.min_val + 1) * draw_info.block_height # add 1 to display the min values

        block_color = draw_info.COLORS[i % 3] # always would give 0,1 or 2

        if i in color_positions:
            print(i)
            block_color = color_positions[i] # change the color
            print(block_color)

        pygame.draw.rect(surface=draw_info.window, color=block_color, rect=(x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()
        # time.sleep(0.2)

def draw(draw_info: DrawInformation, algorithm_name: str, ascending: bool):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_text(draw_info, algorithm_name, ascending)
    draw_lst(draw_info)
    pygame.display.update()  # render the display

def draw_text(draw_info: DrawInformation, algorithm_name, ascending):
    # display title with sorting algorithm name and sorting order
    title = draw_info.FONT.render(f"{algorithm_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    # draw the line separating from the menu
    menu_x = draw_info.start_x - 50
    pygame.draw.line(draw_info.window, draw_info.GRAY, (menu_x, 0), (menu_x, draw_info.height), 2)

    # create menu texts
    text_menu_ls = ["space - sort", "r - Restart", "a - ascending", "d - descending"]
    labels = []
    for text in text_menu_ls:
        labels.append(draw_info.SMALL_FONT.render(text, 1, draw_info.BLACK))

    y_title_position = 10
    x_title_position = 10
    for label in labels:
        draw_info.window.blit(label, (x_title_position, y_title_position))
        y_title_position += 50

    # controls = draw_info.FONT.render("1 - sort1, \n 2 - sort2", 1, draw_info.BLACK)
    # draw_info.window.blit(controls, (0, 10))


def generate_list(n: int, min_val: int, max_val: int):
    return [rnd.randint(min_val, max_val) for _ in range(n)]

def main():
    run_visualization = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 1
    max_val = 10

    lst = generate_list(n, min_val, max_val)
    draw_information = DrawInformation(1000, 600, lst)

    sorting = False
    ascending = True
    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_generator = None

    while run_visualization:
        clock.tick(60) # fps of the loop

        if sorting:
            try:
                next(sorting_generator)
            except StopIteration as e:
                sorting = False # no more values

        draw(draw_information, sorting_algo_name, ascending)

        for event in pygame.event.get(): # get all the events that happened
            if event == pygame.QUIT:
                run_visualization = False

            if event.type != pygame.KEYDOWN: # need this so the program wouldn't crash immediately
                continue

            if event.key == pygame.K_r: # press r to restart the list values
                lst = generate_list(n, min_val, max_val)
                draw_information.set_lst(lst)

            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_generator = sorting_algo(draw_information, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            # if event.key == pygame.K_b:
            #     bubble_sort(draw_information)

    pygame.quit()

# O(n^2)
def bubble_sort(draw_info: DrawInformation, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        swapped = False
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j] # swap num1 and num2
                swapped = True
                draw_lst(draw_info, color_positions={j: draw_info.GREEN, j+1: draw_info.RED}, clear_bg=True)
                yield True # return to the main event so the swap can be visualized
        if not swapped: # no more swapping needed, list is ordered
            return lst


if __name__ == "__main__":
    main()