import arcade
from misc import *


def create_map():
    tiles = {}
    world_map = []
    for x in range(256):
        world_map += [WORLD_MAP_DATA[x * 256:x * 256 + 256]]
    return world_map


def gera_room(world_map, pos, scale):
    sprite_tiles = arcade.SpriteList()
    for linha in range(11):
        for coluna in range(16):
            tile_linha = (pos[0] * 11) + linha
            tile_coluna = (pos[1] * 16) + coluna
            tile = arcade.Sprite('sprites/' + world_map[tile_linha][tile_coluna] + '.png', scale*1.05)
            tile.set_position((scale * ((coluna * 16) + 8)), (scale * (176 - (linha * 16) - 8)))
            sprite_tiles.append(tile)
    return sprite_tiles


def gera_colisoes():
    mapa_colisoes = []
    file = open('Colisoes.txt')
    for linha in file:
        mapa_colisoes += [linha.split()]
    # print(mapa_colisoes)
    return mapa_colisoes


def getColisao(player_x, player_y, room_x, room_y, colisionmap):
    if player_y < 15 or player_y > 164:
        return 1
    if player_x < 10 or player_x > 250:
        return 1
    coluna = (16 * room_y) + int(player_x / 16)
    linha = (11 * room_x) + int((14 - (player_y / 13)) - 1)

    print(player_x, player_y, linha, coluna, room_x, room_y)
    print(colisionmap[linha][0][coluna])
    if colisionmap[linha][0][coluna] == 'X':
        return 0
    else:
        return 1
