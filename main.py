from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock

from math import atan

from constants import *
from tile import *
from level import *

class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

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
                target_tile = Tile.get_tile(self.tile + Tile.V)
                if target_tile.walkable:

                    for box in self.game.boxes:
                        if box.tile == target_tile.number:
                            if box.move('up'):
                                self.change_sprite('back')
                                self.velocity_y = self.speed_y
                                self.tile += Tile.V
                            return

                    self.change_sprite('back')
                    self.velocity_y = self.speed_y
                    self.tile += Tile.V
                    return

            #Swipe LEFT
            elif angle > 135 and angle < 225:
                target_tile = Tile.get_tile(self.tile - 1)
                if target_tile.walkable:

                    for box in self.game.boxes:
                        if box.tile == target_tile.number:
                            if box.move('left'):
                                self.change_sprite('left')
                                self.velocity_x = -self.speed_x
                                self.tile -= 1
                            return

                    self.change_sprite('left')
                    self.velocity_x = -self.speed_x
                    self.tile -= 1
                    return

            #Swipe DOWN
            elif angle > 225 and angle < 315:
                target_tile = Tile.get_tile(self.tile - Tile.V)
                if target_tile.walkable:

                    for box in self.game.boxes:
                        if box.tile == target_tile.number:
                            if box.move('down'):
                                self.change_sprite('front')
                                self.velocity_y = -self.speed_y
                                self.tile -= Tile.V
                            return

                    self.change_sprite('front')
                    self.velocity_y = -self.speed_y
                    self.tile -= Tile.V
                    return

            #Swipe RIGHT
            elif angle > 315 and angle < 360 or angle > 0 and angle < 45:
                target_tile = Tile.get_tile(self.tile + 1)
                if target_tile.walkable:

                    for box in self.game.boxes:
                        if box.tile == target_tile.number:
                            if box.move('right'):
                                self.change_sprite('right')
                                self.velocity_x = self.speed_x
                                self.tile += 1
                            return

                    self.change_sprite('right')
                    self.velocity_x = self.speed_x
                    self.tile += 1

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


class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.player = None
        self.level = Level.load_level(1337)
        self.boxes = []

        #Add bg widget first to not cover other sprites
        #Also scale the game size to the bg size
        self.background = Sprite(source='img/background.png')
        self.size = self.background.size
        self.add_widget(self.background)

        Tile.make_tiles(self.size, self.level)
        #Calculate the horizontal and vertical differences in tiles
        Tile.V, Tile.H = self.size[0] / Tile.width, self.size[1] / Tile.height

        #Add proper widgets for every non-empty tile in the Tile.List
        for tile in Tile.List:
            if tile.type != 'empty':
                if Tile.get_tile(tile.number - Tile.V).walkable:
                    self.add_widget(Sprite(source=Tile.image_files[tile.type], pos=(tile.x, tile.y)))
                else:
                    self.add_widget(Sprite(source=Tile.image_files[tile.type + '_edge'], pos=(tile.x, tile.y - SPRITE_EDGE_OFFSET)))

        self.player = Character(self.level.playerspawn, 'img/character.png', self)
        self.add_widget(self.player)

        for tile in self.level.boxspawn:
            self.boxes.append(Box(tile, 'img/box.png', self))
        for box in self.boxes:
            self.add_widget(box)

        self.add_widget(Label(text="Level {}".format(self.level.level), pos=(0, self.height - 80), font_name=APP_FONT, font_size=20, color=(240,240,240,0.8)))

        #Schedule an interval for the game update function
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, *ignore):
        self.player.update()
        for box in self.boxes:
            box.update()

class Application(App):
    def build(self):
        self.game = Game()
        Window.size = self.game.size #[420, 700]
        Window.bind(on_motion=self.on_touch_move)
        return self.game

    def on_touch_move(self, window, etype, touch):
        if etype == 'end' and touch.opos != (None, None):
            deltaX = touch.pos[0] - touch.opos[0]
            deltaY = touch.pos[1] - touch.opos[1]

            if deltaX:
                if deltaX < 0:
                    angle = 180 + atan(deltaY / deltaX) * (180/3.14)
                elif deltaY < 0:
                    if deltaX < 0:
                        angle = 360 + atan(deltaY / deltaX) * (180/3.14)
                    else:
                        angle = 360 - atan(deltaY / deltaX) * (180/3.14)
                else:
                    angle = atan(deltaY / deltaX) * (180/3.14)

                self.game.player.move(angle)

                print(angle)

if __name__ == "__main__":
    Application().run()
