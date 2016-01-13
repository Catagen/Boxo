from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock

from math import atan

from constants import *
from objects import *
from tile import *
from level import *

class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.level = Level.load_level(1337)
        self.background = Sprite(source='img/background.png')
        self.size = self.background.size
        self.player = None
        self.boxes = []

        #Initiate the game by creating tiles
        Tile.make_tiles(self.size, self.level)

        #Add bg widget first to not cover other sprites
        self.add_widget(self.background)

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

        boxes_on_point = 0
        for box in self.boxes:
            box.update()
            if box.tile in self.level.blockpoints:
                boxes_on_point += 1

        if boxes_on_point == len(self.boxes):
            print('Level {} beat!'.format(self.level.level))

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
