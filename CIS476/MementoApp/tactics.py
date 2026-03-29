class TacticsMemento:
    def __init__(self, formation, style):
        self.formation = formation
        self.style = style


class TeamTactics:
    def __init__(self):
        self.formation = "4-4-2"
        self.style = "Balanced"

    def set_tactics(self, formation, style):
        self.formation = formation
        self.style = style

    def save(self):
        return TacticsMemento(self.formation, self.style)

    def restore(self, memento):
        self.formation = memento.formation
        self.style = memento.style


class TacticsHistory:
    def __init__(self):
        self.history = []

    def save(self, memento):
        self.history.append(memento)

    def undo(self):
        if self.history:
            return self.history.pop()
        return None