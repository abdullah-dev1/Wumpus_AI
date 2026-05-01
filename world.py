import random

class World:
    def __init__(self, r, c, p):
        self.r = r
        self.c = c
        self.grid = [[{"pit": False, "wumpus": False, "gold": False} for _ in range(c)] for _ in range(r)]
        self.generate(p)

    def generate(self, p):
        for i in range(self.r):
            for j in range(self.c):
                if (i, j) != (self.r-1, 0):
                    if random.randint(1,100) < p:
                        self.grid[i][j]["pit"] = True

        wr, wc = random.randint(0,self.r-1), random.randint(0,self.c-1)
        self.grid[wr][wc]["wumpus"] = True

        while True:
            gr, gc = random.randint(0,self.r-1), random.randint(0,self.c-1)
            if not self.grid[gr][gc]["pit"] and not self.grid[gr][gc]["wumpus"]:
                self.grid[gr][gc]["gold"] = True
                break

    def neighbors(self, r, c):
        n = []
        if r>0: n.append((r-1,c))
        if r<self.r-1: n.append((r+1,c))
        if c>0: n.append((r,c-1))
        if c<self.c-1: n.append((r,c+1))
        return n

    def get_percept(self, r, c):
        cell = self.grid[r][c]

        breeze = any(self.grid[nr][nc]["pit"] for nr,nc in self.neighbors(r,c))
        stench = any(self.grid[nr][nc]["wumpus"] for nr,nc in self.neighbors(r,c))

        return {
            "breeze": breeze,
            "stench": stench,
            "glitter": cell["gold"]
        }

    def get_grid(self):
        return self.grid


def create_world(r,c,p):
    return World(r,c,p)