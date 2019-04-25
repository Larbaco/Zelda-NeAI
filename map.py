import arcade
import misc

multiplier = 1


def create_map():
    tiles = {}
    world_map = []
    for x in range(256):
        world_map += [misc.WORLD_MAP_DATA[x * 256:x * 256 + 256]]
    return world_map


def draw_room(world_map, pos):
    sprite_tiles = arcade.SpriteList()
    debug = ''
    for linha in range(11):
        for coluna in range(16):
            # print(world_y, world_x)
            tile_linha = (pos[0]*11)+linha
            tile_coluna= (pos[1]*16)+coluna
            tile = arcade.Sprite('sprites/' + world_map[tile_linha][tile_coluna] + '.png',multiplier)
            tile.set_position((multiplier*(coluna*16)+8),(multiplier*(167-(linha*16))))
            #tile.center_x = ((coluna * 16) + 8)
            #tile.center_y = ((linha * 16) + 8)
            sprite_tiles.append(tile)
            # debug += world_map[pos[0] + x][pos[1] + y] + ' '
    sprite_tiles.draw()
