from flask import Flask, request, jsonify
from flask_cors import CORS
from world import World,create_world
from agent import WumpusAgent

app = Flask(__name__)
CORS(app)

world = None
agent = None


@app.route("/new_game", methods=["POST"])
def new_game():
    global world, agent

    data = request.json
    rows = data.get("rows", 8)
    cols = data.get("cols", 8)
    pit_prob = data.get("pit_prob", 15)

    world = create_world(rows, cols, pit_prob)
    agent = WumpusAgent(rows, cols)

    return jsonify({
        "grid": world.get_grid()
    })


@app.route("/step", methods=["POST"])
def step():
    global world, agent

    r, c = agent.pos
    percept = world.get_percept(r, c)

    result = agent.step(percept, world)

    return jsonify({
        "agent_pos": agent.pos,
        "action": result["action"],
        "status": result["status"],
        "visited": list(agent.visited),
        "safe": list(agent.safe),
        "kb_size": agent.kb_size()
    })


if __name__ == "__main__":
    app.run(debug=True)