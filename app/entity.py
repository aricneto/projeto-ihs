class Entity():
    DEFAULT_ANIM = ["@", "O"]
    def __init__(self, x=0, y=0, rep=".", color=1) -> None:
        self.x = x
        self.y = y
        self.rep = rep
        self.color = color
        self.start_frame = 0
        pass

    def getChar(self):
        nextf = self.DEFAULT_ANIM[self.start_frame]
        self.start_frame = (self.start_frame + 1) % len(self.DEFAULT_ANIM)
        return nextf