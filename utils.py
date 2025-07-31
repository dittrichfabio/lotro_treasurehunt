import json
import os
import re
import math
import sys

from definitions import ORIGIN_X, ORIGIN_Y

world_pos_from_loc = lambda l, o: int(l/8) * 160 + o
game_Xpos_from_world_pos = lambda world_x: round((world_x - ORIGIN_X) / 200, 2)
game_Ypos_from_world_pos = lambda world_y: round((world_y - ORIGIN_Y) / 200, 2)
game_position = lambda world_x, world_y: f"{abs(game_Ypos_from_world_pos(world_y=world_y))}{'N' if game_Ypos_from_world_pos(world_y=world_y)>=0 else 'S'}/{abs(game_Xpos_from_world_pos(world_x=world_x))}{'E' if game_Xpos_from_world_pos(world_x=world_x)>=0 else 'W'}"

def extract_loc_data(file_path):
    loc_pattern = re.compile(
        r"lx(?P<lx>\d+)\s+ly(?P<ly>\d+)\s+ox(?P<ox>[\d.]+)\s+oy(?P<oy>[\d.]+)\s+oz(?P<oz>[\d.]+)"
    )
    loc_entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = loc_pattern.search(line)
            if match:
                lx = int(match.group("lx"))
                ly = int(match.group("ly"))
                ox = float(match.group("ox"))
                oy = float(match.group("oy"))
                oz = float(match.group("oz"))
                world_x = world_pos_from_loc(l=lx, o=ox)
                world_y = world_pos_from_loc(l=ly, o=oy)

                entry = {"lx": lx, "ly": ly, "ox": ox, "oy": oy, "oz": oz,
                        "world_x": world_x, "world_y": world_y}
                print(entry)
                loc_entries.append(entry)

    return loc_entries

def deduplicate(entries, epsilon=0.5):
    unique = []
    for e in entries:
        if not any(math.hypot(e['world_x'] - u['world_x'], e['world_y'] - u['world_y']) < epsilon for u in unique):
            unique.append(e)
        else:
            print(e)
    return unique

def load_digsites(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run in 'extract' mode first.")
        sys.exit(1)
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)