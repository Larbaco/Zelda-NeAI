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
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
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

        # Spawn em area aberta (centro da sala 0,0), longe das paredes
        self.player.center_x = 180 * scale
        self.player.center_y = 92 * scale
        self.colisionmap = gera_colisoes()

    def on_draw(self):
        """ Draw everything """
        self.clear()
        # map.draw_room(world, (self.x, self.y))

        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"
        self.room.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        global MUDATELA

        # 1) Transicao de sala: jogador alcancou uma borda da janela
        if self.player.center_x >= res_X - MOVEMENT_SPEED:
            if self.y < 15:
                self.player.center_x = 0 + MOVEMENT_SPEED
                self.y += 1
                MUDATELA = 1
            else:
                self.player.center_x = self.player.center_x - MOVEMENT_SPEED
        elif self.player.center_x <= MOVEMENT_SPEED:
            if self.y > 0:
                self.player.center_x = res_X - MOVEMENT_SPEED
                self.y -= 1
                MUDATELA = 1
            else:
                self.player.center_x = self.player.center_x + MOVEMENT_SPEED
        elif self.player.center_y >= res_Y - MOVEMENT_SPEED:
            if self.x > 0:
                self.player.center_y = MOVEMENT_SPEED
                self.x -= 1
                MUDATELA = 1
            else:
                self.player.center_y = self.player.center_y - MOVEMENT_SPEED
        elif self.player.center_y <= MOVEMENT_SPEED:
            if self.x < 7:
                self.player.center_y = res_Y - MOVEMENT_SPEED
                self.x += 1
                MUDATELA = 1
            else:
                self.player.center_y = self.player.center_y + MOVEMENT_SPEED

        # 2) Colisao com parede interna (fora das bordas de transicao)
        elif abs(self.player.change_x) + abs(self.player.change_y) > 0:
            # Checa a posicao ALVO (atual + velocidade) com bounding box do sprite
            target_x = self.player.center_x + self.player.change_x
            target_y = self.player.center_y + self.player.change_y
            # Hitbox menor que o sprite (fator 0.5): evita grudar em corredores
            half_w = ((self.player.width / 2) / scale) * 0.5
            half_h = ((self.player.height / 2) / scale) * 0.5
            collision = getColisaoBox(target_x / scale, target_y / scale, self.x, self.y,
                                      self.colisionmap, half_w, half_h)
            if collision:
                # Parede interna: para o jogador (nao atravessa, nao quica)
                self.player.change_x = 0
                self.player.change_y = 0

        if MUDATELA:
            # print(self.x, self.y)
            self.room = gera_room(world, (self.x, self.y), scale)
            MUDATELA = 0

        self.player.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        global MOVEMENT_SPEED
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.UP or key == arcade.key.W:
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
        if key == arcade.key.UP or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0


class Link(arcade.Sprite):
    """ Classe para definir o Link """

    def __init__(self):
        """ Set up Link """
        global scale
        # Call the parent Sprite constructor
        super().__init__()
        self.scale = scale / 2

        texture = arcade.load_texture("sprites/link_esquerda.png")
        self.textures.append(texture)
        texture = arcade.load_texture("sprites/link_direita.png")
        self.textures.append(texture)
        texture = arcade.load_texture("sprites/link_cima.png")
        self.textures.append(texture)
        texture = arcade.load_texture("sprites/link_baixo.png")
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
