import pygame 
from pygame import mixer
import time


pygame.init()

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Game of life")
font = pygame.font.Font('freesansbold.ttf', 62)

textX = 10
textY = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165 ,0)

def show_score(score,x,y):
    cells = font.render("cells alive", True, (0,255,0)) 
    WIN.blit(cells, (x,y))
    print("shown on screen")
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.age = 0

    def get_pos(self):
        return self.row, self.col

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def make_alive(self):
        self.color = BLACK
    
    def make_dead(self):
        self.color = WHITE
        self.age = 0
    
    def age_cell(self):
        self.age += 1
        if self.age > 3:
            self.color = RED
        if self.age == 3:
            self.color = ORANGE
        if self.age == 2:
            self.color = YELLOW

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.row + 1][self.col]) # down
        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col]) # up
        if self.col < self.total_rows - 1:
            self.neighbors.append(grid[self.row][self.col + 1]) # right
        if self.col > 0:
            self.neighbors.append(grid[self.row][self.col - 1]) # left
        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1:
            self.neighbors.append(grid[self.row + 1][self.col + 1]) # below and right
        if self.row < self.total_rows - 1 and self.col > 0:
            self.neighbors.append(grid[self.row + 1][self.col - 1]) # bottom left
        if self.row > 0 and self.col < self.total_rows - 1:
            self.neighbors.append(grid[self.row - 1][self.col + 1]) #top right
        if self.row > 0 and self.col > 0:
            self.neighbors.append(grid[self.row - 1][self.col - 1]) #top left
        
    



def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

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
    ROWS = 10
    grid = make_grid(ROWS, width)

    # for row in grid:
    #     for spot in row:
    #         spot.update_neighbors(grid)
    #         print(f"postion: {spot.get_pos()}")
    #         for n in spot.neighbors:
    #             print(n.get_pos())

    run = True
    Alive_Cells = 0
    Population_over_time= []
    Time_taken_per_Step = []
    steps = 0
    while run:
        draw(win, grid, ROWS, width)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.make_alive()
                spot.age_cell()
                Alive_Cells += 1
                show_score(Alive_Cells, 10, 10)

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.make_dead()
                Alive_Cells -= 1
                show_score(Alive_Cells)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = time.time()
                    To_Kill = []
                    To_Revive = []
                    To_Keep_alive = []
                    To_Keep_Dead = []
                    

                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid) 
                            # print(f"postion: {spot.get_pos()}")
                            # if spot.color == (0,0,0):
                            #     print("Alive")
                            # else:
                            #     print("Dead")


                            Live_neighbors= 0
                            for n in spot.neighbors:
                                if n.color == (0,0,0) or n.color == RED or n.color == YELLOW or n.color == ORANGE:
                                   Live_neighbors += 1
                                # if spot.get_pos() == (1,0):
                                #     print(f"{n.get_pos()} {n.color} ")
                            
                            if spot.color == (255,255,255):
                                if Live_neighbors == 3:     #rule 4
                                    # print(f"reviving {spot.get_pos()}")
                                    To_Revive.append(spot.get_pos())
                                else:
                                    # print(f"has {Live_neighbors}")
                                    # print(f"keeping dead")
                                    To_Keep_Dead.append(spot.get_pos())

                            else:
                                if Live_neighbors < 2 or Live_neighbors >= 4: #rule 1 and 3
                                    # print(f"killing cell {spot.get_pos()}")
                                    To_Kill.append(spot.get_pos())

                                elif Live_neighbors >= 2 and Live_neighbors < 4: #rule 2
                                    # print(f"{spot.get_pos()} is alive")

                                    To_Keep_alive.append(spot.get_pos())


                    # print(To_Keep_Dead)
                    # print(To_Keep_alive)
                    # print(To_Kill)
                    # print(To_Revive)
                    print(f"cells  alive before process = {Alive_Cells}")
                    for row in grid:
                        for spot in row:
                            if spot.get_pos() in To_Revive:
                                spot.make_alive()
                                spot.age_cell()
                                Alive_Cells += 1
                            elif spot.get_pos() in To_Kill:
                                spot.make_dead()
                                Alive_Cells -= 1 
                            elif spot.get_pos() in To_Keep_alive:
                                spot.age_cell()
                                print(spot.get_pos(), spot.age)
                            elif spot.get_pos() in To_Keep_Dead:
                                pass
                    Population_over_time.append(Alive_Cells)
                    print(f"cells  alive = {Alive_Cells}")
                    end = time.time()
                    steps += 1
                    Time_taken_per_Step.append(end-start)
                    print(end - start)

                    if Alive_Cells == 0:
                        run = False
                        print(f"steps: {steps}")
                        print(f"Population over time: {Population_over_time}")
                        total=0
                        for t in Time_taken_per_Step:
                            total += t
                        print(f"average time taken per step: {total/steps}s")
                            


                        



                    
                            


main(WIN, WIDTH)
