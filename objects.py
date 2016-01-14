from kivy.uix.image import Image
from constants import CHAR_SPEED_X, CHAR_SPEED_Y, CHAR_DEACCELERATION
from tile import Tile

"""
A simple addition of default sprite size to the kivy image class
"""
class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

"""
Character is a class primarily a parent class for Player, but also other movable objects will
inherit from this class since all the update code for mevement between tiles is prewritten here.
Only the move function will have to be rewritten for it to work

If multiple instances of a class inheriting from character appear in the application,
the child class will most likely have a Class.List containing all the objects
"""
class Character(Sprite):
    def __init__(self, tile, source, game):
        super(Character, self).__init__(source=source, pos=(Tile.get_tile(tile).x, Tile.get_tile(tile).y))
        self.speed_x, self.speed_y = CHAR_SPEED_X, CHAR_SPEED_Y
        self.deacc = CHAR_DEACCELERATION
        self.velocity_x = 0
        self.velocity_y = 0
        self.tile = tile
        self.game = game
        self.moving = False

        self.game.add_widget(self)

    def update(self):
        if abs(self.velocity_y) >= self.deacc:
            self.velocity_y += self.deacc if self.velocity_y < 0 else -self.deacc

        elif abs(self.velocity_x) >= self.deacc:
            self.velocity_x += self.deacc if self.velocity_x < 0 else -self.deacc

        else:
            self.stop()
            self.move_to_tile(self.tile)

        self.y += self.velocity_y
        self.x += self.velocity_x

    def move_to_tile(self, tilenum):
        tile = Tile.get_tile(tilenum)
        self.x, self.y = tile.x, tile.y

    def stop(self):
        self.velocity_x, self.velocity_y = 0, 0
        self.moving = False

class Player(Character):
    def __init__(self, tile, game):
        source = 'img/character6.png'
        super(Player, self).__init__(tile, source, game)

    def move(self, angle):
        if not self.moving:

            self.moving = True

            if angle > 45 and angle < 135:
                direction = 12
                speed = self.speed_y
                tile_difference = Tile.V
            elif angle > 135 and angle < 225:
                direction = 9
                speed = -self.speed_x
                tile_difference = -Tile.H
            elif angle > 225 and angle < 315:
                direction = 6
                speed = -self.speed_y
                tile_difference = -Tile.V
            elif angle < 360:
                direction = 3
                speed = self.speed_x
                tile_difference = Tile.H
            else:
                raise ValueError("Incorrect angle in Player.move()")

            self.change_sprite(direction)
            target_tile = Tile.get_tile(self.tile + tile_difference)

            if target_tile.walkable:
                for box in self.game.boxes:
                    if box.tile == target_tile.number:
                        if box.move(direction):
                            if direction in (6, 12): self.velocity_y = speed
                            else: self.velocity_x = speed
                            self.tile += tile_difference
                        return

                if direction in (6, 12): self.velocity_y = speed
                else: self.velocity_x = speed
                self.tile += tile_difference
                return

    def change_sprite(self, direction):
        self.source = 'img/character{}.png'.format(direction)
        self.reload()

class Box(Character):

    List = []

    def __init__(self, tile, game):
        source = 'img/box.png'
        super(Box, self).__init__(tile, source, game)
        Box.List.append(self)

    def move(self, direction):

        if direction == 12:
            tile_difference = Tile.V
            speed = self.speed_y
        elif direction == 3:
            tile_difference = Tile.H
            speed = self.speed_x
        elif direction == 6:
            tile_difference = -Tile.V
            speed = -self.speed_y
        elif direction == 9:
            tile_difference = -Tile.H
            speed = -self.speed_x
        else:
            raise ValueError("Incorrect direction in Box.move()")

        target_tile = Tile.get_tile(self.tile + tile_difference)

        if target_tile.walkable:

            for box in self.game.boxes:
                if box.tile == self.tile + tile_difference:
                    return False

            if direction in (6, 12): self.velocity_y = speed
            if direction in (9, 3): self.velocity_x = speed

            self.tile += tile_difference
            return True

        return False
