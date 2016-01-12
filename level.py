

class Level():
    @staticmethod
    def load_level(level):
        if level == 1337:
            return Level(1, [68, 69, 70, 79, 80, 81, 83, 84, 85, 90, 91, 92, 94, 95, 96, 103, 104, 105, 106, 107, 113, 114, 115, 124, 125, 126, 127, 128], [126, 127, 128], [80, 95, 103], 113)
        #open csv file and initiate an instance of the Level class

    def __init__(self, level, normal, blockpoints, boxspawn, playerspawn):
        self.normal = normal
        self.level = level
        self.blockpoints = blockpoints
        self.boxspawn = boxspawn
        self.playerspawn = playerspawn
