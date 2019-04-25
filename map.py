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
    for linha in range(11):
        for coluna in range(16):
            tile_linha = (pos[0] * 11) + linha
            tile_coluna = (pos[1] * 16) + coluna
            tile = arcade.Sprite('sprites/' + world_map[tile_linha][tile_coluna] + '.png', multiplier)
            tile.set_position((multiplier * (coluna * 16) + 8), (multiplier * (167 - (linha * 16))))
            sprite_tiles.append(tile)
    sprite_tiles.draw()


def gera_colisoes():
    mapa_colisoes = []
    file = open('Colisoes.txt')
    for linha in file:
        mapa_colisoes += [linha.split()]
    print(mapa_colisoes)
    return mapa_colisoes


def getColisao(pos_x_personagem, pos_y_personagem, room_x, room_y, colisionmap):
    coluna = (pos_y_personagem / 16)
    linha = (14 - (pos_x_personagem / 11))
    linha = int(linha)
    coluna = int(coluna)
    print(linha, coluna, room_x, room_y)
    #print(colisionmap[linha])
