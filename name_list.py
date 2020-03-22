import io

player_list = []
with io.open("all_players.txt", "r", encoding="utf-8") as f:
    i = 0
    for line in f:
        if i != 0:
            s = line.split(':')
            if f'{s[0]}:{s[1]}:{s[2]}' not in player_list:
                player_list.append(f'{s[0]}:{s[1]}:{s[2]}')
        i += 1

with io.open("teamgame_random.txt", "r", encoding="utf-8") as f:
    i = 0
    for line in f:
        if i != 0:
            s = line.split(':')
            if f'{s[0]}:{s[1]}:{s[2]}' not in player_list:
                player_list.append(f'{s[0]}:{s[1]}:{s[2]}')
        i += 1

with io.open("player_list.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(player_list))
