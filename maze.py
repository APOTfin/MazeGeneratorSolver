import random
import pygame as pg

size = 100
res = 800
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
        direction = best[0]
        if len(best) > 1:
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
                elif done[x - 1][y] == 2:
                    blocked += 1
                elif done[x - 1][y] == 1 and poles[x * 2][y * 2 + 1] == 1:
                    blocked += 1
                if x == size - 2:
                    blocked += 1
                elif done[x + 1][y] == 2:
                    blocked += 1
                elif done[x + 1][y] == 1 and poles[x * 2 + 2][y * 2 + 1] == 1:
                    blocked += 1
                if y == 0:
                    blocked += 1
                elif done[x][y - 1] == 2:
                    blocked += 1
                elif done[x][y - 1] == 1 and poles[x * 2 + 1][y * 2] == 1:
                    blocked += 1
                if y == size - 2:
                    blocked += 1
                elif done[x][y + 1] == 2:
                    blocked += 1
                elif done[x][y + 1] == 1 and poles[x * 2 + 1][y * 2 + 2] == 1:
                    blocked += 1
                if blocked >= 3:
                    done[x][y] = 2

def createMaze():
    # Creates a random new maze and draws it to the screen.
    path = Path()
    ready = False
    while not ready:
        if len(pg.event.get()) != 0:
            pg.quit()
            exit()
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
                    updaterects.append(window.fill(color, (x * tilesize, y * tilesize, tilesize, tilesize)))
        pg.display.update(updaterects)
        updaterects.clear()
    window.fill((0, 0, 0))
    for x in range(1, size * 2 - 1):
        for y in range(1, size * 2 - 1):
            if poles[x][y] == 0:
                window.fill((255, 255, 255), ((x - 0.5) * halftile, (y - 0.5) * halftile, halftile, halftile))
    pg.display.update()

def solve():
    # Solves the maze by filling in all dead ends, leaving only the correct route.
    solved = poles.copy()
    unsolved = []
    for x in range(1, size * 2 - 1):
        for y in range(1, size * 2 - 1):
            if solved[x][y] == 0 and (x, y) != (1, 1) and (x, y) != (size * 2 - 3, size * 2 - 3):
                unsolved.append((x, y))
    while True:
        if len(pg.event.get()) != 0:
            pg.quit()
            exit()
        finished = True
        removed = []
        for tile in unsolved:
            x, y = tile[0], tile[1]
            blocked = 0
            blocked += solved[x - 1][y]
            blocked += solved[x + 1][y]
            blocked += solved[x][y - 1]
            blocked += solved[x][y + 1]
            if blocked >= 3:
                removed.append(tile)
                solved[x][y] = 1
                updaterects.append(window.fill((50, 50, 50), ((x - 0.5) * halftile, (y - 0.5) * halftile, halftile, halftile)))
                finished = False
        pg.display.update(updaterects)
        updaterects.clear()
        for tile in removed:
            unsolved.remove(tile)
        removed.clear()
        if finished:
            break

if __name__ == "__main__":
    pg.init()
    pg.event.set_blocked(None)
    pg.event.set_allowed(pg.QUIT)
    window = pg.display.set_mode(((int((size - 1) * tilesize)), int(((size - 1) * tilesize))))
    createMaze()
    solve()
    while True:
        if len(pg.event.get()) != 0:
            pg.quit()
            exit()
