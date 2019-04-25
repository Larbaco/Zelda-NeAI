import random
import map
import time

import arcade

multiplier = 1
COIN_COUNT = 50
res_X = int(256 * multiplier)
res_Y = int(176 * multiplier)
SPRITE_SCALING_COIN = 2
SPRITE_SCALING_PLAYER = 2


class Zenai(arcade.Window):
    """ Main application class. """

    def __init__(self, titulo):
        super().__init__(res_X, res_Y, titulo)
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None
        arcade.set_background_color((155, 192, 122))  # FFC07A
        self.x = 7
        self.y = 7

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Create the sprite lists

        # Score

        global world
        world = map.create_map()
        for i in range(11):
            a = ''
            for j in range(16):
                a += world[i][j] + '| '
            # print(a)
        # print()

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        print("quadrante x,y ", self.x, self.y)
        map.draw_room(world, (self.x, self.y))

        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            if self.y > 0:
                self.y -= 1;
            else:
                pass
        elif key == arcade.key.RIGHT:
            if self.y < 15:
                self.y += 1;
            else:
                pass
        elif key == arcade.key.UP:
            if self.x > 0:
                self.x -= 1;
            else:
                pass
        elif key == arcade.key.DOWN:
            if self.x < 7:
                self.x += 1;
            else:
                pass
