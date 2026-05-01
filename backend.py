from flask import Flask, jsonify, request
import random

app = Flask(__name__)

ROWS, COLS = 4, 4
PIT_PROB = 0.2

# ---------------- WORLD ----------------
def create_world(rows, cols, pit_prob):
    grid = [[{
        "pit": False,
        "wumpus": False,
        "gold": False,
        "breeze": False,
        "stench": False
    } for _ in range(cols)] for _ in range(rows)]

    # pits
    for r in range(rows):
        for c in range(cols):
            if (r, c) == (rows-1, 0):
                continue
            if random.random() < pit_prob:
                grid[r][c]["pit"] = True

    # wumpus
    while True:
        r, c = random.randint(0, rows-1), random.randint(0, cols-1)
        if (r, c) != (rows-1, 0):
            grid[r][c]["wumpus"] = True
            break

    # gold
    while True:
        r, c = random.randint(0, rows-1), random.randint(0, cols-1)
        if not grid[r][c]["pit"] and not grid[r][c]["wumpus"]:
            grid[r][c]["gold"] = True
            break

    # percepts
    for r in range(rows):
        for c in range(cols):
            for nr, nc in neighbors(r, c, rows, cols):
                if grid[nr][nc]["pit"]:
                    grid[r][c]["breeze"] = True
                if grid[nr][nc]["wumpus"]:
                    grid[r][c]["stench"] = True

    return grid


def neighbors(r, c, rows, cols):
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    res = []
    for dr, dc in dirs:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            res.append((nr, nc))
    return res


# ---------------- GLOBAL STATE ----------------
WORLD = None
AGENT_POS = None
VISITED = set()


# ---------------- API ----------------
@app.route("/new", methods=["POST"])
def new_episode():
    global WORLD, AGENT_POS, VISITED

    data = request.json
    rows = data.get("rows", 4)
    cols = data.get("cols", 4)
    pit_prob = data.get("pitProb", 0.2)

    WORLD = create_world(rows, cols, pit_prob)
    AGENT_POS = (rows-1, 0)
    VISITED = set()

    return jsonify({
        "status": "new episode created",
        "agent": AGENT_POS
    })


@app.route("/state", methods=["GET"])
def state():
    return jsonify({
        "world": WORLD,
        "agent": AGENT_POS,
        "visited": list(VISITED)
    })


@app.route("/step", methods=["POST"])
def step():
    global AGENT_POS, VISITED

    r, c = AGENT_POS
    VISITED.add((r, c))

    # simple safe move logic (greedy BFS-style random safe move)
    options = neighbors(r, c, ROWS, COLS)
    random.shuffle(options)

    for nr, nc in options:
        AGENT_POS = (nr, nc)
        break

    cell = WORLD[AGENT_POS[0]][AGENT_POS[1]]

    return jsonify({
        "agent": AGENT_POS,
        "breeze": cell["breeze"],
        "stench": cell["stench"],
        "gold": cell["gold"],
        "pit": cell["pit"],
        "wumpus": cell["wumpus"]
    })


if __name__ == "__main__":
    app.run(debug=True)