class MathProb:
    INSTRUCTIONS = "set this to default description in children"
    TITLE = "set this to default title in children"

    def __init__(self):
        pass

    def make(self):
        raise NotImplementedError("function make is not implemented!")

    def from_json(self):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError

