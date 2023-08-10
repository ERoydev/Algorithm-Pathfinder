import pygame
from pygame import *
from collections import deque
from queue import PriorityQueue
import config
from tkinter import *
from tkinter import messagebox
import time


Tk().wm_withdraw()
# Colors
WIDTH = 800
pygame.display.set_caption("Pathfinding Algorithm")
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
CYAN = (66, 245, 215)

# MAIN MENU - Text fonts and setups
screen = pygame.display.set_mode([700, 460])
pygame.init()
pygame.display.set_caption("Menu")
bg = pygame.image.load("abstract-art-atom-background.jpg")
clicked = False

font = pygame.font.SysFont('gabriola', 30)
font_introduction = pygame.font.SysFont("Arial", 20)
font_instructions = pygame.font.SysFont('verdana', 16)
text = font.render("Choose the algorithm that you want to explore :)", True, (50, 168, 149))
text_intro = font_introduction.render("Click to select Start and end points then create walls (optional).", True, (255, 255, 255))
text_instruction1 = font_instructions.render("After that click SPACE to start and press R to reset after.", True, (255, 255, 255))
text_instruction2 = font_instructions.render("Click Q to return to main menu.", True, (255, 255, 255))


class Button:
    button_col = (25, 190, 225)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = (255, 255, 255)
    width = 180
    height = 40

    def __init__(self, x ,y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):
        global clicked
        action = False

        pos = pygame.mouse.get_pos()

        #Create pygame rectangle for button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked condition
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)

            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True

            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)

        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # Add shading to button
        pygame.draw.line(screen, "white", (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, "white", (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, "black", (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, "black", (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # Add Text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 5))
        return action

#-------------------------
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == YELLOW

    def is_open(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == CYAN

    def is_end(self):
        return self.color == ORANGE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = CYAN

    def make_closed(self):
        self.color = YELLOW

    def make_open(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2): #manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def path_create(parent, current, draw):
    while current in parent:
        current = parent[current]
        current.make_path()
        draw()


def dijkstra(draw, source, destination, grid):
    pq = PriorityQueue()
    pq.put((0, source))

    parent = {}
    distance = {spot: float('inf') for row in grid for spot in row}
    distance[source] = 0
    counter = 0

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        min_distance, node = pq.get()

        if node == destination:
            path_create(parent, destination, draw)
            destination.make_end()
            source.make_start()
            break

        for child in node.neighbours:
            new_distance = min_distance + 1
            if new_distance < distance[child]:
                distance[child] = new_distance
                parent[child] = node
                pq.put((new_distance, child))
                child.make_open()
                counter += 1
                draw()

        if node != source:
            node.make_closed()

    return counter


def dfs(draw, grid, stack,start, destination, visited):
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        node = stack.pop()
        if node in visited:
            continue

        if node == grid[destination.row][destination.col]:
            break

        visited.add(node)
        node.make_open()
        draw()
        for child in node.neighbours:
            if child in visited:
                continue

            stack.append(child)

        if node != start:
            node.make_closed()


def bfs(draw, source, destination, grid):
    visited = set()
    queue = deque((source.row, source.col, source))

    while queue:
        current = queue.pop()
        if current in visited:
            continue

        if current == destination:
            destination.make_end()
            source.make_start()
            break

        visited.add(current)
        for child in current.neighbours:
            if child in visited:
                continue

            queue.append(child)
            draw()

        if current != source:
            current.make_closed()

    return visited


def a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    parent = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    counter = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path_create(parent, end, draw)
            end.make_end()
            start.make_start()
            return True, counter

        for child in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[child]:
                parent[child] = current
                g_score[child] = temp_g_score
                f_score[child] = temp_g_score + h(child.get_pos(), end.get_pos())
                counter += 1
                if child not in open_set_hash:
                    count += 1
                    open_set.put((f_score[child], count, child))
                    open_set_hash.add(child)
                    child.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # Left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()

                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    if config.x == "ASTAR":
                        counter = 0
                        start_time = time.time()
                        el = a_star_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        messagebox.showinfo('Complexity', f'Nodes Checked => {el[1]}\n Time => {time.time() - start_time:.2f} seconds.')

                    if config.x == "DFS":
                        visited = set()
                        stack = deque((start.row, start.col, start))
                        start_time = time.time()
                        dfs(lambda: draw(win, grid, ROWS, width), grid, stack,start, end, visited)
                        messagebox.showinfo('Complexity', f'Nodes Checked => {len(visited) - 1}\n Time => {time.time() - start_time:.2f} seconds.')

                    if config.x == "DIJKSTRA":
                        start_time = time.time()

                        count = dijkstra(lambda: draw(win, grid, ROWS, width), start, end, grid)
                        messagebox.showinfo("Complexity", f"Nodes Checked => {count}\n Time => {time.time() - start_time:.2f} seconds.")

                    if config.x == "BFS":
                        start_time = time.time()
                        count = bfs(lambda: draw(win, grid, ROWS, width), start, end, grid)
                        messagebox.showinfo("Complexity", f"Nodes Checked => {len(count)}\n Time => {time.time() - start_time:.2f} seconds.")

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_q:
                    screen = pygame.display.set_mode([700, 460])
                    menu(screen)

    pygame.quit()

#------------------------------------MAIN MENU---------------------------------------

def menu(screen):
    a_star = Button(100, 100, "A_Star")
    dijkstra_btn = Button(100, 180, "Dijkstra")
    dfs_btn = Button(100, 260, "DFS")
    bfs_btn = Button(100, 340, "BFS")

    running = True
    while running:
        screen.blit(bg, (0, 0))
        screen.blit(text,(20, 20))
        screen.blit(text_intro, (50, 50))
        screen.blit(text_instruction1, (20, 400))
        screen.blit(text_instruction2, (400, 430))

        if a_star.draw_button():
            config.x = "ASTAR"
            WIN = pygame.display.set_mode((WIDTH, WIDTH))
            main(WIN, WIDTH)

        if dijkstra_btn.draw_button():
            config.x = "DIJKSTRA"
            WIN = pygame.display.set_mode((WIDTH, WIDTH))
            main(WIN, WIDTH)

        if dfs_btn.draw_button():
            config.x = "DFS"
            WIN = pygame.display.set_mode((WIDTH, WIDTH))
            main(WIN, WIDTH)

        if bfs_btn.draw_button():
            config.x = "BFS"
            WIN = pygame.display.set_mode((WIDTH, WIDTH))
            main(WIN, WIDTH)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()

menu(screen)
