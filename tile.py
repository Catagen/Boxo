
class Tile():

    #Contains all the tiles created (added in __init__())
    List = []
    #Height and width for now will also have to be changed in the image files
    height, width = 35, 45
    #The vertical and horizontal distance (in tiles) to the wanted tile
    H, V = 1, 11

    #Image sources to various tile types
    image_files = { 'normal' : 'img/solid_block.png',
                    'normal_edge' : 'img/solid_block_edge.png',
                    'blockpoint' : 'img/point_block.png',
                    'blockpoint_edge' : 'img/point_block_edge.png'}

    #Initialize the world by creating virtual tiles to cover the screen
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

    #Returns the tile object corresponding to a tile number
    @staticmethod
    def get_tile(number):
        for tile in Tile.List:
            if tile.number == number:
                return tile
