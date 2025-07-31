
import re

world_pos_from_loc = lambda l, o: int(l/8) * 160 + o
loc_pattern = re.compile(
        r"lx(?P<lx>\d+)\s+ly(?P<ly>\d+)\s+ox(?P<ox>[\d.]+)\s+oy(?P<oy>[\d.]+)\s+oz(?P<oz>[\d.]+)"
    )

line_br = "You are on Peregrin server 12 at r1 lx484 ly1058 ox96.75 oy40.22 oz569.47 h94.2. Game timestamp 13645842.737."
line_top = "You are on Peregrin server 12 at r1 lx482 ly1071 ox54.51 oy154.65 oz599.48 h1.4. Game timestamp 13645743.391."
line_left = "You are on Peregrin server 12 at r1 lx473 ly1067 ox38.68 oy65.04 oz598.62 h0. Game timestamp 13647312.196."

map_bounds = {}

#BR
match_br = loc_pattern.search(line_br)
lx = int(match_br.group("lx"))
ly = int(match_br.group("ly"))
ox = float(match_br.group("ox"))
oy = float(match_br.group("oy"))
oz = float(match_br.group("oz"))
world_x = world_pos_from_loc(l=lx, o=ox)
world_y = world_pos_from_loc(l=ly, o=oy)
map_bounds["x_max"] = world_x
map_bounds["y_min"] = world_y


#top
match_top = loc_pattern.search(line_top)
lx = int(match_top.group("lx"))
ly = int(match_top.group("ly"))
ox = float(match_top.group("ox"))
oy = float(match_top.group("oy"))
oz = float(match_top.group("oz"))
world_x = world_pos_from_loc(l=lx, o=ox)
world_y = world_pos_from_loc(l=ly, o=oy)

map_bounds["y_max"] = world_y


#left
match_left = loc_pattern.search(line_left)
lx = int(match_left.group("lx"))
ly = int(match_left.group("ly"))
ox = float(match_left.group("ox"))
oy = float(match_left.group("oy"))
oz = float(match_left.group("oz"))
world_x = world_pos_from_loc(l=lx, o=ox)
world_y = world_pos_from_loc(l=ly, o=oy)

map_bounds["x_min"] = world_x


print(map_bounds)