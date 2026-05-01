class KnowledgeBase:
    def __init__(self):
        self.safe = set()
        self.unsafe = set()

    def mark_safe(self, cell):
        self.safe.add(cell)

    def mark_unsafe(self, cell):
        self.unsafe.add(cell)

    def is_safe(self, cell):
        return cell in self.safe and cell not in self.unsafe