class WumpusAgent:
    def __init__(self, r, c):
        self.pos = [r-1, 0]
        self.visited = set()
        self.safe = set()
        self.kb = set()

    def kb_size(self):
        return len(self.kb)

    def step(self, percept, world):
        r, c = self.pos
        self.visited.add((r,c))
        self.safe.add((r,c))

        self.kb.add(f"S_{r}_{c}" if percept["stench"] else f"¬S_{r}_{c}")
        self.kb.add(f"B_{r}_{c}" if percept["breeze"] else f"¬B_{r}_{c}")

        if percept["glitter"]:
            return {"action":"GRAB","status":"WIN"}

        # SAFE MOVEMENT LOGIC (AI DECISION)
        if c+1 < world.c:
            self.pos = [r, c+1]
        elif r-1 >= 0:
            self.pos = [r-1, c]

        return {"action":"MOVE","status":"RUNNING"}