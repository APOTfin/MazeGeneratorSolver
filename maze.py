import random
import pygame as pg

size = 100
res = 400
tilesize = res / size
halftile = tilesize / 2
size += 1
poles = [[1 for y in range(size * 2)] for x in range(size * 2)]
poles[1][1] = 0
done = [[0 for y in range(size)] for x in range(size)]
done[0][0] = 2
updaterects = []

class Path:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self):
        # Checks for possible directions to move in and chooses the most appealing one.
        possible = [0, 0, 0, 0]
        if self.x >= 2:
            if done[int(self.x / 2) - 1][int(self.y / 2)] == 0:
                possible[0] = 2
            elif poles[self.x][self.y + 1] == 0 and done[int(self.x / 2) - 1][int(self.y / 2)] != 2:
                possible[0] = 1
        if self.x < size * 2 - 4:
            if done[int(self.x / 2) + 1][int(self.y / 2)] == 0:
                possible[1] = 2
            elif poles[self.x + 2][self.y + 1] == 0 and done[int(self.x / 2) + 1][int(self.y / 2)] != 2:
                possible[1] = 1
        if self.y >= 2:
            if done[int(self.x / 2)][int(self.y / 2) - 1] == 0:
                possible[2] = 2
            elif poles[self.x + 1][self.y] == 0 and done[int(self.x / 2)][int(self.y / 2) - 1] != 2:
                possible[2] = 1
        if self.y < size * 2 - 4:
            if done[int(self.x / 2)][int(self.y / 2) + 1] == 0:
                possible[3] = 2
            elif poles[self.x + 1][self.y + 2] == 0 and done[int(self.x / 2)][int(self.y / 2) + 1] != 2:
                possible[3] = 1
        if max(possible) == 0:
            return True
        best = []
        for i, option in enumerate(possible):
            if option == max(possible):
                best.append(i)
        direction = random.choice(best)
        self.x += -(direction == 0) + (direction == 1)
        self.y += -(direction == 2) + (direction == 3)
        poles[self.x + 1][self.y + 1] = 0
        self.x += -(direction == 0) + (direction == 1)
        self.y += -(direction == 2) + (direction == 3)
        poles[self.x + 1][self.y + 1] = 0
        done[int(self.x / 2)][int(self.y / 2)] = 1

        # Checks if any neighboring tiles are dead ends, and updates the done -array accordingly.
        neighbors = []
        if self.x > 0:
            neighbors.append((int(self.x / 2 - 1), int(self.y / 2)))
        if self.x < size * 2 - 3:
            neighbors.append((int(self.x / 2 + 1), int(self.y / 2)))
        if self.y > 0:
            neighbors.append((int(self.x / 2), int(self.y / 2 - 1)))
        if self.y < size * 2 - 3:
            neighbors.append((int(self.x / 2), int(self.y / 2 + 1)))
        for tile in neighbors:
            x = tile[0]
            y = tile[1]
            if done[x][y] == 1:
                blocked = 0
                if x == 0:
                    blocked += 1
                elif done[x - 1][y] + poles[x * 2][y * 2 + 1] >= 2:
                    blocked += 1
                if x == size - 2:
                    blocked += 1
                elif done[x + 1][y] + poles[x * 2 + 2][y * 2 + 1] >= 2:
                    blocked += 1
                if y == 0:
                    blocked += 1
                elif done[x][y - 1] + poles[x * 2 + 1][y * 2] >= 2:
                    blocked += 1
                if y == size - 2:
                    blocked += 1
                elif done[x][y + 1] + poles[x * 2 + 1][y * 2 + 2] >= 2:
                    blocked += 1
                if blocked >= 3:
                    done[x][y] = 2

def magnifier(pos):
    if size > res / 10:
        x, y = pos
        zoomed = pg.Surface((8 * tilesize, 8 * tilesize))
        zoomed.blit(window, (-x + 4 * tilesize, -y + 4 * tilesize))
        zoomed = pg.transform.scale(zoomed, (int(res / 4), int(res / 4)))
        window.blit(zoomed, (x - int(res / 8), y - int(res / 8)))

def createMaze():
    # Creates a random new maze and draws it to the screen.
    path = Path()
    ready = False
    while not ready:
        if pg.event.get() != []:
            pg.quit()
            break
        ready = path.update()
        left = int(path.x / 2) - (path.x != 0)
        right = int(path.x / 2) + (path.x != size * 2 - 4)
        top = int(path.y / 2) - (path.y != 0)
        bottom = int(path.y / 2) + (path.y != size * 2 - 4)
        for x in range(left, right + 1):
            for y in range(top, bottom + 1):
                state = done[x][y]
                if state != 0:
                    color = (125 * state, 125 * state, 125 * state)
                    rect = window.fill(color, (x * tilesize, y * tilesize, tilesize, tilesize))
                    updaterects.append(rect)
        pg.display.update(updaterects)
        updaterects.clear()
    window.fill((0, 0, 0))
    for x in range(1, size * 2 - 1):
        for y in range(1, size * 2 - 1):
            if poles[x][y] == 0:
                rect = ((x - 0.5) * halftile, (y - 0.5) * halftile, halftile, halftile)
                window.fill((255, 255, 255), rect)
    pg.display.update()

def solve(startpoint, endpoint):
    # Solves the maze by filling in all dead ends, leaving only the correct route.
    solved = poles.copy()
    unsolved = []
    ends = []
    for x in range(1, size * 2 - 1):
        for y in range(1, size * 2 - 1):
            if solved[x][y] == 0:
                unsolved.append((x, y))
    for tile in unsolved:
        x, y = tile[0], tile[1]
        blocked = 0
        blocked += solved[x - 1][y]
        blocked += solved[x + 1][y]
        blocked += solved[x][y - 1]
        blocked += solved[x][y + 1]
        if blocked >= 3:
            ends.append((x, y))
    while True:
        newends = []
        for tile in ends:
            if pg.event.get() != []:
                pg.quit()
                break
            if tile not in [startpoint, endpoint]:
                x, y = tile[0], tile[1]
                solved[x][y] = 1
                neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for other in neighbors:
                    if solved[other[0]][other[1]] == 0:
                        x, y = other[0], other[1]
                        blocked = 0
                        blocked += solved[x - 1][y]
                        blocked += solved[x + 1][y]
                        blocked += solved[x][y - 1]
                        blocked += solved[x][y + 1]
                        if blocked >= 3:
                            if other not in newends:
                                newends.append(other)
        ends = newends.copy()
        if ends == []:
            for x in range(1, size * 2 - 1):
                for y in range(1, size * 2 - 1):
                    if solved[x][y] == 0:
                        updaterects.append(window.fill((255, 0, 0), (x * halftile - halftile / 2, y * halftile - halftile / 2, halftile, halftile)))
            pg.display.update(updaterects)
            break

if __name__ == "__main__":
    pg.init()
    pg.event.set_blocked(None)
    pg.event.set_allowed(pg.QUIT)
    window = pg.display.set_mode((res, res))
    createMaze()
    bg = pg.Surface((res, res))
    bg.blit(window, (0, 0))
    pg.event.set_allowed((pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION))
    point1, point2 = None, None
    while point2 == None:
        mousepos = int(pg.mouse.get_pos()[0] / halftile + 0.5), int(pg.mouse.get_pos()[1] / halftile + 0.5)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                if poles[mousepos[0]][mousepos[1]] == 0:
                    if point1 == None:
                        point1 = mousepos
                    else:
                        point2 = mousepos
            elif event.type == pg.MOUSEMOTION:
                window.blit(bg, (0, 0))
                if poles[mousepos[0]][mousepos[1]] == 0:
                    window.fill((255, 0, 0), ((mousepos[0] - 0.5) * halftile, (mousepos[1] - 0.5) * halftile, halftile, halftile))
                if point1 != None:
                    window.fill((255, 0, 0), ((point1[0] - 0.5) * halftile, (point1[1] - 0.5) * halftile, halftile, halftile))
                if point2 != None:
                    window.fill((255, 0, 0), ((point2[0] - 0.5) * halftile, (point2[1] - 0.5) * halftile, halftile, halftile))
                magnifier(pg.mouse.get_pos())
                pg.display.update()
    window.blit(bg, (0, 0))
    window.fill((255, 0, 0), ((point1[0] - 0.5) * halftile, (point1[1] - 0.5) * halftile, halftile, halftile))
    window.fill((255, 0, 0), ((point2[0] - 0.5) * halftile, (point2[1] - 0.5) * halftile, halftile, halftile))
    pg.event.set_blocked((pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION))
    solve(point1, point2)
    bg.blit(window, (0,0))
    pg.event.set_allowed(pg.MOUSEMOTION)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False
            elif event.type == pg.MOUSEMOTION:
                window.blit(bg, (0, 0))
                magnifier(pg.mouse.get_pos())
                pg.display.update()
