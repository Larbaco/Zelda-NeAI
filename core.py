import random
from map import *
import time

import arcade

scale = 3
COIN_COUNT = 50
res_X = int(256 * scale)
res_Y = int(176 * scale)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 2
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_UP = 2
TEXTURE_DOWN = 3
MUDATELA = 0


class Zenai(arcade.Window):
    """ Main application class. """

    def __init__(self, titulo):
        super().__init__(res_X, res_Y, titulo)
        global world
        world = create_map()
        self.player = Link()
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None
        self.x = 0
        self.y = 0
        self.down = 0
        self.up = 0
        self.left = 0
        self.right = 0
        self.room = gera_room(world, (self.x, self.y), scale)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # self.score = 0

        self.player.set_position(123 * scale, 95 * scale)
        self.colisionmap = gera_colisoes()

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        # map.draw_room(world, (self.x, self.y))

        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"
        self.room.draw()
        self.player.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        collision = 0
        global MUDATELA
        if abs(self.player.velocity[0]) + abs(self.player.velocity[1]) > 0:
            collision = getColisao(self.player.center_x / scale, self.player.center_y / scale, self.x, self.y,
                                   self.colisionmap)
        if collision:
            if self.player.center_x >= (253 * scale) + MOVEMENT_SPEED:
                if self.y < 15:
                    self.player.set_position(0 + MOVEMENT_SPEED, self.player.center_y)
                    self.y += 1
                    MUDATELA = 1
                else:
                    self.player.velocity = [0, 0]
                    self.player.set_position(self.player.center_x - MOVEMENT_SPEED, self.player.center_y)
            elif self.player.center_x < 0 - MOVEMENT_SPEED:
                if self.y > 0:
                    self.player.set_position((250 * scale) - MOVEMENT_SPEED, self.player.center_y)
                    self.y -= 1
                    MUDATELA = 1
                else:
                    self.player.velocity = [0, 0]
                    self.player.set_position(self.player.center_x + MOVEMENT_SPEED, self.player.center_y)
            elif self.player.center_y >= (165 * scale) + MOVEMENT_SPEED:
                if self.x > 0:
                    self.player.set_position(self.player.center_x, (25 * scale) + MOVEMENT_SPEED)
                    self.x -= 1
                    MUDATELA = 1
                else:
                    self.player.velocity = [0, 0]
                    self.player.set_position(self.player.center_x, self.player.center_y - MOVEMENT_SPEED)
            elif self.player.center_y < 25 - MOVEMENT_SPEED:
                if self.x < 7:
                    self.player.set_position(self.player.center_x, (167 * scale) - MOVEMENT_SPEED)
                    self.x += 1
                    MUDATELA = 1
                else:
                    self.player.velocity = [0, 0]
                    self.player.set_position(self.player.center_x, self.player.center_y + MOVEMENT_SPEED)

        elif not MUDATELA:
            self.player.change_y *= (-1)
            self.player.change_x *= (-1)
            # MUDATELA = 0
        if MUDATELA:
            # print(self.x, self.y)
            self.room = gera_room(world, (self.x, self.y), scale)
            MUDATELA = 0

        self.player.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        global MOVEMENT_SPEED
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            exit(1)
        elif key == arcade.key.PLUS:
            print(MOVEMENT_SPEED)
            MOVEMENT_SPEED += 1
        elif key == arcade.key.MINUS:
            print(MOVEMENT_SPEED)
            if abs(MOVEMENT_SPEED) > 1:
                MOVEMENT_SPEED -= 1
        elif key == arcade.key.NUM_MULTIPLY:
            print(MOVEMENT_SPEED)
            MOVEMENT_SPEED *= 2
        elif key == arcade.key.NUM_DIVIDE:
            print(MOVEMENT_SPEED)
            MOVEMENT_SPEED /= 2

    def on_key_release(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0


class Link(arcade.Sprite):
    """ Classe para definir o Link """

    def __init__(self):
        """ Set up Link """
        global scale
        # Call the parent Sprite constructor
        super().__init__()

        texture = arcade.load_texture("sprites/link_esquerda.png", scale=scale)
        self.textures.append(texture)
        texture = arcade.load_texture("sprites/link_direita.png", scale=scale)
        self.textures.append(texture)
        texture = arcade.load_texture("sprites/link_cima.png", scale=scale)
        self.textures.append(texture)
        texture = arcade.load_texture("sprites/link_baixo.png", scale=scale)
        self.textures.append(texture)

        self.set_texture(TEXTURE_LEFT)
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05
        self.respawning = 0

        # Mark that we are respawning.
        self.respawn()

    def respawn(self):
        """
        Called when we die and need to make a new ship.
        'respawning' is an invulnerability timer.
        """
        # If we are in the middle of respawning, this is non-zero.
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0

    def update(self):
        """
        Update our position and other particulars.
        """
        if self.change_x > 0:
            self.set_texture(TEXTURE_RIGHT)
        if self.change_x < 0:
            self.set_texture(TEXTURE_LEFT)
        if self.change_y > 0:
            self.set_texture(TEXTURE_UP)
        if self.change_y < 0:
            self.set_texture(TEXTURE_DOWN)

        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        # self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        # self.change_y = math.cos(math.radians(self.angle)) * self.speed

        # self.center_x += self.change_x
        # self.center_y += self.change_y

        """ Call the parent class. """
        super().update()
