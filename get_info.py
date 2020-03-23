import io

def search_player(name):
    profile_id = []
    steam_id = []
    with io.open("player_list.txt", "r", encoding="utf-8") as f:
        for line in f:
            l = line.split(':')
            if name.lower() == l[0].lower():
                profile_id.append(l[1])
                steam_id.append(l[2])

    return profile_id, steam_id

profile_id_list, steam_id_list = search_player("TescoValue13")
profile_id_list, steam_id_list = search_player("TheViper")
profile_id_list, steam_id_list = search_player("MiniWolskys")