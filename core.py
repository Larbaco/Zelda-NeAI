import random
from map import *
import time
from game_state import GameState
import os
import arcade

project_root = os.path.dirname(os.path.abspath(__file__))

scale = 3
COIN_COUNT = 50
res_X = int(256 * scale)
res_Y = int(176 * scale)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_UP = 2
TEXTURE_DOWN = 3


class Zenai(arcade.Window):
    """ Main application class. """

    def __init__(self, titulo):
        super().__init__(res_X, res_Y, titulo)
        
        # Replace global state with GameState class
        self.game_state = GameState()
        
        # Sprite management for Arcade 3.2.0 compatibility
        self.player_list = None
        
        global world
        world = create_map()

        self.last_time = None
        self.frame_count = 0
        self.fps_message = None
        self.down = 0
        self.up = 0
        self.left = 0
        self.right = 0
        
        # Use GameState for room coordinates
        self.room = gera_room(world, (self.game_state.current_room_x, self.game_state.current_room_y), scale)

    def setup(self):
        """ Set up the game and initialize the variables. """
        
        # Initialize sprite lists (Arcade 3.2.0 compatibility)
        self.player_list = arcade.SpriteList()

        # Create and add player sprite
        self.player = Link()
        self.player_list.append(self.player)

        self.colisionmap = gera_colisoes()
        self.player.center_x = 123 * scale
        self.player.center_y = 95 * scale

    def on_draw(self):
        """ Draw everything """
        
        # Clear screen (Arcade 3.2.0 - replaces arcade.start_render())
        self.clear()
        
        # FPS calculation
        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"
        
        # Draw room and sprites
        self.room.draw()
        # Use SpriteList for rendering (Arcade 3.2.0 compatibility)
        self.player_list.draw()
        
        # Update frame tracking
        self.frame_count += 1
        self.last_time = time.time()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        collision = 0
        
        if abs(self.player.change_x) + abs(self.player.change_y) > 0:
            collision = getColisao(self.player.center_x / scale, self.player.center_y / scale, 
                                 self.game_state.current_room_x, self.game_state.current_room_y,
                                 self.colisionmap)
        
        if collision:
            # Room transition logic - right edge
            if self.player.center_x >= (253 * scale) + self.game_state.movement_speed:
                if self.game_state.current_room_y < 15:
                    self.player.center_x = 0 + self.game_state.movement_speed
                    self.game_state.current_room_y += 1
                    self.game_state.room_transition_pending = True
                else:
                    self.player.change_x = 0
                    self.player.change_y = 0
                    self.player.center_x = self.player.center_x - self.game_state.movement_speed
            
            # Room transition logic - left edge
            elif self.player.center_x < 0 - self.game_state.movement_speed:
                if self.game_state.current_room_y > 0:
                    self.player.center_x = (250 * scale) - self.game_state.movement_speed
                    self.game_state.current_room_y -= 1
                    self.game_state.room_transition_pending = True
                else:
                    self.player.change_x = 0
                    self.player.change_y = 0
                    self.player.center_x = self.player.center_x + self.game_state.movement_speed
            
            # Room transition logic - top edge
            elif self.player.center_y >= (165 * scale) + self.game_state.movement_speed:
                if self.game_state.current_room_x > 0:
                    self.player.center_y = (25 * scale) + self.game_state.movement_speed
                    self.game_state.current_room_x -= 1
                    self.game_state.room_transition_pending = True
                else:
                    self.player.change_x = 0
                    self.player.change_y = 0
                    self.player.center_y = self.player.center_y - self.game_state.movement_speed
            
            # Room transition logic - bottom edge
            elif self.player.center_y < 25 - self.game_state.movement_speed:
                if self.game_state.current_room_x < 7:
                    self.player.center_y = (167 * scale) - self.game_state.movement_speed
                    self.game_state.current_room_x += 1
                    self.game_state.room_transition_pending = True
                else:
                    self.player.change_x = 0
                    self.player.change_y = 0
                    self.player.center_y = self.player.center_y + self.game_state.movement_speed

        elif not self.game_state.room_transition_pending:
            # Bounce back from collision
            self.player.change_y *= (-1)
            self.player.change_x *= (-1)
        
        # Generate new room if transitioning
        if self.game_state.room_transition_pending:
            self.room = gera_room(world, (self.game_state.current_room_x, self.game_state.current_room_y), scale)
            self.game_state.room_transition_pending = False

        self.player.update()
        
    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.player.change_x = -self.game_state.movement_speed
        elif key == arcade.key.RIGHT:
            self.player.change_x = self.game_state.movement_speed
        elif key == arcade.key.DOWN:
            self.player.change_y = -self.game_state.movement_speed
        elif key == arcade.key.UP:
            self.player.change_y = self.game_state.movement_speed
        elif key == arcade.key.ESCAPE:
            exit(1)
        elif key == arcade.key.PLUS:
            print(self.game_state.movement_speed)
            self.game_state.movement_speed += 1
        elif key == arcade.key.MINUS:
            print(self.game_state.movement_speed)
            if abs(self.game_state.movement_speed) > 1:
                self.game_state.movement_speed -= 1
        elif key == arcade.key.NUM_MULTIPLY:
            print(self.game_state.movement_speed)
            self.game_state.movement_speed *= 2
        elif key == arcade.key.NUM_DIVIDE:
            print(self.game_state.movement_speed)
            self.game_state.movement_speed /= 2

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
        
        # Initialize with default texture for Arcade 3.2.0 compatibility
        try:
            default_texture = arcade.load_texture(os.path.join(project_root, "sprites", "link_esquerda.png"))
            super().__init__(default_texture, scale=float(scale))
        except FileNotFoundError:
            # Fallback for missing sprites
            fallback_texture = arcade.Texture.create_filled("link_fallback", (16, 16), arcade.color.GREEN)
            super().__init__(fallback_texture, scale=float(scale))

        # Load directional textures
        self.textures = []
        texture_files = [
            "link_esquerda.png",   # TEXTURE_LEFT = 0
            "link_direita.png",    # TEXTURE_RIGHT = 1
            "link_cima.png",       # TEXTURE_UP = 2
            "link_baixo.png"       # TEXTURE_DOWN = 3
        ]
        
        for texture_file in texture_files:
            try:
                texture_path = os.path.join(project_root, "sprites", texture_file)
                texture = arcade.load_texture(texture_path)
                self.textures.append(texture)
            except FileNotFoundError:
                # Fallback for missing textures
                fallback = arcade.Texture.create_filled(f"link_{len(self.textures)}", (16, 16), arcade.color.RED)
                self.textures.append(fallback)

        # Set initial texture
        if len(self.textures) > 0:
            self.set_texture(TEXTURE_LEFT)

        # Initialize sprite properties
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05
        self.respawning = 0
        
        # Set initial position
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0

    def respawn(self):
        """
        Called when we die and need to make a new ship.
        'respawning' is an invulnerability timer.
        """
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0

    def update(self):
        """
        Update our position and other particulars.
        """
        # Update texture based on movement direction
        if len(self.textures) >= 4:
            if self.change_x > 0:
                self.set_texture(TEXTURE_RIGHT)
            elif self.change_x < 0:
                self.set_texture(TEXTURE_LEFT)
            elif self.change_y > 0:
                self.set_texture(TEXTURE_UP)
            elif self.change_y < 0:
                self.set_texture(TEXTURE_DOWN)

        # Speed limits
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        # Call parent class update
        super().update()
        
    # Note: draw() method removed - SpriteList handles rendering in Arcade 3.2.0