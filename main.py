import pygame
import random
import keyboard

# Constants
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
UNVISITED_COLOR = (50, 135, 168) #light blue
VISITED_COLOR = (219, 135, 57) #orange
BACKTRACKED_COLOR = (240, 224, 223) # skin colour
CURRENT_COLOR = (247, 227, 126) #yellowish
OPEN_COLOR = (29, 219, 118) #light green
CLOSED_COLOR = (222, 65, 55) #RED
PATH_COLOR = (83, 169, 219) # lighter blue?


# Initialize Pygame
pygame.init()

# Cell size and maze size
CELL_SIZE = 40
WIDTH, HEIGHT = 45, 20
WINDOW_SIZE = (CELL_SIZE * WIDTH, CELL_SIZE * HEIGHT)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze")



class Cell:
    def __init__(self,x, y):
        #1 means border, 0 means no border
        self.borders = [1, 1, 1, 1] # UP, RIGHT, DOWN, LEFT (Clockwise)
        self.visited = False
        self.backtracked = False
        self.current = False
        self.checkedForNeighbours = False
        self.x = x
        self.y = y
        self.gcost = -1 #distance from start
        self.hcost = -1 #distance from end
        self.fcost = -1 #g + h
        self.parent = None
        self.open = False
        self.closed = False
        self.start = False
        self.target = False
        self.path = False


# Define a custom key function to find the minimum based on fcost and hcost
def custom_key(cell):
    return (cell.fcost, cell.hcost, random.random())


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[Cell(x, y) for x in range(width)] for y in range(height)]

    def get_neighbours(self, cell, borders=False):
        x = cell.x
        y = cell.y
        neighbours = []
        # Check UP neighbor
        if y > 0:
            if not (borders and cell.borders[UP]):
                neighbours.append(self.maze[y - 1][x])
            #neighbours.append((x, y - 1))
        #else:
        #    neighbours.append((-1, -1))  # No UP neighbor

        # Check RIGHT neighbor
        if x < self.width - 1:
            if not (borders and cell.borders[RIGHT]):
                neighbours.append(self.maze[y][x + 1])
            #neighbours.append((x + 1, y))
        #else:
        #    neighbours.append((-1, -1))  # No RIGHT neighbor

        # Check DOWN neighbor
        if y < self.height - 1:
            if not (borders and cell.borders[DOWN]):
                neighbours.append(self.maze[y + 1][x])
            #neighbours.append((x, y + 1))
        #else:
        #    neighbours.append((-1, -1))  # No DOWN neighbor

        # Check LEFT neighbor
        if x > 0:
            if not (borders and cell.borders[LEFT]):
                neighbours.append(self.maze[y][x - 1])
            #neighbours.append((x - 1, y))
        #else:
        #    neighbours.append((-1, -1))  # No LEFT neighbor

        return neighbours
    

    def generate_maze(self):
        enter_pressed = False
        cell_stack = []
        cell_stack.append(self.maze[0][0])
        self.maze[0][0].visited = True
        self.maze[0][0].vistamount = 1
        clock = pygame.time.Clock()  # Create a Pygame clock object
        while cell_stack:
            changeVisit = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            #print("###")
            current_cell = cell_stack.pop()
            current_cell.current = True
            if current_cell.checkedForNeighbours:
                current_cell.backtracked = True
            #print(f"Current: x: {current_cell.x}, y: {current_cell.y}")
            neighbours = self.get_neighbours(current_cell)
            #print("Neighbours: ")
            unvisited_neighbours = []
            for neighbour_cell in neighbours:
                current_cell.checkedForNeighbours = True
                #print(f"x: {neighbour_cell.x}, y: {neighbour_cell.y}")
                if not neighbour_cell.visited:
                    unvisited_neighbours.append(neighbour_cell)
            if unvisited_neighbours:
                cell_stack.append(current_cell)
                random_neighbour = random.choice(unvisited_neighbours)
                #print(f"Random: x: {random_neighbour.x}, y: {random_neighbour.y}")
                #remove wall between random neighbour and current cell
                if random_neighbour.y > current_cell.y:
                    random_neighbour.borders[UP] = 0
                    current_cell.borders[DOWN] = 0
                elif random_neighbour.y < current_cell.y:
                    random_neighbour.borders[DOWN] = 0
                    current_cell.borders[UP] = 0
                elif random_neighbour.x > current_cell.x:
                    random_neighbour.borders[LEFT] = 0
                    current_cell.borders[RIGHT] = 0
                elif random_neighbour.x < current_cell.x:
                    random_neighbour.borders[RIGHT] = 0
                    current_cell.borders[LEFT] = 0
                changeVisit = True
                #random_neighbour.visited = True
                cell_stack.append(random_neighbour)
            else:
                current_cell.backtracked = True

            # Redraw the maze and wait for a delay
            # Clear the screen
            WINDOW.fill(WHITE)
            self.draw()
            pygame.display.flip()
            clock.tick(150)
            current_cell.current = False
            if changeVisit:
                random_neighbour.visited = True
            while not enter_pressed:
                if keyboard.is_pressed("enter"):
                    enter_pressed = True
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                


    def solve(self):
        open = [] # cells to be evaluated (GREEN)
        closed = [] # cells that have been evaluated (RED)
        start = self.maze[0][0]
        start.start = True
        open.append(start) # start cell
        target = self.maze[self.height - 1][self.width - 1]
        target.target = True
        start.gcost = 0
        start.hcost = 10 * (abs(target.x - start.x) + abs(target.y - start.y))
        start.fcost = start.gcost + start.hcost
        clock = pygame.time.Clock()
        i = 0
        while True:
            clock.tick(25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current = min(open, key=custom_key)
            open.remove(current)
            closed.append(current)
            current.closed = True
            if current == target:
                parent = current.parent
                while parent:
                    parent.path = True
                    parent = parent.parent
                    WINDOW.fill(WHITE)
                    self.draw()
                    pygame.display.flip()
                return
            neighbours = self.get_neighbours(current, True)
            for neighbour in neighbours:
                if neighbour in closed:
                    continue
                tmphcost = 10 * (abs(target.x - neighbour.x) + abs(target.y - neighbour.y))
                tmpgcost = current.gcost + 10
                tmpfcost = tmphcost + tmpgcost
                if neighbour not in open or tmpfcost < neighbour.fcost:
                    neighbour.hcost = tmphcost
                    neighbour.gcost = tmpgcost
                    neighbour.fcost = tmpfcost
                    neighbour.parent = current
                    if neighbour not in open:
                        open.append(neighbour)
                        neighbour.open = True
            WINDOW.fill(WHITE)
            self.draw()
            pygame.display.flip()



    def draw(self):
        for row in self.maze:
            for cell in row:
                x = cell.x
                y = cell.y
                x_pos = x * CELL_SIZE
                y_pos = y * CELL_SIZE

                if cell.start or cell.target:
                    CELL_COLOR = UNVISITED_COLOR
                elif cell.path:
                    CELL_COLOR = PATH_COLOR
                elif cell.closed:
                    CELL_COLOR = CLOSED_COLOR
                elif cell.open:
                    CELL_COLOR = OPEN_COLOR
                elif cell.current:
                    CELL_COLOR = CURRENT_COLOR
                elif cell.backtracked:
                    CELL_COLOR = BACKTRACKED_COLOR
                elif cell.visited:
                    CELL_COLOR = VISITED_COLOR
                else:
                    CELL_COLOR = UNVISITED_COLOR
                # Draw a light blue square for each cell
                pygame.draw.rect(WINDOW, CELL_COLOR, (x_pos, y_pos, CELL_SIZE, CELL_SIZE))
                line_thickness = 5
                # Draw borders based on self.borders
                if cell.borders[UP]:
                    pygame.draw.line(WINDOW, BLACK, (x_pos, y_pos), (x_pos + CELL_SIZE, y_pos), line_thickness)
                if cell.borders[RIGHT]:
                    pygame.draw.line(WINDOW, BLACK, (x_pos + CELL_SIZE, y_pos), (x_pos + CELL_SIZE, y_pos + CELL_SIZE), line_thickness)
                if cell.borders[DOWN]:
                    pygame.draw.line(WINDOW, BLACK, (x_pos, y_pos + CELL_SIZE), (x_pos + CELL_SIZE, y_pos + CELL_SIZE), line_thickness)
                if cell.borders[LEFT]:
                    pygame.draw.line(WINDOW, BLACK, (x_pos, y_pos), (x_pos, y_pos + CELL_SIZE), line_thickness)
                # Render the fcost value as text
                #fcost_text = font.render(str(cell.fcost), True, BLACK)

                # Get the text rect and position it inside the square
                #text_rect = fcost_text.get_rect()
                #text_rect.center = (x_pos + CELL_SIZE // 2, y_pos + CELL_SIZE // 2)

                # Draw the text on the window
                #WINDOW.blit(fcost_text, text_rect)



if __name__ == "__main__":
    pygame.init()
    # Create a Pygame font object
    font = pygame.font.Font(None, 36)  # You can adjust the font size as needed
    # Define the codec and create a VideoWriter object
    maze = Maze(WIDTH, HEIGHT)
    # Capture the screen and add it to the video
    running = True
    for row in maze.maze:
        for cell in row:
            print(f"x: {cell.x}, y: {cell.y}", end = " ")
        print()

    maze.generate_maze()
    maze.solve()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()