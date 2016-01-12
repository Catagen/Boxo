from main import Sprite

class Tile():

    List = []
    height, width = 35, 45
    H, V = 0, 0
    image_files = {'normal' : 'img/solid_block.png', 'normal_edge' : 'img/solid_block_edge.png', 'blockpoint' : 'img/point_block.png', 'blockpoint_edge' : 'img/point_block_edge.png'}

    @staticmethod
    def make_tiles(size, level):
        """
        Passing a game object for the game size (width height) reference
        Passing the level elements to initiate the tiles with right types
        """
        for y in range(0, size[1], Tile.height):
            for x in range(0, size[0], Tile.width):
                if len(Tile.List) in level.blockpoints:
                    Tile(x, y, 'blockpoint')
                elif len(Tile.List) in level.normal:
                    Tile(x, y, 'normal')
                else:
                    Tile(x, y, 'empty')

    def __init__(self, x, y, type_):
        self.type = type_
        self.number = len(Tile.List)
        self.x, self.y = x, y

        if type_ == 'empty':
            self.walkable = False
        else:
            self.walkable = True

        Tile.List.append(self)

    @staticmethod
    def get_tile(number):
        for tile in Tile.List:
            if tile.number == number:
                return tile
