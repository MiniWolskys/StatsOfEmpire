import io

def search_player(name):
    profile_id = ""
    steam_id = ""
    with io.open("player_list.txt", "r", encoding="utf-8") as f:
        for line in f:
            l = line.split(':')
            if name.lower() == l[0].lower():
                profile_id = l[1]
                steam_id = l[2]

search_player("TescoValue13")
search_player("TheViper")
search_player("MiniWolskys")