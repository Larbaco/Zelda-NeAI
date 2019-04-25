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
        self.pos_x_personagem = 88
        self.pos_y_personagem = 128
        self.down = 0
        self.up = 0
        self.left = 0
        self.right = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Create the sprite lists
        self.player = arcade.Sprite('sprites/character.png', multiplier)
        self.player.set_position(self.pos_y_personagem, self.pos_x_personagem)
        self.player.draw()
        # Score

        global world
        world = map.create_map()
        for i in range(11):
            a = ''
            for j in range(16):
                a += world[i][j] + '| '
            # print(a)
        # print()
        self.colisionmap = map.gera_colisoes()

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        # print("quadrante x,y ", self.x, self.y)
        map.draw_room(world, (self.x, self.y))

        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"

        self.player.set_position(self.pos_y_personagem, self.pos_x_personagem)
        self.player.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        colisao = map.getColisao(self.pos_x_personagem + 1, self.pos_y_personagem + 1, self.x, self.y, self.colisionmap)
        if self.left:
            if self.pos_y_personagem > 0:
                if colisao:
                    pass
                self.pos_y_personagem -= 2;
            else:
                self.pos_y_personagem = 249
                self.y -= 1;
                pass
        elif self.right:
            if self.pos_y_personagem < 250:
                self.pos_y_personagem += 2;
            else:
                self.pos_y_personagem = 0
                self.y += 1
                pass
        elif self.down:
            if self.pos_x_personagem > 0:
                self.pos_x_personagem -= 2;

            else:
                self.pos_x_personagem = 165
                self.x += 1
                pass
        elif self.up:
            if self.pos_x_personagem < 170:
                self.pos_x_personagem += 2;
            else:
                self.pos_x_personagem = 0
                self.x -= 1
                pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.left = 1
        elif key == arcade.key.RIGHT:
            self.right = 1
        elif key == arcade.key.DOWN:
            self.down = 1
        elif key == arcade.key.UP:
            self.up = 1

    def on_key_release(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.left = 0
        elif key == arcade.key.RIGHT:
            self.right = 0
        elif key == arcade.key.DOWN:
            self.down = 0
        elif key == arcade.key.UP:
            self.up = 0
