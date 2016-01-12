from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock

from tile import Tile
from level import Level

class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

class Character(Sprite):
    def __init__(self, pos):
        super(Character, self).__init__(source='img/character.png', pos=pos)
        self.velocity_y = 0
        self.gravity = -0.3

    def update(self):
        self.velocity_y += self.gravity
        self.velocity_y = max(self.velocity_y, -10)
        self.y += self.velocity_y

    def on_touch_down(self, *ignore):
        self.velocity_y = 5.5

class Background(Sprite):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)
    def update(self):
        self.image.x -= 2
        self.image_dupe.x -= 2

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width

class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()

        self.level = Level(1, [10,11,12,25], [11,12])
        Tile.make_tiles(self.size, self.level)

        self.background = Background(source='img/background.png')
        self.size = self.background.size
        self.add_widget(self.background)
        self.character = Character(pos=(20, self.height/2))
        self.add_widget(self.character)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, *ignore):
        self.background.update()
        self.character.update()

class Application(App):
    def build(self):
        game = Game()
        Window.size = game.size #[420, 700]
        return game

if __name__ == "__main__":
    Application().run()
