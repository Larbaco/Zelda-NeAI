import arcade
from misc import *


def create_map():
    tiles = {}
    world_map = []
    for x in range(256):
        world_map += [WORLD_MAP_DATA[x * 256:x * 256 + 256]]
    return world_map


def gera_room(world_map, pos, scale):
    import os

    project_root = os.path.dirname(os.path.abspath(__file__))

    sprite_tiles = arcade.SpriteList()
    for linha in range(11):
        for coluna in range(16):
            tile_linha = (pos[0] * 11) + linha
            tile_coluna = (pos[1] * 16) + coluna
            sprite_path = os.path.join(project_root, 'sprites', world_map[tile_linha][tile_coluna] + '.png')
            tile = arcade.Sprite(sprite_path)
            tile.scale = scale * 1.05
            tile.center_x = scale * ((coluna * 16) + 8)
            tile.center_y = scale * (176 - (linha * 16) - 8)
            sprite_tiles.append(tile)
    return sprite_tiles


def gera_colisoes():
    import os
    mapa_colisoes = []
    
    # Try multiple possible locations for Colisoes.txt
    possible_paths = [
        'Colisoes.txt',  # Current directory
        os.path.join('..', 'Colisoes.txt'),  # Parent directory
        os.path.join('..', '..', 'Colisoes.txt'),  # Two levels up
    ]
    
    collision_file = None
    for path in possible_paths:
        if os.path.exists(path):
            collision_file = path
            break
    
    if not collision_file:
        print("Error: Colisoes.txt not found in any expected location")
        return []
    
    try:
        with open(collision_file, 'r') as file:
            for linha in file:
                linha = linha.strip()  # Remove whitespace
                if linha:  # Skip empty lines
                    mapa_colisoes.append(linha.split())
        print(f"Loaded collision map from: {collision_file}")
        return mapa_colisoes
    except Exception as e:
        print(f"Error loading collision map: {e}")
        return []


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
