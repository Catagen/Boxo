from csv import reader

class Level():

    @staticmethod
    def load_level(level):
        try:
            print('Loading level {}...'.format(level))
            filename = 'level/level{}.csv'.format(level)

            levelfile = open(filename)
            csv_levelfile = reader(levelfile)

            lvl = 0
            nrml = []
            blkp = []
            bxsp = []
            plsp = 0

            for i, row in enumerate(csv_levelfile):
                if i == 0:
                    lvl = int(row[0])
                elif i == 1:
                    for val in row:
                        nrml.append(int(val))
                elif i == 2:
                    for val in row:
                        blkp.append(int(val))
                elif i == 3:
                    for val in row:
                        bxsp.append(int(val))
                elif i == 4:
                    plsp = int(row[0])

            levelfile.close()

            return Level(lvl, nrml, blkp, bxsp, plsp)

        except Exception as e:
            print(e)

    def __init__(self, level, normal, blockpoints, boxspawn, playerspawn):
        self.normal = normal
        self.level = level
        self.blockpoints = blockpoints
        self.boxspawn = boxspawn
        self.playerspawn = playerspawn

if __name__ == '__main__':
    print(Level.load_level(1))
