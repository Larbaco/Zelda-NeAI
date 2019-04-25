import random

import arcade
multiplier = 3.8
COIN_COUNT = 50
res_X = int(256 * multiplier)
res_Y = int(240 * multiplier)
SPRITE_SCALING_COIN = 2
SPRITE_SCALING_PLAYER = 2


class Zenai(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(res_X, res_Y)

        self.player_sprite = arcade.Sprite("sprites/character.png", SPRITE_SCALING_PLAYER)
        self.score = 0
        self.coin_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        arcade.set_background_color((155, 192, 122))  # FFC07A

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Create the sprite lists

        # Score

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite.center_x = 50  # Starting position
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("sprites/ruppie.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(res_X)
            coin.center_y = random.randrange(res_Y)

            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()
        self.player_list.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass
