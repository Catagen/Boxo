from kivy.uix.image import Image
from tile import Tile

"""
A simple addition of default sprite size to the kivy image class
"""
class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

"""
Character is a class primarily for the player, but also other movable objects will
inherit from this class since all the code for mevement between tiles is prewritten here.
Only the move function will have to be rewritten for it to work
"""
class Character(Sprite):
    def __init__(self, tile, source, game):
        super(Character, self).__init__(source=source, pos=(Tile.get_tile(tile).x, Tile.get_tile(tile).y))
        self.speed_x, self.speed_y = 3.8, 3.38
        self.deacc = 0.15
        self.velocity_x = 0
        self.velocity_y = 0
        self.tile = tile
        self.game = game
        self.moving = False

    def update(self):
        if self.velocity_y >= self.deacc or self.velocity_y <= -self.deacc:
            self.velocity_y += self.deacc if self.velocity_y < 0 else -self.deacc

        elif self.velocity_x >= self.deacc or self.velocity_x <= -self.deacc:
            self.velocity_x += self.deacc if self.velocity_x < 0 else -self.deacc

        else:
            self.stop()
            self.x, self.y = Tile.get_tile(self.tile).x, Tile.get_tile(self.tile).y

        self.y += self.velocity_y
        self.x += self.velocity_x

    def move(self, angle):
        if not self.moving:

            self.moving = True

            #Swipe UP
            if angle > 45 and angle < 135:

                self.change_sprite('back')

                target_tile = Tile.get_tile(self.tile + Tile.V)

                if target_tile.walkable:

                    for box in self.game.boxes:
                        if box.tile == target_tile.number:
                            if box.move('up'):
                                self.velocity_y = self.speed_y
                                self.tile += Tile.V
                            return

                    self.velocity_y = self.speed_y
                    self.tile += Tile.V
                    return

            #Swipe LEFT
            elif angle > 135 and angle < 225:

                self.change_sprite('left')

                target_tile = Tile.get_tile(self.tile - Tile.H)

                if target_tile.walkable:

                    for box in self.game.boxes:
                        if box.tile == target_tile.number:
                            if box.move('left'):
                                self.velocity_x = -self.speed_x
                                self.tile -= Tile.H
                            return

                    self.velocity_x = -self.speed_x
                    self.tile -= Tile.H
                    return

            #Swipe DOWN
            elif angle > 225 and angle < 315:

                self.change_sprite('front')

                target_tile = Tile.get_tile(self.tile - Tile.V)

                if target_tile.walkable:

                    for box in self.game.boxes:
                        if box.tile == target_tile.number:
                            if box.move('down'):
                                self.velocity_y = -self.speed_y
                                self.tile -= Tile.V
                            return

                    self.velocity_y = -self.speed_y
                    self.tile -= Tile.V
                    return

            #Swipe RIGHT
            elif angle > 315 and angle < 360 or angle > 0 and angle < 45:

                self.change_sprite('right')

                target_tile = Tile.get_tile(self.tile + Tile.H)
                
                if target_tile.walkable:

                    for box in self.game.boxes:
                        if box.tile == target_tile.number:
                            if box.move('right'):
                                self.velocity_x = self.speed_x
                                self.tile += Tile.H
                            return

                    self.velocity_x = self.speed_x
                    self.tile += Tile.H

    def change_sprite(self, way):
        if way == 'left':
            self.source = 'img/character_left.png'
        elif way == 'right':
            self.source = 'img/character_right.png'
        elif way == 'back':
            self.source = 'img/character_back.png'
        elif way == 'front':
            self.source = 'img/character.png'

        self.reload()

    def stop(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.moving = False

class Box(Character):

    List = []

    def __init__(self, tile, source, game):
        super(Box, self).__init__(tile, source, game)
        Box.List.append(self)

    def move(self, direction):
        #Check direction and the walkable status of the target tile
        if direction == 'up' and Tile.get_tile(self.tile + Tile.V).walkable:
            self.velocity_y = self.speed_y
            self.tile += Tile.V
            return True
        elif direction == 'right' and Tile.get_tile(self.tile + 1).walkable:
            self.velocity_x = self.speed_x
            self.tile += 1
            return True
        elif direction == 'down' and Tile.get_tile(self.tile - Tile.V).walkable:
            self.velocity_y = -self.speed_y
            self.tile -= Tile.V
            return True
        elif direction == 'left' and Tile.get_tile(self.tile - 1).walkable:
            self.velocity_x = -self.speed_x
            self.tile -= 1
            return True

        return False
