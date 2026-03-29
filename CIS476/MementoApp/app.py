from flask import Flask, render_template, request
from tactics import TeamTactics, TacticsHistory

app = Flask(__name__)

team = TeamTactics()
history = TacticsHistory()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]

        if action == "save":
            history.save(team.save())

        elif action == "set":
            history.save(team.save())
            formation = request.form["formation"]
            style = request.form["style"]
            team.set_tactics(formation, style)

        elif action == "undo":
            memento = history.undo()
            if memento:
                team.restore(memento)

    return render_template(
        "index.html",
        formation=team.formation,
        style=team.style,
        history=len(history.history)
    )

if __name__ == "__main__":
    app.run(debug=True)